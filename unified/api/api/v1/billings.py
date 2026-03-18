from logging import getLogger
from bson.objectid import ObjectId
from flask import request
from flasgger import SwaggerView, Schema, fields

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

from thursday.models.billing import Billing
from thursday.settings import APP_TITLE

MODULE_NAME = 'Billing'
TAGS = [MODULE_NAME]
log = getLogger(f"{APP_TITLE}.api.v1.billings")


class BillingPostViewSchema(ExtSchema):
    tenant_id = fields.String(required=True)
    plan = fields.String(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    status = fields.Int(required=True)  # BILLING_STATUS


class BillingPostInquiryView(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'body',
        'name': 'body',
        'type': 'object',
        'schema': DatatableViewSchema
    }]
    responses = DefaultResponsesWith({
        '200': {
            "description": "Success Response",
            "schema": DatatableViewSchemaResponseSchema
        },
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
        payload = request.get_json(silent=True) or {}
        required_filters = {}
        log.info('billing inquiry payload: %s', payload)
        # For now, no pagination helper wired; return all matching
        records = list(Billing.getDocuments(required_filters))
        total = len(records)
        return jsonify({'total': total, 'items': records, 'filtered': total})


class BillingGetView(ExtSwaggerView):
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
            "schema": BillingPostViewSchema
        },
    })

    def get(self, _id):
        """
        Fetch By ID
        """
        record = Billing.getDocument(_id)
        log.info('billing record: %s', record)
        if not record:
            return abort(404, msg=f"{MODULE_NAME} not found")
        result = record
        return jsonify({'record': result}), 200


class BillingPostView(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'body',
        'name': 'body',
        'type': 'object',
        'schema': BillingPostViewSchema
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
        Create billing record
        """
        form = request.get_json(silent=True) or request.form
        log.info('billing form: %s', form)
        args = BillingPostViewSchema.postmap(form)
        billing = Billing.create(args)
        return jsonify({'success': True, 'id': str(billing._id)}), 200


class BillingPutView(ExtSwaggerView):
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
            'schema': BillingPostViewSchema
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
            billing = Billing.getDocument(_id)
            if not billing:
                return abort(404, msg=f"{MODULE_NAME} not found")
            form = request.get_json(silent=True) or request.form
            log.info('billing update form: %s', form)
            args = BillingPostViewSchema.putmap(form)
            billing.update(args)
            return jsonify({'success': True}), 200
        except Exception as e:
            log.error('billing update error: %s', e)
            return abort(500, msg=str(e))


class BillingDeleteView(ExtSwaggerView):
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
            billing = Billing.getDocument(_id)
            if not billing:
                return abort(404, msg=f"{MODULE_NAME} not found")
            Billing.collection.delete_one({'_id': ObjectId(_id)})
            return jsonify({'success': True}), 200
        except Exception as e:
            log.error('billing delete error: %s', e)
            return abort(500, msg=str(e))

