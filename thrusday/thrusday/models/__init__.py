from logging import getLogger
from bson import ObjectId
from pymongo import MongoClient
from thrusday.settings import DB_CONFIG
from common.crypto import make_hash
from common.dict_tools import merge_dicts, merge_in_place, merge_recursion
from micromongo4 import Model, Index, fields, validate

from thrusday.references import categories, accounts

APPSERVER_NAME = 'thrusday'
HOST = DB_CONFIG[APPSERVER_NAME]['location']
DATABASE = DB_CONFIG[APPSERVER_NAME]['name']
USERNAME = DB_CONFIG[APPSERVER_NAME]['username']
PASSWORD = DB_CONFIG[APPSERVER_NAME]['password']
REPLICASET = DB_CONFIG[APPSERVER_NAME].get('replicaset', APPSERVER_NAME)

log = getLogger('thrusday.models')

def initialize():
    pass
    # print("model.initialization")
    # categories = ['Savings', 'Food', 'Social Life', 'Pets', 'Transport', 'Household', 'Health', 'Education', 'Gift', 'Donation']
    # try:
    #     from thrusday.models.category import Category
    #     for category in categories:
    #         category = Category({
    #             'parent_id': None,
    #             'name': category,
    #             'default': True
    #         }).save()
    # except Exception as ex:
    #     log.info('default category is already exist!')




    
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