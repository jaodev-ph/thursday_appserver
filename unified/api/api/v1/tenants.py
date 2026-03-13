

from logging import getLogger
from bson.objectid import ObjectId
from logging import getLogger
from flask import request, current_app, session, url_for, request, make_response, send_file, Response
from flasgger import Swagger, SwaggerView, Schema, fields

from common.jsonify import jsonify

from api.v1.ext import abort, ExtSchema, DefaultResponsesWith, PostResultSchema, PostSuccessSchema, PostErrorSchema, ExtSwaggerView , \
    PAGINATION_PARAMETERS, ReferencesDictSchema, DatatableViewSchemaResponseSchema, DatatableViewSchema, DeleteSelectedViewSchema , \
    SOCKETIO_REDIS_HOST, SOCKETIO_REDIS_CHANNEL, REDIS_PASSWORD, parseValidationError, FILES_PARAMETERS
#models
from thursday.models.tenant import Tenant

MODULE_NAME = 'Tenant'
TAGS = [MODULE_NAME]
log = getLogger(f"{APP_TITLE}.api.v1.chat")



class TenantPostViewSchema(ExtSchema):
    name = fields.String(required=True)
    contact_number = fields.String(required=True)
    email_address = fields.String(required=False, allow_none=True)
    address = fields.String(required=False, allow_none=True)
    logo = fields.String(required=False, allow_none=True)
    bot_id = fields.String(required=False, allow_none=True)  # could be ObjectId or string
    business_type = fields.String(required=False, allow_none=True)
    geolocation = fields.List(fields.Float())  # e.g., {"lat": 0.0, "lng": 0.0}


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
        if record:
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
        pass
        return jsonify({'sucecss': True}), 200
