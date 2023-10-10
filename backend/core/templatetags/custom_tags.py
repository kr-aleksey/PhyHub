from django import template

register = template.Library()


@register.filter
def add_class(value, arg):
    try:
        value.field.widget.attrs['class'] = arg
    except AttributeError:
        return value
    return value


@register.simple_tag
def widget_with_attrs(field, **attrs):
    field.field.widget.attrs.update(attrs)
    field.field.widget.attrs['type'] = 'datetime-local'
    return field
