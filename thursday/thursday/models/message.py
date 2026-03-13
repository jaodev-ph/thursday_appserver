import pytz
from logging import getLogger
from datetime import datetime
from common.jsonify import json_decode, json_encode
from common.dict_tools import merge_dicts
from common.time_utils import convert_date_to_str

from . import HOST, DATABASE, USERNAME, PASSWORD, REPLICASET, Model, Index, fields, ObjectId, merge_dicts, validate, process_query, APPSERVER_NAME

from thursday.settings import DEFAULT_TIMEZONE
log = getLogger(f"{APPSERVER_NAME}.models.tenant")


class Message(Model):  
    TEMPLATE = {
        'tenant_id': None,
        'conversation_id': None,
        'channel_id': None,
        'customer_id': None,
        'status': '',
        'token_usage': '',
        'token_usage': {
            'type': '', # input/output
            'value': ''
        }
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
        collection = 'conversations'
        host = HOST
        database = DATABASE
        username = USERNAME
        password = PASSWORD
        indices = (
            Index('name', unique=True),
        )
        replicaset = REPLICASET