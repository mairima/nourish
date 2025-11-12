from decimal import Decimal
from django import template

register = template.Library()


@register.filter
def calc_subtotal(price, quantity):
    # Return price × quantity rounded to 2 decimals
    try:
        p = Decimal(str(price))
        q = int(quantity)
        return (p * q).quantize(Decimal("0.01"))
    except Exception:
        return ""
