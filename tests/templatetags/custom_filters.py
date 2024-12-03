from django import template

register = template.Library()

@register.filter(name='get_value')
def get_value(value, key):
    """
    Фильтр для получения значения из словаря по ключу.
    """
    if isinstance(value, dict):
        return value.get(key)
    return None