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
log = getLogger(f"{APP_TITLE}.api.v1.chat")

def detect_intent(query):
    prompt = f"""
    Classify the following user query into one of these intents:
    - services
    - products
    Only return the intent name.

    Query: {query}
    """
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    log.info('detect_intent: %s', response)
    return response["message"]["content"].strip().lower()


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
        result = rag_chat(question)
        log.info('result: %s', result)
        # messages = [{"role": "user", "content": question}]

        # response_text = ""
        # for part in ollama.chat("llama3.2", messages=messages, stream=True):
        #     response_text += part["message"]["content"]


        return jsonify({'response': result}), 200



def rag_chat(query):
    intent = detect_intent(query)
    log.info('intent: %s', intent)
    vs = VectorService("rsp_dental_clinic")
    response = ollama.embed(model="mxbai-embed-large", input=[query])
    results = vs.collection.query(
        query_embeddings=response.embeddings,
        n_results=5,
        where={"category": intent}
    )
    log.info('cs_count: %s', vs.collection.count())
    data = vs.collection.get()
    log.info('data: %s', data)

    log.info('results: %s', results)
    docs = results["documents"][0]

    context = "\n".join([f"- {d}" for d in docs])

    prompt = f"""
        User question: {query}

        Use ONLY this info:
        {context}

        Answer clearly and short.
        """

    answer = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "intent": intent,
        "answer": answer["message"]["content"],
        "sources": docs
    }