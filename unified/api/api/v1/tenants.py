
import time
from logging import getLogger
from bson.objectid import ObjectId
from logging import getLogger
from flask import request, current_app, session, url_for, request, make_response, send_file, Response
from flasgger import Swagger, SwaggerView, Schema, fields
from common.dict_tools import merge_dicts
from common.jsonify import jsonify
from marshmallow import EXCLUDE, missing

from api.v1.ext import abort, ExtSchema, DefaultResponsesWith, PostResultSchema, PostSuccessSchema, PostErrorSchema, ExtSwaggerView , \
    PAGINATION_PARAMETERS, ReferencesDictSchema, DatatableViewSchemaResponseSchema, DatatableViewSchema, DeleteSelectedViewSchema , \
    SOCKETIO_REDIS_HOST, SOCKETIO_REDIS_CHANNEL, REDIS_PASSWORD, parseValidationError, FILES_PARAMETERS
#models
from thursday.models.tenant import Tenant
from thursday.settings import APP_TITLE
MODULE_NAME = 'Tenant'
TAGS = [MODULE_NAME]
log = getLogger(f"{APP_TITLE}.api.v1.tenants")



class TenantPostViewSchema(ExtSchema):
    name = fields.String(required=True, min=3)
    contact_number = fields.String(required=True)
    email_address = fields.String(required=False, allow_none=True)
    address = fields.String(required=False, allow_none=True)
    logo = fields.String(required=False, allow_none=True)
    bot_id = fields.String(required=False, allow_none=True)  # could be ObjectId or string
    business_type = fields.String(required=False, allow_none=True)
    geolocation = fields.List(fields.Float())  # e.g., {"lat": 0.0, "lng": 0.0}

class TenantPostInquiryViewSchema(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'body',
        'name': 'body',
        'type': 'object',
        'schema': DatatableViewSchema
    }]
    responses = DefaultResponsesWith({
        '200': {
            "description": "Stations of Department" ,
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
        log.info("*Tenant Datatable Load")
        form = request.get_json()
        log.info('form: %s', form)
       
        required_filters = {}
        log.info('request.json: %s', request.form)
        records, recordsTotal = Tenant.search(request.json, [], required_filters)
        time.sleep(5)
        return jsonify({'total': recordsTotal, 'items': records })


class TenantGetView(ExtSwaggerView):
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
            "schema": TenantPostViewSchema
        },
    })
    def get(self, _id):
        """
        Fetch By ID
        """
        record = Tenant.getDocument(_id)
        log.info('record: %s', record)
        if not record:
            return abort(404, msg=f"{MODULE_NAME} not found")
        result = TenantPostViewSchema.getmaps(record)
        return jsonify({'record': result}), 200


class TenantPostView(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'body',
        'name': 'body',
        'type': 'object',
        'schema': TenantPostViewSchema
    }]
    responses = DefaultResponsesWith({
        '200': {
            "description": "Success Response" ,
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
        Create Post view
        """
        form = request.json or request.form
        log.info('form: %s', form)
        args = TenantPostViewSchema.postmap(form)
        tenant = Tenant.create(args)
        return jsonify({'sucecss': True}), 200
        # try:
           
        # except Exception as e:
        #     log.error('error: %s', e)
        #     return abort(500, msg=str(e))

class TenantPutView(ExtSwaggerView):
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
        }
    ]
    responses = DefaultResponsesWith({
        '200': {
            "description": "Success Response" ,
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
            tenant = Tenant.getDocument(_id)
            if not tenant:  
                return abort(404, msg=f"{MODULE_NAME} not found")
            form = request.json or request.form
            args = TenantPostViewSchema().load(form, partial=True, unknown=EXCLUDE)
            log.info('args: %s', args)
            tenant.update(args)
            return jsonify({'message': "Tenant updated successfully"}), 200
        except Exception as e:
            log.error('error: %s', e)
            return abort(500, msg=str(e))

class TenantDeleteView(ExtSwaggerView):
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
            "description": "Success Response" ,
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
            tenant = Tenant.getDocument(_id)
            if not tenant:
                return abort(404, msg=f"{MODULE_NAME} not found")
            tenant.remove()
            return jsonify({'message': "Tenant deleted successfully"}), 200
        except Exception as e:
            log.error('error: %s', e)
            return abort(500, msg=str(e))
        return jsonify({'sucecss': True}), 200
