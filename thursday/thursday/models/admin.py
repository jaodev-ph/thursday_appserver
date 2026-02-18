# SECTION: Default Imports
from . import HOST, DATABASE, USERNAME, PASSWORD, REPLICASET, Model, Index, ObjectId, validate, process_query, APPSERVER_NAME
import random
from common.dict_tools import merge_dicts
from common.generators import generate_random_password
from common.crypto import check_hash, make_hash
from common.time_utils import utcnow
from logging import getLogger

from thursday.settings import PERSONNEL_CONFIG
# END

log = getLogger(f"{APPSERVER_NAME}.models.admin")


class Admin(Model):

    class Meta:
        collection = 'admins'

        host = HOST
        database = DATABASE
        username = USERNAME
        password = PASSWORD

        indices = (
            Index('username'),
        )
        replicaset = REPLICASET

    validation = {
        'required': ['username', 'name']
    }


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
        validate(args, self.validation)
        self.hash_password(args)
        args.pop('_id', '')
        merge_dicts(self, args, True)
        self.save()


    @classmethod
    def getDocument(cls, filters):
        if isinstance(filters, ObjectId):
            filters = {'_id': filters}
        return cls.collection.find_one(filters)


    @classmethod
    def getDocuments(cls, filters=None, projection=None, sort_by=None):
        output = cls.collection.find(filters, projection)
        if sort_by:
            output.sort(sort_by, 1)
        return output



    def update_password(self, new_password=None):
        if new_password is None:
            new_password = generate_random_password()
        self.password = make_hash(new_password)
        self.password_tmp = False
        self.save()
        return new_password


    @staticmethod
    def hash_password(args):
        if 'password' in args:
            if args['password'] in ['', None]:
                del args['password']
            else:
                args['password'] = make_hash(args['password'])


    def check_hash(self, input_password):
        return check_hash(input_password, self.password)