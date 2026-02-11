import sys
if sys.version_info < (3,6,5):
    sys.stderr.write('You need python 3.6.5 or later to run this script\n')
    sys.exit(1)

from thrusday.settings import APP_TITLE, DEBUG, LOG_FORMAT, RELEASE
from platform import platform, python_version

print(f'''
    __
 __/  \ {APP_TITLE}.API
/  \__/ {RELEASE[:8]}
\__/  \ Whale bytes (c) 2026
   \__/ {platform()} Python v{python_version()}
''')

from importlib import reload
reload(sys)

import warnings
from gevent import monkey
from logging import basicConfig, getLogger, CRITICAL

warnings.filterwarnings('ignore')
monkey.patch_all()

basicConfig(level=10 if DEBUG else 30, format=LOG_FORMAT)
log = getLogger(APP_TITLE)
log.setLevel(10 if DEBUG else 30)

from thrusday.migration import  initialize
log.info('Executing migration scripts..')
initialize()

from api import app
log.info('Application loaded')
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    ADMIN_PORT = 5031
    run_simple('0.0.0.0', ADMIN_PORT, app, use_reloader=True, use_debugger=True)
