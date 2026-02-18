import logging
from flask_restful import Api, abort
from flask import Flask, request, session
from thursday.settings import DEFAULT_TIMEZONE, SECURITY_NONCE_LIFETIME, SOCKETIO_REDIS_HOST, SOCKETIO_REDIS_CHANNEL, S3_BUCKET, DB_CONFIG, REDIS_PASSWORD
from hashlib import sha256
from api.v1.ext import add_api_url_rules, jsonify, abort
from api.v1.factory import create_app
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO

log = logging.getLogger('thursday.api.v1.0')
app = create_app(__name__)


from api.v1.chat import ChatPostView

add_api_url_rules(app, [
   ('/chat', ChatPostView, 'POST')
])

from api.v1.embedding import EmbeddingPostView

add_api_url_rules(app, [
   ('/embeddings', EmbeddingPostView, 'POST')
])

