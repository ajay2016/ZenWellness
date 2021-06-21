from django import template

register = template.Library()


@register.filter(name='add_class')
def addclass(value, arg):
    value.field.widget.attrs.update({'class': arg})
    return value
