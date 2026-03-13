from os import path, environ
from sys import exit
from yaml import safe_load
from socket import gethostname
from copy import deepcopy, copy
from common.dict_tools import merge_dicts

CACHE_REDIS_HOST = CACHE_REDIS_CHANNEL = REDIS_PASSWORD = None

def load_settings():
    # Default configuration
    defaults = {}
    with open(path.join(path.dirname(path.abspath(__file__)), 'default_settings.yaml'), 'r') as stream:
        try:
            defaults = safe_load(stream)
        except Exception as ex:
            print(f'Configuration file parsing error: {ex}')
            exit()
    # Configuration file
    settings = {}
    for settings_override in ['settings.yaml', '/settings.yaml']:
        if path.isfile(settings_override):
            with open(settings_override, 'r') as stream:
                try:
                    settings = safe_load(stream)
                    print(f'Loaded override config file from {settings_override}: {settings}')
                except Exception as ex:
                    print(f'Configuration file parsing error: {ex}')
            break
    if settings == {}:
        print('settings.yaml file not found! Using defaults!')
    return merge_dicts(defaults, settings or {})

settings = load_settings()
settings = dict([(k.upper(), v) for k, v in settings.items()])

for k in settings.keys():
	override = environ.get(k)
	if override:
		# BUG: Cannot set a setting to None
		print(f'Enviro settings override detected - {k}:{override}')
		settings[k] = override

HOSTNAME = gethostname()
locals().update(settings)

from common.caching import oredis
oredis.setup(CACHE_REDIS_HOST, CACHE_REDIS_CHANNEL, REDIS_PASSWORD)