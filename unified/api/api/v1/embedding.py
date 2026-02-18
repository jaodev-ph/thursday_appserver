from bson.objectid import ObjectId
from logging import getLogger
from flask import request, current_app, session, url_for, request, make_response, send_file, Response
from flasgger import Swagger, SwaggerView, Schema, fields

from common.jsonify import jsonify

from api.v1.ext import ExtSchema, DefaultResponsesWith, PostResultSchema, PostSuccessSchema, PostErrorSchema, ExtSwaggerView , \
    PAGINATION_PARAMETERS, ReferencesDictSchema, DatatableViewSchemaResponseSchema, DatatableViewSchema, DeleteSelectedViewSchema , \
    SOCKETIO_REDIS_HOST, SOCKETIO_REDIS_CHANNEL, REDIS_PASSWORD, parseValidationError, FILES_PARAMETERS

from thursday.settings import APP_TITLE
from thursday.vector_service import VectorService

import ollama

TAGS = ['Chat']
log = getLogger(f"{APP_TITLE}.api.v1.embeddings")

class EmmbeddingPostViewSchema(ExtSchema):
    ids = fields.List(fields.String(), required=True, default=[])
    documents = fields.List(fields.String(), required=True, default=[])
    metadatas = fields.List(fields.String(), required=True, default=[])

class EmbeddingPostView(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'body',
        'name': 'body',
        'type': 'object',
        'schema': EmmbeddingPostViewSchema
    }]
    responses = DefaultResponsesWith({
        '200': {
            "description": "Data Embeddings" ,
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
        Embedding Post View
        """
        pass


        return jsonify({'response': ""}), 200