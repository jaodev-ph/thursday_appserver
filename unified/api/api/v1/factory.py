API_VERSION = '1.0'
import json
import redis
import requests
import logging
from datetime import datetime
from bson import ObjectId
from flask import Flask, request
# from flask_cors import CORS, cross_origin
from flasgger import Swagger, APISpec
from common.jsonify import jsonify
from thrusday.settings import DEFAULT_TIMEZONE, SECURITY_NONCE_LIFETIME, SOCKETIO_REDIS_HOST, SOCKETIO_REDIS_CHANNEL, S3_BUCKET, DB_CONFIG, REDIS_PASSWORD, SESSIONS_CONFIG, \
    SESSION_LIFETIME
from api.v1.ext import api_route_config, socketio
from flask_socketio import SocketIO, rooms, join_room, leave_room
from werkzeug.routing import BaseConverter, ValidationError

from common.time_utils import utcnow

from thrusday.mongodb_session_interface import MongoSessionInterface

log = logging.getLogger('api.factory')

redis_client = redis.Redis(
    host=SOCKETIO_REDIS_HOST,
    port=6379,
    password=REDIS_PASSWORD,
    decode_responses=True
)


def before_request():
    request.version = API_VERSION
    if request.endpoint in ('flasgger.apispec_1', 'flasgger.apidocs', 'flasgger.static', 'static'):
        return

def create_app(package_name):
    app = Flask(package_name, instance_relative_config=True)
    app.before_request(before_request)
    log.debug('Creating API %s', package_name)
    app.url_map.converters['objectid'] = ObjectIDConverter
    app.config['SWAGGER'] = {'uiversion': 3 }
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['PROPAGATE_EXCEPTIONS'] = False
    app.config['SESSION_COOKIE_NAME'] = f'thursday.{package_name}'
    app.permanent_session_lifetime = SESSION_LIFETIME
    app.session_interface = MongoSessionInterface(config=SESSIONS_CONFIG, app=app)
    log.debug('Creating API 234234%s', package_name)
    initialize_socketio(app)
    initialize_swagger(app)
    app.register_error_handler(403, errorhandler)
    app.register_error_handler(404, errorhandler)
    app.register_error_handler(412, errorhandler)
    app.register_error_handler(500, errorhandler)
    app.register_error_handler(429, ratelimit_handler)
    return app

# def initialize_limiter(app):
#     # limiter = Limiter(app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
#     limiter = Limiter(app, key_func=get_remote_address)
#     limiter.init_app(app)
#     return limiter

def errorhandler(e):
    message = 'Resource not found'
    if hasattr(e, 'data'):
        message = e.data.get('message', message)
    return jsonify({'message': message}), e.code

def errorhandler(e):
    message = 'Resource not found'
    if hasattr(e, 'data'):
        message = e.data.get('message', message)
    return jsonify({'message': message}), e.code

def ratelimit_handler(e):
    return jsonify({'message': "You have exceeded the maximum resend limit for today. Please try again tomorrow"}), e.code


def initialize_socketio(app):
    # https://flask-socketio.readthedocs.io/en/latest/
    socketio = SocketIO(app, cors_allowed_origins='*')
    broker_url = f'redis://:{REDIS_PASSWORD}@{SOCKETIO_REDIS_HOST}:6379/{SOCKETIO_REDIS_CHANNEL}'
    socketio.init_app(app, message_queue=broker_url, path='s.io', always_connect=True, logger=True, engineio_logger=True)
    app.socketio = socketio
       
    @socketio.on('join')
    def socketio_join_room(room):
        join_room(room)

    @socketio.on('leave')
    def socketio_leave_room(room):
        leave_room(room)

    @socketio.on('leave_all')
    def socketio_leave_all():
        for room in rooms():
            leave_room(room)

    @socketio.on('connect')
    def socketio_connect(*args, **kwargs):
        log.info('Client is connected! : %s', request.sid)
        return True

    @socketio.on('disconnect')
    def handle_disconnect():
        # Perform any necessary cleanup here
        pass

    @socketio.on_error_default
    def error_handler(e):
        log.error('[ERROR] SocketIO: ' + str(e))

class ObjectIDConverter(BaseConverter):
    def __init__(self, url_map):
        super(ObjectIDConverter, self).__init__(url_map)
        # self.regex = '^[a-f\d]{24}$'
    def to_python(self, value):
        try:
            return ObjectId(value)
        except (InvalidId, ValueError, TypeError):
            raise ValidationError()
    def to_url(self, value):
        return str(value)

def initialize_swagger(app):
    log.info('swagger initialiaze')
    swagger_config = Swagger.DEFAULT_CONFIG.copy()
    swagger_config['specs'][0]['route'] = '/api/apispec_1.json'
    swagger_config['specs'][0]['static_url_path'] = '/api/static'
    log.info('swagger_config: %s', swagger_config)

    Swagger(app,
        config=swagger_config,
        template = {
            "info": {
                "title": "Thrusday API",
                "description": "The API is based on REST (Representational State Transfer) principles, invoked via normal HTTP requests, which enables any web development language to easily use the API.",
                "contact": {
                    "email": "josephjaojoco@gmail.com",
                    "url": "http://www.entropysolution.com",
                },
                "version": "3.0"
            },
            # for openapi 2.0
            # "basePath": "/api",
            'securityDefinitions': {
                'ApiKeyAuth': {
                    'in': 'header',
                    'name': 'X-APIKey',
                    'type': 'apiKey'
                },
                'JWT': {
                    'in': 'header',
                    'name': 'Authorization',
                    'type': 'apiKey'
                },
                'X-Auth': {
                    'in': 'header',
                    'name': 'X-Auth',
                    'type': 'apiKey'
                },
                'X-Timestamp': {
                    'in': 'header',
                    'name': 'X-Timestamp',
                    'type': 'apiKey'
                },
            },
            # for openapi 3.0.2
            # "servers": [
            #     {
            #         "url": "/api",
            #         "description": "Default"
            #     },
            # ],
            # "security": [{"ApiKeyAuth": [], "Bearer": []}]
        }
    )