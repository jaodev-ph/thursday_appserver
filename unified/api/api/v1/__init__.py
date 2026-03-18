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

from api.v1.embedding import EmbeddingPostView, EmbeddingDeleteView

add_api_url_rules(app, [
   ('/embeddings', EmbeddingPostView, 'POST'),
   ('/embeddings/<string:collection_name>', EmbeddingDeleteView, 'DELETE')
])


from api.v1.tenants import TenantPostView, TenantGetView, TenantPutView, TenantDeleteView, TenantPostInquiryViewSchema
add_api_url_rules(app, [
   ('/tenants/<objectid:_id>', TenantGetView, 'GET'),
   ('/tenants', TenantPostView, 'POST'),
   ('/tenants/inquiry', TenantPostInquiryViewSchema, 'POST'),
   ('/tenants/<objectid:_id>', TenantPutView, 'PUT'),
   ('/tenants/<objectid:_id>', TenantDeleteView, 'DELETE'), # delete tenant by id
])

from api.v1.billings import BillingPostView, BillingGetView, BillingPutView, BillingDeleteView, BillingPostInquiryView
add_api_url_rules(app, [
   ('/billings/<objectid:_id>', BillingGetView, 'GET'),
   ('/billings', BillingPostView, 'POST'),
   ('/billings/inquiry', BillingPostInquiryView, 'POST'),
   ('/billings/<objectid:_id>', BillingPutView, 'PUT'),
   ('/billings/<objectid:_id>', BillingDeleteView, 'DELETE'),
])

from api.v1.customers import CustomerPostView, CustomerGetView, CustomerPutView, CustomerDeleteView, CustomerPostInquiryView
add_api_url_rules(app, [
   ('/customers/<objectid:_id>', CustomerGetView, 'GET'),
   ('/customers', CustomerPostView, 'POST'),
   ('/customers/inquiry', CustomerPostInquiryView, 'POST'),
   ('/customers/<objectid:_id>', CustomerPutView, 'PUT'),
   ('/customers/<objectid:_id>', CustomerDeleteView, 'DELETE'),
])

from api.v1.bots import BotPostView, BotGetView, BotPutView, BotDeleteView, BotPostInquiryView
add_api_url_rules(app, [
   ('/bots/<objectid:_id>', BotGetView, 'GET'),
   ('/bots', BotPostView, 'POST'),
   ('/bots/inquiry', BotPostInquiryView, 'POST'),
   ('/bots/<objectid:_id>', BotPutView, 'PUT'),
   ('/bots/<objectid:_id>', BotDeleteView, 'DELETE'),
])

from api.v1.conversations import ConversationPostView, ConversationGetView, ConversationPutView, ConversationDeleteView, ConversationPostInquiryView
add_api_url_rules(app, [
   ('/conversations/<objectid:_id>', ConversationGetView, 'GET'),
   ('/conversations', ConversationPostView, 'POST'),
   ('/conversations/inquiry', ConversationPostInquiryView, 'POST'),
   ('/conversations/<objectid:_id>', ConversationPutView, 'PUT'),
   ('/conversations/<objectid:_id>', ConversationDeleteView, 'DELETE'),
])

from api.v1.messages import MessagePostView, MessageGetView, MessagePutView, MessageDeleteView, MessagePostInquiryView
add_api_url_rules(app, [
   ('/messages/<objectid:_id>', MessageGetView, 'GET'),
   ('/messages', MessagePostView, 'POST'),
   ('/messages/inquiry', MessagePostInquiryView, 'POST'),
   ('/messages/<objectid:_id>', MessagePutView, 'PUT'),
   ('/messages/<objectid:_id>', MessageDeleteView, 'DELETE'),
])

from api.v1.users import UserPostView, UserGetView, UserPutView, UserDeleteView, UserPostInquiryView
add_api_url_rules(app, [
   ('/users/<objectid:_id>', UserGetView, 'GET'),
   ('/users', UserPostView, 'POST'),
   ('/users/inquiry', UserPostInquiryView, 'POST'),
   ('/users/<objectid:_id>', UserPutView, 'PUT'),
   ('/users/<objectid:_id>', UserDeleteView, 'DELETE'),
])

from api.v1.acl_profiles import AclProfilePostView, AclProfileGetView, AclProfilePutView, AclProfileDeleteView, AclProfilePostInquiryView
add_api_url_rules(app, [
   ('/acl_profiles/<objectid:_id>', AclProfileGetView, 'GET'),
   ('/acl_profiles', AclProfilePostView, 'POST'),
   ('/acl_profiles/inquiry', AclProfilePostInquiryView, 'POST'),
   ('/acl_profiles/<objectid:_id>', AclProfilePutView, 'PUT'),
   ('/acl_profiles/<objectid:_id>', AclProfileDeleteView, 'DELETE'),
])