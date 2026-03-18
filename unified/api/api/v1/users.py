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

from thursday.models.user import User
from thursday.settings import APP_TITLE

MODULE_NAME = 'User'
TAGS = [MODULE_NAME]
log = getLogger(f"{APP_TITLE}.api.v1.users")


class UserPostViewSchema(ExtSchema):
    tenant_id = fields.String(required=True)
    name = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    contact_number = fields.String(required=False, allow_none=True)
    email_address = fields.String(required=False, allow_none=True)
    address = fields.String(required=False, allow_none=True)


class UserPostInquiryView(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'body',
        'name': 'body',
        'type': 'object',
        'schema': DatatableViewSchema
    }]
    responses = DefaultResponsesWith({
        '200': {
            "description": "User list",
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
        log.info("*User Datatable Load %s", form)
        required_filters = {}
        records, recordsTotal, recordsFiltered = User.search(form, [], required_filters)
        return jsonify({'total': recordsTotal, 'items': records, 'filtered': recordsFiltered})


class UserGetView(ExtSwaggerView):
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
            "schema": UserPostViewSchema
        },
    })

    def get(self, _id):
        """
        Fetch By ID
        """
        record = User.getDocument(_id)
        log.info('record: %s', record)
        if not record:
            return abort(404, msg=f"{MODULE_NAME} not found")
        result = UserPostViewSchema.getmaps(record)
        return jsonify({'record': result}), 200


class UserPostView(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'body',
        'name': 'body',
        'type': 'object',
        'schema': UserPostViewSchema
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
        Create User
        """
        form = request.get_json(silent=True) or request.form
        log.info('form: %s', form)
        args = UserPostViewSchema.postmap(form)
        instance = User.create(args)
        return jsonify({'success': True, 'id': str(instance._id)}), 200


class UserPutView(ExtSwaggerView):
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
            'schema': UserPostViewSchema
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
            user = User.getDocument(_id)
            if not user:
                return abort(404, msg=f"{MODULE_NAME} not found")
            form = request.get_json(silent=True) or request.form
            args = UserPostViewSchema().load(form, partial=True, unknown=EXCLUDE)
            user.update(args)
            return jsonify({'success': True}), 200
        except Exception as e:
            log.error('User update error: %s', e)
            return abort(500, msg=str(e))


class UserDeleteView(ExtSwaggerView):
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
            user = User.getDocument(_id)
            if not user:
                return abort(404, msg=f"{MODULE_NAME} not found")
            User.collection.delete_one({'_id': ObjectId(_id)})
            return jsonify({'success': True}), 200
        except Exception as e:
            log.error('User delete error: %s', e)
            return abort(500, msg=str(e))

