APP_TITLE = __name__

from thursday.settings import DEBUG, LOG_FORMAT
from common.decorators import route, validate_form, cast_form
from common.fixed_datetime import datetime as fdatetime, timezone
from common.jsonify import jsonify
from common.dict_tools import merge_dicts

from bson import ObjectId
from logging.config import dictConfig as loggingDictConfig
from logging import getLogger, INFO as LOG_INFO, WARNING as LOG_WARNING, DEBUG as LOG_DEBUG, CRITICAL as LOG_CRITICAL
from flask import Blueprint, render_template, redirect, url_for, session, request, abort, flash, make_response

loggingDictConfig({
    'version': 1,
    'formatters': {'default': {'format': LOG_FORMAT,
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG' if DEBUG else 'INFO',
        'handlers': ['wsgi']
    }
})
# getLogger('matplotlib').setLevel(LOG_CRITICAL)
# getLogger('socketio').setLevel(LOG_CRITICAL)
# getLogger('engineio').setLevel(LOG_CRITICAL)
# getLogger('geventwebsocket.handler').setLevel(LOG_CRITICAL)
# getLogger('apscheduler').setLevel(LOG_CRITICAL)
