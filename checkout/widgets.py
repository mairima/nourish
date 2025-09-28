from django_countries.widgets import CountrySelectWidget as _Base
from django_countries import countries

class SafeCountrySelectWidget(_Base):
    @property
    def choices(self):
        base = getattr(self, "_choices", None)
        if base is None:
            return list(countries)
        try:
            return list(base)
        except Exception:
            return list(countries)

    @choices.setter
    def choices(self, value):
        self._choices = list(value) if value is not None else []
