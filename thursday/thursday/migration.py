from logging import getLogger
from thursday.settings import APP_TITLE
log = getLogger(f"{APP_TITLE}.migration")
from thursday.models.admin import Admin
from common.crypto import check_hash, make_hash
from thursday.acl import get_admin_acl

def initialize():
    log.info('Executing migration scripts..')
    # Admin account creation
    try:
        admin_args = {
            'username': 'admin',
            'password': make_hash('admin'),
            'email': 'admin@example.com',
            'name': 'Admin',
            'access_control': get_admin_acl(),
            'active': True
        }
        record = Admin.create(admin_args)
        log.info(f'Admin account created: {record}')
    except Exception as e:
        log.error(f'Admin is already created: {e}')