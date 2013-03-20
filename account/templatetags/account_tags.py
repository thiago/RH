__author__ = 'thiago.rodrigues'

from django import template
register = template.Library()

@register.filter('get_info')
def get_info(user, attr):
	# USAGE: {{ USER|get_info:"telefone" }}
	# {% with tel=USER|get_info:"telefone" %}
	#	...
	# {% endwith %}
	return user.profile.get_info(attr)

@register.filter('get_avatar')
def get_avatar(user, size=None):
	# USAGE: {{ USER|get_avatar:"square" }}
	# Default is 'square' but you can use 'square', 'small', 'normal' or 'large'
	# You can set must values with variable "ACCOUNT_SIZES" in settings file.
	return user.profile.get_avatar(size)