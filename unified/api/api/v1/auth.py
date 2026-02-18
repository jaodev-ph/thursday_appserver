mport logging
import jwt
import calendar
import time
from flask import request
from datetime import datetime
from bson.objectid import ObjectId

from functools import wraps
from thursday.settings import SECRET_TOKEN, SECURITY_NONCE_LIFETIME
from flask import request, make_response, current_app as app
from common.jsonify import jsonify

def requires_token(f):
    """Decorator to require JWT for your SPA endpoint."""
    @wraps(f)
    def decorated(*args, **kwargs):
        pass
            # token = request.headers.get('Authorization', None) or request.args.get('token', None)
            # cookie = request.cookies.get(app.session_cookie_name)
            # # log.info('token: %s', token)
            # log.info('request_cookie: %s', request.cookies.get(app.session_cookie_name))
            # if token in ["null", None, '']:
            #     abort(401, message='Invalid token')
            # try:
            #     db_session = AdminSession.getSession({'sid': cookie})
            #     if not db_session:
            #          abort(419, message='Session Expired')
            #     if OVERRIDE_KEYS and token is None:
            #         web_user = AdminModel.getAdmin({})
            #         web_user['personnel'] = False
            #         web_user['path'] = '' #get_avatar_path(web_user)
            #         web_user['access_control'] = web_user.get('access_control', get_admin_acl())
            #         request.user_id = web_user._id
            #         request.web_user = web_user
            #         return f(*args, **kwargs)
            #     else:
            #         if token is None:
            #             log.warning('Token required')
            #             abort(401, message='Token required')
            #         payload = jwt.decode(token, SECRET_TOKEN, algorithms=['HS256'])
            #         username = payload.get('user').get('username')
            #         # Admin/Personnel User recognition
            #         admin = AdminModel.getAdmin({'username': username})
            #         personnel = PersonnelModel.getPersonnel({'username': username})
            #         if personnel:
            #             personnel.tagAccess(request.endpoint)
            #     web_user =  admin or personnel
            #     if web_user is None:
            #         log.warning('Authorization: User %s not found.', username)
            #         abort(401, message='User not found')
            #     web_user['access_control'] = web_user.get('access_control', {})
            #     request.user_id = web_user._id
            #     request.web_user = web_user
            # except jwt.ExpiredSignatureError:
            #     log.warning('Expired token')
            #     abort(401, message='Expired token')
            # except jwt.InvalidTokenError as e:
            #     log.warning('Invalid token: %s', str(e))
            #     abort(401, message='Invalid token')
            # return f(*args, **kwargs)
    return decorated