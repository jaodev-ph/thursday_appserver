import pytz
from logging import getLogger
from datetime import datetime
from common.jsonify import json_decode, json_encode
from common.dict_tools import merge_dicts
from common.time_utils import convert_date_to_str

from . import HOST, DATABASE, USERNAME, PASSWORD, REPLICASET, Model, Index, fields, ObjectId, merge_dicts, validate, process_query, APPSERVER_NAME

from thursday.settings import DEFAULT_TIMEZONE
log = getLogger(f"{APPSERVER_NAME}.models.tenant")


class User(Model):  
    TEMPLATE = {
        'tenant_id': None
        'name': '',
        'username': '',
        'password': None,
        'contact_number': '',
        'email_address': '',
        'address': '',
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
        collection = 'users'
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
        fields, limit, start, sort, query_text = process_query(query, columns)
        log.info('filters: %s', required_filters)
        total_records = cls.collection.count_documents(required_filters)
        result = cls.collection.find(required_filters, fields)
        records = list(result.sort(sort).skip(start).limit(limit))
        return records, total_records, result.count()

    @classmethod
    def create(cls, args):
        is_invalid = validate(args, cls.validation)
        if is_invalid:
            raise is_invalid

        # SECTION: Check existing
        instance = cls.collection.find_one({'username': args['username']})
        if instance is not None:
            raise ValueError('Username %s already exists' % (args['username']))
        # END

        instance = cls(args).save()
        return instance


    def update(self, args):
        validate(args, self.validation, partial=True)
        self.hash_password(args)
        args.pop('_id', '')
        merge_dicts(self, args, True)
        self.save()
    
    @classmethod
    def getDocument(cls, filters):
        if isinstance(filters, ObjectId):
            filters = {'_id': filters}
        log.info('getting documents1')
        return cls.collection.find_one(filters)

    @classmethod
    def getDocuments(cls, filters=None, projection=None, sort_by=None):
        output = cls.collection.find(filters, projection)
        log.info('getting documents')
        if sort_by:
            output.sort(sort_by, 1)
        return output