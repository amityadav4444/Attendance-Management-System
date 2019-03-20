# teacher/login/templatetags/getattribute.py

import re
from django import template
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()

def getattribute(value, arg):
	"""Gets an attribute of an object dynamically from a string name"""
	
	try:
		return value[arg]
	except:
		print('no')
		return settings.string_if_invalid
register.filter('getattribute', getattribute)


def index(sequence, position):
    return sequence[position]
	
register.filter('index',index)