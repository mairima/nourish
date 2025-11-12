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
APP_LABELS = [
    "products",
    "checkout",
    "profiles",
    "contact",
    "newsletter",
    "faqs",
    "home",
]


def field_decl(field: models.Field) -> str:
    """Return a Mermaid-friendly field declaration."""
    name = field.name
    pk = " PK" if getattr(field, "primary_key", False) or name == "id" else ""

    if isinstance(field, models.AutoField) or name == "id":
        dtype = "int"
    elif isinstance(field, models.CharField):
        dtype = "varchar"
    elif isinstance(field, models.TextField):
        dtype = "text"
    elif isinstance(field, models.EmailField):
        dtype = "varchar"
    elif isinstance(field, models.DecimalField):
        dtype = "decimal"
    elif isinstance(field, models.BooleanField):
        dtype = "bool"
    elif isinstance(field, models.DateTimeField):
        dtype = "datetime"
    elif isinstance(field, models.IntegerField):
        dtype = "int"
    elif isinstance(field, models.ForeignKey):
        dtype = "int"  # show FK inline
    else:
        dtype = field.__class__.__name__.lower()

    return f"        {dtype} {name}{pk}"


def rel_line(from_model, to_model, rel_type, label):
    """
    Return a Mermaid relationship line.

    Mermaid cardinalities:
      one-to-many  : '||--o{'
      many-to-one  : '}o--||'
      one-to-one   : '||--||'
      many-to-many : '}o--o{'
    """
    if rel_type == "fk":
        return f"    {from_model} }}o--|| {to_model} : {label}"
    if rel_type == "o2o":
        return f"    {from_model} ||--|| {to_model} : {label}"
    if rel_type == "m2m":
        return f"    {from_model} }}o--o{{ {to_model} : {label}"
    return ""


lines = ["erDiagram"]
relations = []

for model in apps.get_models():
    app_label = model._meta.app_label
    if APP_LABELS and app_label not in APP_LABELS:
        continue

    model_name = model.__name__
    lines.append(f"    {model_name} {{")

    for field in model._meta.get_fields():
        if field.auto_created and not field.concrete:
            continue
        if isinstance(
            field,
            (
                models.ManyToOneRel,
                models.ManyToManyRel,
                models.OneToOneRel,
            ),
        ):
            continue
        lines.append(field_decl(field))

    lines.append("    }")
    lines.append("")

    for field in model._meta.get_fields():
        parent = getattr(field.remote_field, "model", None)
        if not parent:
            continue
        parent_name = parent.__name__

        if isinstance(field, models.ForeignKey):
            relations.append(
                rel_line(model_name, parent_name, "fk", field.name)
            )
        elif isinstance(field, models.OneToOneField):
            relations.append(
                rel_line(model_name, parent_name, "o2o", field.name)
            )
        elif isinstance(field, models.ManyToManyField):
            relations.append(
                rel_line(model_name, parent_name, "m2m", field.name)
            )

# Append unique relations
for rel in sorted(set(relations)):
    if rel.strip():
        lines.append(rel)

with open(OUTPUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))

print(f"✅ Mermaid ERD written to {OUTPUT}")
