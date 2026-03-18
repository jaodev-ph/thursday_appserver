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

from thursday.models.acl_profile import AclProfile
from thursday.settings import APP_TITLE

MODULE_NAME = 'AclProfile'
TAGS = [MODULE_NAME]
log = getLogger(f"{APP_TITLE}.api.v1.acl_profiles")


class AclProfilePostViewSchema(ExtSchema):
    tenant_id = fields.String(required=True)
    name = fields.String(required=True)
    access_control = fields.Dict(required=False)
    active = fields.Boolean(required=False)


class AclProfilePostInquiryView(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'body',
        'name': 'body',
        'type': 'object',
        'schema': DatatableViewSchema
    }]
    responses = DefaultResponsesWith({
        '200': {
            "description": "ACL Profiles list",
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
        log.info("*AclProfile Datatable Load %s", form)
        required_filters = {}
        records, recordsTotal, recordsFiltered = AclProfile.search(form, [], required_filters)
        return jsonify({'total': recordsTotal, 'items': records, 'filtered': recordsFiltered})


class AclProfileGetView(ExtSwaggerView):
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
            "schema": AclProfilePostViewSchema
        },
    })

    def get(self, _id):
        """
        Fetch By ID
        """
        record = AclProfile.getDocument(_id)
        log.info('record: %s', record)
        if not record:
            return abort(404, msg=f"{MODULE_NAME} not found")
        result = AclProfilePostViewSchema.getmaps(record)
        return jsonify({'record': result}), 200


class AclProfilePostView(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'body',
        'name': 'body',
        'type': 'object',
        'schema': AclProfilePostViewSchema
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
        Create ACL Profile
        """
        form = request.get_json(silent=True) or request.form
        log.info('form: %s', form)
        args = AclProfilePostViewSchema.postmap(form)
        instance = AclProfile.create(args)
        return jsonify({'success': True, 'id': str(instance._id)}), 200


class AclProfilePutView(ExtSwaggerView):
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
            'schema': AclProfilePostViewSchema
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
            profile = AclProfile.getDocument(_id)
            if not profile:
                return abort(404, msg=f"{MODULE_NAME} not found")
            form = request.get_json(silent=True) or request.form
            args = AclProfilePostViewSchema().load(form, partial=True, unknown=EXCLUDE)
            profile.update(args)
            return jsonify({'success': True}), 200
        except Exception as e:
            log.error('AclProfile update error: %s', e)
            return abort(500, msg=str(e))


class AclProfileDeleteView(ExtSwaggerView):
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
            profile = AclProfile.getDocument(_id)
            if not profile:
                return abort(404, msg=f"{MODULE_NAME} not found")
            AclProfile.collection.delete_one({'_id': ObjectId(_id)})
            return jsonify({'success': True}), 200
        except Exception as e:
            log.error('AclProfile delete error: %s', e)
            return abort(500, msg=str(e))

