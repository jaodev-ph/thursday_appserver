from logging import getLogger
from bson import ObjectId
from pymongo import MongoClient
from thursday.settings import DB_CONFIG
from common.crypto import make_hash
from common.dict_tools import merge_dicts, merge_in_place, merge_recursion
from micromongo4 import Model, Index, fields, validate

from thursday.references import categories, accounts

APPSERVER_NAME = 'thursday'
HOST = DB_CONFIG[APPSERVER_NAME]['location']
DATABASE = DB_CONFIG[APPSERVER_NAME]['name']
USERNAME = DB_CONFIG[APPSERVER_NAME]['username']
PASSWORD = DB_CONFIG[APPSERVER_NAME]['password']
REPLICASET = DB_CONFIG[APPSERVER_NAME].get('replicaset', APPSERVER_NAME)

log = getLogger('thursday.models')

def initialize():
    pass

    
def process_query(query):
    limit = int(query.get('length', 0))
    limit = 0 if limit < 0 else limit
    start = int(query.get('start', 0))
    query_text = query.get('search[value]', query.get('search', ""))
    sort = []
    for order in query.get('order', []):
        if order.get('name') not in ['', None]:
            sort.append((order.get('name'), 1 if order.get('dir') == 'asc' else -1))
    if len(sort) == 0:
        sort = [('created_datetime', -1)]
    return limit, start, sort, query_text



def validate(args, validation):
    for att in validation.get('required', []):
        if args.get(att) == None or args.get(att) == '':
            raise ValueError('%s field is required' % (att.title().replace('_', ' ')))

    for v in validation.get('minlength', []):
        if args.get(v[0]) == None or args.get(v[0]) == '':
            continue
        if v[0] in args and len(args[v[0]]) < v[1]:
            raise ValueError('%s must be at least %s characters.' % (v[0].title(), v[1]))

    for v in validation.get('maxlength', []):
        if args.get(v[0]) == None or args.get(v[0]) == '':
            continue
        if v[0] in args and len(args[v[0]]) > v[1]:
            raise ValueError('%s must not exceed %s characters.' % (v[0].title(), v[1]))

    for v in validation.get('field_types', []):
        cast_field(args, v[0], v[1])

    return None