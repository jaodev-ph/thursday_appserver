import copy
from . import HOST, DATABASE, USERNAME, PASSWORD, REPLICASET, Model, Index, ObjectId, validate, process_query, APPSERVER_NAME
from common.dict_tools import merge_dicts
from logging import getLogger

log = getLogger(f"{APPSERVER_NAME}.models.acl_profile")


class AclProfile(Model):
    TEMPLATE = {
        'tenant_id': None,
        'name': '',
        'access_control': {},
        'active': True,
    }

    validation = {
        'field_types': [
        ],
        'required': ['tenant_id', 'name'],
        'minlength': [
            ('name', 3),
        ]
    }

    class Meta:
        collection = 'acl_profiles'
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
        total_records = cls.collection.count_documents(required_filters)
        result = cls.collection.find(required_filters, fields)
        records = list(result.sort(sort).skip(start).limit(limit))
        return records, total_records, result.count()

    @classmethod
    def create(cls, args):
        validate(args, cls.validation)
        args = merge_dicts(copy.deepcopy(cls.TEMPLATE), args, True)
        record = cls(args).save()
        return record

    def update(self, args):
        validate(args, self.validation, partial=True)
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