from bson.objectid import ObjectId
from logging import getLogger
from flask import request, current_app, session, url_for, request, make_response, send_file, Response
from flasgger import Swagger, SwaggerView, Schema, fields

from common.jsonify import jsonify

from api.v1.ext import ExtSchema, DefaultResponsesWith, PostResultSchema, PostSuccessSchema, PostErrorSchema, ExtSwaggerView , \
    PAGINATION_PARAMETERS, ReferencesDictSchema, DatatableViewSchemaResponseSchema, DatatableViewSchema, DeleteSelectedViewSchema , \
    SOCKETIO_REDIS_HOST, SOCKETIO_REDIS_CHANNEL, REDIS_PASSWORD, parseValidationError, FILES_PARAMETERS

from thursday.settings import APP_TITLE


import ollama

TAGS = ['Chat']
log = getLogger(f"{APP_TITLE}.api.v1.chat")

class ChatPostViewSchema(ExtSchema):
    question = fields.Str(required=True)
    tenant_id = fields.ObjectId(required=False)



class ChatPostView(ExtSwaggerView):
    tags = TAGS
    parameters = [{
        'in': 'body',
        'name': 'body',
        'type': 'object',
        'schema': ChatPostViewSchema
    }]
    responses = DefaultResponsesWith({
        '200': {
            "description": "Chat Response" ,
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
        Chat post view
        """
        args = ChatPostViewSchema.postmap(request.json)
        log.info('args: %s', args)
        question = args.get('question')

        messages = [{"role": "user", "content": question}]

        response_text = ""
        for part in ollama.chat("llama3.2", messages=messages, stream=True):
            response_text += part["message"]["content"]


        return jsonify({'response': response_text}), 200
