import pytz
from logging import getLogger
from datetime import datetime
from common.jsonify import json_decode, json_encode
from common.dict_tools import merge_dicts
from common.time_utils import convert_date_to_str
from bson import ObjectId

from . import HOST, DATABASE, USERNAME, PASSWORD, REPLICASET, Model, Index, fields, ObjectId, merge_dicts, validate, process_query, APPSERVER_NAME

from thursday.settings import DEFAULT_TIMEZONE
log = getLogger(f"{APPSERVER_NAME}.models.tenant")


class User(Model):  
    TEMPLATE = {
        'tenant_id': None,
        'type': ""
    }

     validation = {
        'field_types': [  # you can skip fields with type of 'string'
            ('tenant_id', ObjectId),
        ],
        'required': ['tenant_id', 'type'],
        'minlength': [
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