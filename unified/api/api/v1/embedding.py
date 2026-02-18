from bson.objectid import ObjectId
from logging import getLogger
from flask import request, current_app, session, url_for, request, make_response, send_file, Response
from flasgger import Swagger, SwaggerView, Schema, fields

from common.jsonify import jsonify

from api.v1.ext import ExtSchema, DefaultResponsesWith, PostResultSchema, PostSuccessSchema, PostErrorSchema, ExtSwaggerView , \
    PAGINATION_PARAMETERS, ReferencesDictSchema, DatatableViewSchemaResponseSchema, DatatableViewSchema, DeleteSelectedViewSchema , \
    SOCKETIO_REDIS_HOST, SOCKETIO_REDIS_CHANNEL, REDIS_PASSWORD, parseValidationError, FILES_PARAMETERS

from thursday.settings import APP_TITLE
from thursday.vector_service import VectorService, vector_client

import ollama

TAGS = ['Chat']
log = getLogger(f"{APP_TITLE}.api.v1.embeddings")

class EmmbeddingPostViewSchema(ExtSchema):
    collection_name = fields.String(required=True)
    id_prefix = fields.String(required=True)
    documents = fields.List(fields.String(), required=True, default=[])
    metadatas = fields.List(fields.Dict(), required=True, default=[])

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
        form = request.json
        args = EmmbeddingPostViewSchema.postmap(form)
        id_prefix = args.get('id_prefix')
        collection = VectorService(args.get('collection_name'))
        documents = args.get('documents', [])
        metadatas = args.get('metadatas', [])
        log.info('metadatas;: %s', metadatas)
        for i, doc in enumerate(documents):
            vid = f"{id_prefix}_{i}"
            collection.add(
                ids=[vid],
                documents=[doc],
                metadatas=[metadatas[i]]
            )
        return jsonify({'response': args}), 200





class EmbeddingDeleteView(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'path',
        'name': 'collection_name',
        'type': 'string',
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
    def delete(self, collection_name):
        """ 
        Embedding Post View
        """
        log.info('list: %s', vector_client.list_collections())
        log.info('collection_name: %s', collection_name)
        result = vector_client.delete_collection(collection_name)
        log.info('result: %s', result)
        return jsonify({'message': "Successful Deleted"}), 200