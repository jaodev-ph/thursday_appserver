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

from thursday.models.customer import Customer
from thursday.settings import APP_TITLE

MODULE_NAME = 'Customer'
TAGS = [MODULE_NAME]
log = getLogger(f"{APP_TITLE}.api.v1.customers")


class CustomerPostViewSchema(ExtSchema):
    tenant_id = fields.String(required=True)
    name = fields.String(required=True)
    avatart = fields.String(required=False, allow_none=True)
    contact_number = fields.String(required=False, allow_none=True)
    email_address = fields.String(required=False, allow_none=True)
    address = fields.String(required=False, allow_none=True)
    channel_type = fields.Integer(required=False)
    active = fields.Boolean(required=False)


class CustomerPostInquiryView(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'body',
        'name': 'body',
        'type': 'object',
        'schema': DatatableViewSchema
    }]
    responses = DefaultResponsesWith({
        '200': {
            "description": "Customer list",
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
        log.info("*Customer Datatable Load %s", form)
        required_filters = {}
        records, recordsTotal, recordsFiltered = Customer.search(form, [], required_filters)
        return jsonify({'total': recordsTotal, 'items': records, 'filtered': recordsFiltered})


class CustomerGetView(ExtSwaggerView):
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
            "schema": CustomerPostViewSchema
        },
    })

    def get(self, _id):
        """
        Fetch By ID
        """
        record = Customer.getDocument(_id)
        log.info('record: %s', record)
        if not record:
            return abort(404, msg=f"{MODULE_NAME} not found")
        result = CustomerPostViewSchema.getmaps(record)
        return jsonify({'record': result}), 200


class CustomerPostView(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'body',
        'name': 'body',
        'type': 'object',
        'schema': CustomerPostViewSchema
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
        Create Customer
        """
        form = request.get_json(silent=True) or request.form
        log.info('form: %s', form)
        args = CustomerPostViewSchema.postmap(form)
        instance = Customer.create(args)
        return jsonify({'success': True, 'id': str(instance._id)}), 200


class CustomerPutView(ExtSwaggerView):
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
            'schema': CustomerPostViewSchema
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
            customer = Customer.getDocument(_id)
            if not customer:
                return abort(404, msg=f"{MODULE_NAME} not found")
            form = request.get_json(silent=True) or request.form
            args = CustomerPostViewSchema().load(form, partial=True, unknown=EXCLUDE)
            customer.update(args)
            return jsonify({'success': True}), 200
        except Exception as e:
            log.error('Customer update error: %s', e)
            return abort(500, msg=str(e))


class CustomerDeleteView(ExtSwaggerView):
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
            customer = Customer.getDocument(_id)
            if not customer:
                return abort(404, msg=f"{MODULE_NAME} not found")
            Customer.collection.delete_one({'_id': ObjectId(_id)})
            return jsonify({'success': True}), 200
        except Exception as e:
            log.error('Customer delete error: %s', e)
            return abort(500, msg=str(e))

