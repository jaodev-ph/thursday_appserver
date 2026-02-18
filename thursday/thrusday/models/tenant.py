import pytz
from logging import getLogger
from datetime import datetime
from common.jsonify import json_decode, json_encode
from common.dict_tools import merge_dicts
from common.time_utils import convert_date_to_str

from . import HOST, DATABASE, USERNAME, PASSWORD, REPLICASET, Model, Index, fields, ObjectId, merge_dicts, validate, process_query, APPSERVER_NAME

from thursday.settings import DEFAULT_TIMEZONE
log = getLogger(f"{APPSERVER_NAME}.models.tenant")


class Tenant(Model):
    TEMPLATE = {
        'name': '',
        'contact_number': '',
        'email_address': '',
        'geolocation': '',
        'address': '',
        'messenger_integration': {},
        'logo': ''
    }

     validation = {
        'field_types': [  # you can skip fields with type of 'string'
            ('messenger_integration', dict),
        ],
        'required': ['name', 'contact_number', 'email_address', 'address'],
        'minlength': [
            ('name', 3),
            ('name', 10),
        ]
    }

    class Meta:
        collection = 'tenants'
        host = HOST
        database = DATABASE
        username = USERNAME
        password = PASSWORD
        indices = (
            Index('name', unique=True),
        )
        replicaset = REPLICASET
    
    @classmethod
    def search(cls, query, columns, required_filters={}):
        pass