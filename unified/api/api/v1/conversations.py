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

from thursday.models.conversation import Conversation
from thursday.settings import APP_TITLE

MODULE_NAME = 'Conversation'
TAGS = [MODULE_NAME]
log = getLogger(f"{APP_TITLE}.api.v1.conversations")


class ConversationPostViewSchema(ExtSchema):
    tenant_id = fields.String(required=True)
    bot_id = fields.String(required=True)
    channel_type = fields.Integer(required=True)
    customer_id = fields.String(required=True)
    status = fields.Integer(required=True)


class ConversationPostInquiryView(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'body',
        'name': 'body',
        'type': 'object',
        'schema': DatatableViewSchema
    }]
    responses = DefaultResponsesWith({
        '200': {
            "description": "Conversation list",
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
        log.info("*Conversation Datatable Load %s", form)
        required_filters = {}
        records, recordsTotal, recordsFiltered = Conversation.search(form, [], required_filters)
        return jsonify({'total': recordsTotal, 'items': records, 'filtered': recordsFiltered})


class ConversationGetView(ExtSwaggerView):
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
            "schema": ConversationPostViewSchema
        },
    })

    def get(self, _id):
        """
        Fetch By ID
        """
        record = Conversation.getDocument(_id)
        log.info('record: %s', record)
        if not record:
            return abort(404, msg=f"{MODULE_NAME} not found")
        result = ConversationPostViewSchema.getmaps(record)
        return jsonify({'record': result}), 200


class ConversationPostView(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'body',
        'name': 'body',
        'type': 'object',
        'schema': ConversationPostViewSchema
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
        Create Conversation
        """
        form = request.get_json(silent=True) or request.form
        log.info('form: %s', form)
        args = ConversationPostViewSchema.postmap(form)
        instance = Conversation.create(args)
        return jsonify({'success': True, 'id': str(instance._id)}), 200


class ConversationPutView(ExtSwaggerView):
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
            'schema': ConversationPostViewSchema
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
            conversation = Conversation.getDocument(_id)
            if not conversation:
                return abort(404, msg=f"{MODULE_NAME} not found")
            form = request.get_json(silent=True) or request.form
            args = ConversationPostViewSchema().load(form, partial=True, unknown=EXCLUDE)
            conversation.update(args)
            return jsonify({'success': True}), 200
        except Exception as e:
            log.error('Conversation update error: %s', e)
            return abort(500, msg=str(e))


class ConversationDeleteView(ExtSwaggerView):
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
            conversation = Conversation.getDocument(_id)
            if not conversation:
                return abort(404, msg=f"{MODULE_NAME} not found")
            Conversation.collection.delete_one({'_id': ObjectId(_id)})
            return jsonify({'success': True}), 200
        except Exception as e:
            log.error('Conversation delete error: %s', e)
            return abort(500, msg=str(e))

