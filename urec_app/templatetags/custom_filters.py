from ..models import RECURRENCE_CHOICES

from django import template


register = template.Library()


@register.filter
def display_recurrence(recurrence_pattern):
    readable_pattern = "None"
    for CHOICE, READABLE_CHOICE in RECURRENCE_CHOICES:
        if recurrence_pattern == CHOICE:
            readable_pattern = READABLE_CHOICE
    return readable_pattern
