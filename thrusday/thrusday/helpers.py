import re
from bson import ObjectId
from bson.errors import InvalidId
import random
import string
from common.time_utils import utcepoch, convert_str_to_date, convert_date_to_str
from logging import getLogger
from datetime import datetime
import pytz
from common.jsonify import jsonify
from thrusday.settings import DATETIME_FORMAT, DEFAULT_TIMEZONE
from flask import request, abort as original_flask_abort, make_response


log = getLogger('thrusday.helpers')

gsettings = {
    'DATETIME_FORMAT': DATETIME_FORMAT,
    'DEFAULT_TIMEZONE': DEFAULT_TIMEZONE
}

# def jsonify(*args, **kwargs):
#     return _jsonify(*args, **kwargs)

def abort(http_status_code, **kwargs):
    try:
        original_flask_abort(make_response(jsonify(kwargs), http_status_code))
    except Exception as ex:
        ex.data = kwargs
        raise
    except HTTPException as e:
        if len(kwargs):
            e.data = kwargs
        raise


def parse_error_spiel(messages:tuple, html:bool=True) -> str:
    error_dict = messages[0]
    spiels = []
    for key, message in error_dict.items():
        spiels.append(f"{key.capitalize()}: {' '.join(message)}")
    return f"{'<br/>' if html else ' '}".join(spiels)
    
def format_timestamp(timestamp):
    if timestamp is None:
        return 'n/a'
    return convert_date_to_str(timestamp, DATETIME_FORMAT, pytz.timezone(DEFAULT_TIMEZONE))


def parse_duplicate_key_error(error_message):
    # Regular expression to extract the duplicated key field and value
    match = re.search(r'dup key: { (.*?): "(.*)" }', error_message)
    if match:
        field_name, value = match.groups()
        return f'{field_name.capitalize()}: {value} is already exist!'
    return ''

def generate_random_string(length=8):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def generate_password(length=8):
    """Generates a random password of the specified length."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(characters, k=length))


def parse_filters(filters, unix=True):
    log.info('filters: %s', filters)
    tmp = {}
    for key, value in filters.items():
        if key in ['startDate', 'endDate'] or value in ['', None]:
            continue
        tmp[key] = ObjectId(value) if ObjectId.is_valid(value) else value
        if isinstance(value, list):
            included_keys = ['user_ids']
            if key in included_keys:
                tmp[key] = {'$in': [ ObjectId(x) if ObjectId.is_valid(x) else x for x in value]}
            continue
    #parsing dates
    startDate = filters.get('startDate', None)
    endDate = filters.get('endDate', None)
    if startDate not in ['', None] :
        log.info('DATETIME_FORMAT: %s', DATETIME_FORMAT)
        if unix:
            tmp[filters.get('dateRangeField', 'created_datetime')] = { '$gte': startDate, '$lte': endDate}
        else:
            tmp[filters.get('dateRangeField', 'created_datetime')] = { '$gte': convert_str_to_date(startDate, DATETIME_FORMAT), '$lte': convert_str_to_date(endDate, DATETIME_FORMAT)}
        if 'dateRangeField' in filters:
            tmp.pop('dateRangeField')
    log.info('new_filters: %s', tmp)
    return tmp

def unix_to_datetime(unix_ts, tz=None):
    """
    Convert a Unix timestamp to a timezone-aware datetime object.
    
    :param unix_ts: int or float, Unix timestamp in seconds
    :param tz: pytz timezone object (default UTC)
    :return: datetime.datetime (timezone-aware)
    """
    if tz is None:
        tz = pytz.UTC

    dt = datetime.fromtimestamp(unix_ts, tz=pytz.UTC)  # UTC aware
    return dt.astimezone(tz)  # convert to desired timezone
