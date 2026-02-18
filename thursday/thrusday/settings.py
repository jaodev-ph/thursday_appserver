import yaml
import logging
from sys import exit
from os import path, environ
from socket import gethostname
from copy import deepcopy, copy
from common.dict_tools import merge_dicts, merge_recursion

CACHE_REDIS_HOST = CACHE_REDIS_CHANNEL = REDIS_PASSWORD = None

def load_settings():
	# Default configuration
	defaults = {}
	with open(path.join(path.dirname(path.abspath(__file__)), 'default_settings.yaml'), 'r') as stream:
		try:
			defaults = yaml.load(stream, Loader=yaml.FullLoader)
		except Exception as ex:
			print(f'Configuration file parsing error: {ex}')
			exit()

	# Configuration file
	settings = {}
	if path.isfile('settings.yaml'):
		with open('settings.yaml', 'r') as stream:
			try:
				settings = yaml.load(stream, Loader=yaml.FullLoader)
			except Exception as ex:
				print(f'Configuration file parsing error: {ex}')
	else:
		print('settings.yaml file not found! Using defaults!')
	return merge_dicts(defaults, settings or {})

settings = load_settings()
settings = dict([(k.upper(), v) for k, v in settings.items()])

for k in settings.keys():
	override = environ.get(k)
	if override:
		# BUG: Cannot set a setting to None
		print('Settings override detected - {}:{}'.format(k, override))
		settings[k] = override

HOSTNAME = gethostname()
locals().update(settings)

from common.caching import oredis
oredis.setup(CACHE_REDIS_HOST, CACHE_REDIS_CHANNEL, REDIS_PASSWORD)