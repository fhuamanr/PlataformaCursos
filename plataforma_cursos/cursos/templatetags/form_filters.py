from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})


@register.filter(name='add_attrs')
def add_attrs(field, attr_string):
    attrs = {}
    for attr in attr_string.split(','):
        key, value = attr.split(':')
        attrs[key.strip()] = value.strip()
    return field.as_widget(attrs=attrs)