from logging import getLogger
from bson.objectid import ObjectId
from flask import request
from flasgger import fields
from marshmallow import EXCLUDE

from common.jsonify import jsonify

from api.v1.ext import (
    abort,
    ExtSchema,
    DefaultResponsesWith,
    PostSuccessSchema,
    PostErrorSchema,
    ExtSwaggerView,
    DatatableViewSchemaResponseSchema,
    DatatableViewSchema,
)

from thursday.models.message import Message
from thursday.settings import APP_TITLE

MODULE_NAME = 'Message'
TAGS = [MODULE_NAME]
log = getLogger(f"{APP_TITLE}.api.v1.messages")


class MessagePostViewSchema(ExtSchema):
    tenant_id = fields.String(required=True)
    conversation_id = fields.String(required=True)
    customer_id = fields.String(required=False, allow_none=True)
    status = fields.Integer(required=False)
    content = fields.String(required=True)
    sender_type = fields.Integer(required=True)


class MessagePostInquiryView(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'body',
        'name': 'body',
        'type': 'object',
        'schema': DatatableViewSchema
    }]
    responses = DefaultResponsesWith({
        '200': {
            "description": "Message list",
            "schema": DatatableViewSchemaResponseSchema
        }
    })
    validation = False
    security = [{
        'ApiKeyAuth': [],
        'JWT': []
    }]

    def post(self):
        """
        Inquiry View
        """
        form = request.get_json(silent=True) or {}
        log.info("*Message Datatable Load %s", form)
        required_filters = {}
        records, recordsTotal, recordsFiltered = Message.search(form, [], required_filters)
        return jsonify({'total': recordsTotal, 'items': records, 'filtered': recordsFiltered})


class MessageGetView(ExtSwaggerView):
    tags = TAGS
    parameters = [
        {
            'name': '_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID Filter'
        },
    ]
    responses = DefaultResponsesWith({
        '200': {
            "description": "Details of specific ID",
            "schema": MessagePostViewSchema
        },
    })

    def get(self, _id):
        """
        Fetch By ID
        """
        record = Message.getDocument(_id)
        log.info('record: %s', record)
        if not record:
            return abort(404, msg=f"{MODULE_NAME} not found")
        result = MessagePostViewSchema.getmaps(record)
        return jsonify({'record': result}), 200


class MessagePostView(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'body',
        'name': 'body',
        'type': 'object',
        'schema': MessagePostViewSchema
    }]
    responses = DefaultResponsesWith({
        '200': {
            "description": "Success Response",
            "schema": PostSuccessSchema
        },
        '404': {
            'description': 'Generic Error Message / Value Error Message',
            'schema': PostErrorSchema
        }
    })
    validation = False
    security = [{
        'ApiKeyAuth': [],
        'JWT': []
    }]

    def post(self):
        """
        Create Message
        """
        form = request.get_json(silent=True) or request.form
        log.info('form: %s', form)
        args = MessagePostViewSchema.postmap(form)
        instance = Message.create(args)
        return jsonify({'success': True, 'id': str(instance._id)}), 200


class MessagePutView(ExtSwaggerView):
    tags = TAGS
    parameters = [
        {
            'name': '_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID Filter'
        },
        {
            'in': 'body',
            'name': 'body',
            'type': 'object',
            'schema': MessagePostViewSchema
        }
    ]
    responses = DefaultResponsesWith({
        '200': {
            "description": "Success Response",
            "schema": PostSuccessSchema
        },
        '404': {
            'description': 'Generic Error Message / Value Error Message',
            'schema': PostErrorSchema
        }
    })
    validation = False
    security = [{
        'ApiKeyAuth': [],
        'JWT': []
    }]

    def put(self, _id):
        """
        PUT View
        """
        try:
            message = Message.getDocument(_id)
            if not message:
                return abort(404, msg=f"{MODULE_NAME} not found")
            form = request.get_json(silent=True) or request.form
            args = MessagePostViewSchema().load(form, partial=True, unknown=EXCLUDE)
            message.update(args)
            return jsonify({'success': True}), 200
        except Exception as e:
            log.error('Message update error: %s', e)
            return abort(500, msg=str(e))


class MessageDeleteView(ExtSwaggerView):
    tags = TAGS
    parameters = [
        {
            'name': '_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID Filter'
        },
    ]
    responses = DefaultResponsesWith({
        '200': {
            "description": "Success Response",
            "schema": PostSuccessSchema
        },
        '404': {
            'description': 'Generic Error Message / Value Error Message',
            'schema': PostErrorSchema
        }
    })
    validation = False
    security = [{
        'ApiKeyAuth': [],
        'JWT': []
    }]

    def delete(self, _id):
        """
        DELETE View
        """
        try:
            message = Message.getDocument(_id)
            if not message:
                return abort(404, msg=f"{MODULE_NAME} not found")
            Message.collection.delete_one({'_id': ObjectId(_id)})
            return jsonify({'success': True}), 200
        except Exception as e:
            log.error('Message delete error: %s', e)
            return abort(500, msg=str(e))

