from django.contrib.humanize.templatetags.humanize import intcomma
from django import template

register = template.Library()

def to_int(num):
    return intcomma(int(num))

register.filter('to_int', to_int)