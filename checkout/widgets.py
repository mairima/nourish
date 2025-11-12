from django_countries.widgets import CountrySelectWidget as _Base
from django_countries import countries


class SafeCountrySelectWidget(_Base):
    """A safe CountrySelectWidget that avoids iterator reuse issues."""

    @property
    def choices(self):
        """Return a concrete list of country choices."""
        base = getattr(self, "_choices", None)
        if base is None:
            return list(countries)
        try:
            return list(base)
        except Exception:
            return list(countries)

    @choices.setter
    def choices(self, value):
        """Set choices safely, always converting to a list."""
        self._choices = list(value) if value is not None else []
