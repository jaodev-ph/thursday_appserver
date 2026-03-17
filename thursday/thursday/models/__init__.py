from logging import getLogger
from bson import ObjectId
from pymongo import MongoClient
from thursday.settings import DB_CONFIG
from common.crypto import make_hash
from common.dict_tools import merge_dicts, merge_in_place, merge_recursion
from thursday.micromongo4 import Model, Index, fields, validate


APPSERVER_NAME = 'thursday'
HOST = DB_CONFIG[APPSERVER_NAME]['location']
DATABASE = DB_CONFIG[APPSERVER_NAME]['name']
USERNAME = DB_CONFIG[APPSERVER_NAME]['username']
PASSWORD = DB_CONFIG[APPSERVER_NAME]['password']
REPLICASET = DB_CONFIG[APPSERVER_NAME].get('replicaset', APPSERVER_NAME)

log = getLogger('thursday.models')

def initialize():
    pass

def process_query(query, columns):
    if len(columns) > 0:
        fields = {att: True for att in columns if att != ''}
        if '_id' not in fields:
            fields['_id'] = True
    else:
        fields = None
    limit = int(query.get('length', 0))
    limit = 1 if limit < 0 else limit
    start = int(query.get('start', 0))
    if 'search' in query:
        query_text = query.get('search', '')
    else:
        query_text = query.get('search[value]', '') or query.get('searchValue', '')
    if 'sortOrder' in query:
        sort_order = int(query.get('sortOrder'))
    else:
        sort_order = 1 if not query.get('sortDesc', False) else -1
    sort = [(query.get('sortBy', '_id'), sort_order)]
    return fields, limit, start, sort, query_text



def validate(args, validation, partial=False):
    """
    Basic validation helper.

    - partial=False (default): enforce required fields
    - partial=True: validate only fields present in args (skip required checks)
    """
    if not partial:
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


def cast_field(args, field_name, field_type):
    field_value = args.get(field_name)

    if field_value is None and field_type is not bool:
        return field_value
    # if isinstance(args, ImmutableMultiDict):
    #     args = MultiDict(args)

    try:
        if field_type is bool:
            args[field_name] = False if field_value in (None, '0', 'false') else True
        elif field_type is str:
            # field_value = args[field_name]
            field_value = field_type(field_value).strip()
            field_value = normalize('NFKD', field_value)
            args[field_name] = field_value
        else:
            args[field_name] = field_type(field_value)
    except Exception as ex:
        # If unable to cast, set to None
        if field_value != '':
            print('[Exception]', ex)
            raise ValueError('Invalid value "%s" for field "%s" (%s)' % (field_value, field_name, field_type))
        args[field_name] = None

    if field_type is str and len(args[field_name]) == 0:
        args[field_name] = None

    parse_multi_dict_field(args, field_name, args[field_name])


def parse_multi_dict_field(args, field_name, field_value):
    if '[' in field_name:
        current_dict = args
        dict_items = []
        for item in field_name.split('['):
            ditem = item.replace(']', '')
            if ditem not in current_dict:
                current_dict[ditem] = {}
            current_dict = current_dict[ditem]
            dict_items.append(ditem)
        args.pop(field_name)
        d = DynamicAccessNestedDict(args)
        d.setval(dict_items, field_value)