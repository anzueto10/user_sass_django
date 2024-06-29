from django import template
from django.utils import timezone
from django.utils.timezone import localtime

register = template.Library()


@register.filter
def date_format(value):
    now = timezone.now()
    value = localtime(value)

    delta = now - value
    if delta.days == 0:
        return f"Hoy, {value.strftime('%H:%M')}"
    elif delta.days == 1:
        return f"Ayer, {value.strftime('%H:%M')}"
    elif 2 <= delta.days <= 3:
        return f"Hace {delta.days} días, {value.strftime('%H:%M')}"
    else:
        return value.strftime("%d de %B de %Y, %H:%M")
