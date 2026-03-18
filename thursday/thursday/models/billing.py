# for determining the plan

from . import HOST, DATABASE, USERNAME, PASSWORD, REPLICASET, Model, Index, ObjectId, validate, process_query, APPSERVER_NAME
from common.dict_tools import merge_dicts
import copy
from logging import getLogger

log = getLogger(f"{APPSERVER_NAME}.models.billing")

class Billing(Model):
    TEMPLATE = {
        'tenant_id': None,
        'plan': None,
        'start_date': None,
        'end_date': None,
        'status': None, # BILLING_STATUS
    }

    validation = {
        'required': ['tenant_id', 'plan', 'start_date', 'end_date', 'status']
    }

    class Meta:
        collection = 'billings'
        host = HOST
        database = DATABASE
        username = USERNAME
        password = PASSWORD
        indices = ()
        replicaset = REPLICASET

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
        log.info('getting a billing document')
        return cls.collection.find_one(filters)

    @classmethod
    def getDocuments(cls, filters=None, projection=None, sort_by=None):
        output = cls.collection.find(filters, projection)
        log.info('getting billing documents')
        if sort_by:
            output.sort(sort_by, 1)
        return output
