from logging import getLogger
from thursday.settings import APP_TITLE
log = getLogger(f"{APP_TITLE}.migration")
from thursday.models.admin import Admin

def initialize():
    log.info('Executing migration scripts..')
    # Admin account creation
    try:
        admin_args = {
            'username': 'admin',
            'password': 'admin',
            'email': 'admin@example.com',
            'name': 'Admin',
            'role': 'admin',
            'status': 'active',
        }
        record = Admin.create(admin_args)
        log.info(f'Admin account created: {record}')
    except Exception as e:
        log.error(f'Admin is already created: {e}')