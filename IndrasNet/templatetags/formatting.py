from django.contrib.humanize.templatetags.humanize import intcomma
from django import template

register = template.Library()

def to_int(num):
    return int(num)

def to_int_comma(num):
    return intcomma(int(num))

def to_float_2(num):
    return round(float(num), 2)

def class_name(ob):
    return ob.__class__.__name__

register.filter('to_int', to_int)
register.filter('to_int_comma', to_int_comma)
register.filter('to_float_2', to_float_2)
register.filter('class_name', class_name)