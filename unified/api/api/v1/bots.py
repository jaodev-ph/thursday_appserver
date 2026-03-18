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

from thursday.models.bot import Bot
from thursday.settings import APP_TITLE

MODULE_NAME = 'Bot'
TAGS = [MODULE_NAME]
log = getLogger(f"{APP_TITLE}.api.v1.bots")


class BotPostViewSchema(ExtSchema):
    tenant_id = fields.String(required=True)
    name = fields.String(required=True)
    model = fields.String(required=True)
    active = fields.Boolean(required=False)


class BotPostInquiryView(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'body',
        'name': 'body',
        'type': 'object',
        'schema': DatatableViewSchema
    }]
    responses = DefaultResponsesWith({
        '200': {
            "description": "Bot list",
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
        log.info("*Bot Datatable Load %s", form)
        required_filters = {}
        records, recordsTotal, recordsFiltered = Bot.search(form, [], required_filters)
        return jsonify({'total': recordsTotal, 'items': records, 'filtered': recordsFiltered})


class BotGetView(ExtSwaggerView):
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
            "schema": BotPostViewSchema
        },
    })

    def get(self, _id):
        """
        Fetch By ID
        """
        record = Bot.getDocument(_id)
        log.info('record: %s', record)
        if not record:
            return abort(404, msg=f"{MODULE_NAME} not found")
        result = BotPostViewSchema.getmaps(record)
        return jsonify({'record': result}), 200


class BotPostView(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'body',
        'name': 'body',
        'type': 'object',
        'schema': BotPostViewSchema
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
        Create Bot
        """
        form = request.get_json(silent=True) or request.form
        log.info('form: %s', form)
        args = BotPostViewSchema.postmap(form)
        instance = Bot.create(args)
        return jsonify({'success': True, 'id': str(instance._id)}), 200


class BotPutView(ExtSwaggerView):
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
            'schema': BotPostViewSchema
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
            bot = Bot.getDocument(_id)
            if not bot:
                return abort(404, msg=f"{MODULE_NAME} not found")
            form = request.get_json(silent=True) or request.form
            args = BotPostViewSchema().load(form, partial=True, unknown=EXCLUDE)
            bot.update(args)
            return jsonify({'success': True}), 200
        except Exception as e:
            log.error('Bot update error: %s', e)
            return abort(500, msg=str(e))


class BotDeleteView(ExtSwaggerView):
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
            bot = Bot.getDocument(_id)
            if not bot:
                return abort(404, msg=f"{MODULE_NAME} not found")
            Bot.collection.delete_one({'_id': ObjectId(_id)})
            return jsonify({'success': True}), 200
        except Exception as e:
            log.error('Bot delete error: %s', e)
            return abort(500, msg=str(e))

