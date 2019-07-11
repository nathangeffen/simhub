from django import template

register = template.Library()

@register.filter(name='starts_with')
def starts_with(value, arg):
    return value.field_subset(arg)
