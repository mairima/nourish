import os
import django
from django.apps import apps
from django.db import models

# Configure Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nourish.settings")
django.setup()

OUTPUT = "documentation/erd.mmd"
os.makedirs("documentation", exist_ok=True)

# Which apps to include (edit as needed)
APP_LABELS = ["products", "checkout", "profiles", "contact", "newsletter", "faqs", "home"]

def field_decl(f: models.Field) -> str:
    # Basic Mermaid-friendly dtype names
    name = f.name
    pk = " PK" if getattr(f, "primary_key", False) or name == "id" else ""
    if isinstance(f, models.AutoField) or name == "id":
        dtype = "int"
    elif isinstance(f, models.CharField):
        dtype = "varchar"
    elif isinstance(f, models.TextField):
        dtype = "text"
    elif isinstance(f, models.EmailField):
        dtype = "varchar"
    elif isinstance(f, models.DecimalField):
        dtype = "decimal"
    elif isinstance(f, models.BooleanField):
        dtype = "bool"
    elif isinstance(f, models.DateTimeField):
        dtype = "datetime"
    elif isinstance(f, models.IntegerField):
        dtype = "int"
    elif isinstance(f, models.ForeignKey):
        # Show FK column inline; relation will be drawn separately
        dtype = "int"
    else:
        dtype = f.__class__.__name__.lower()
    return f"        {dtype} {name}{pk}"

def rel_line(from_model, to_model, rel_type, label):
    """
    Mermaid cardinalities:
      one-to-many  : '||--o{'
      many-to-one  : '}o--||'
      one-to-one   : '||--||'
      many-to-many : '}o--o{'
    We render from child -> parent for FK (many-to-one).
    """
    if rel_type == "fk":
        return f"    {from_model} }}o--|| {to_model} : {label}"
    if rel_type == "o2o":
        return f"    {from_model} ||--|| {to_model} : {label}"
    if rel_type == "m2m":
        return f"    {from_model} }}o--o{{ {to_model} : {label}"
    return ""

lines = ["erDiagram"]
models_seen = []
relations = []

for model in apps.get_models():
    app_label = model._meta.app_label
    if APP_LABELS and app_label not in APP_LABELS:
        continue

    model_name = model.__name__
    models_seen.append(model_name)

    # Table block
    lines.append(f"    {model_name} {{")
    # fields
    for f in model._meta.get_fields():
        # Skip reverse relations in the field list
        if f.auto_created and not f.concrete:
            continue
        if isinstance(f, (models.ManyToOneRel, models.ManyToManyRel, models.OneToOneRel)):
            continue
        lines.append(field_decl(f))
    lines.append("    }")
    lines.append("")

    # Relations
    for f in model._meta.get_fields():
        if isinstance(f, models.ForeignKey):
            parent = f.remote_field.model.__name__
            relations.append(rel_line(model_name, parent, "fk", f.name))
        elif isinstance(f, models.OneToOneField):
            parent = f.remote_field.model.__name__
            relations.append(rel_line(model_name, parent, "o2o", f.name))
        elif isinstance(f, models.ManyToManyField):
            parent = f.remote_field.model.__name__
            relations.append(rel_line(model_name, parent, "m2m", f.name))

# Append unique relations to avoid duplicates
for r in sorted(set(relations)):
    if r.strip():
        lines.append(r)

with open(OUTPUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))

print(f"✅ Mermaid ERD written to {OUTPUT}")
