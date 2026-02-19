from marshmallow import EXCLUDE, missing
from bson.errors import InvalidId
from bson.objectid import ObjectId
from flasgger import fields, Schema, SwaggerView
from werkzeug.exceptions import HTTPException
from common.jsonify import jsonify as _jsonify
from flask import request, abort as original_flask_abort, make_response
from logging import getLogger
from thursday.settings import SOCKETIO_REDIS_HOST, SOCKETIO_REDIS_CHANNEL, REDIS_PASSWORD, S3_BUCKET, DEFAULT_TIMEZONE
from flask_socketio import SocketIO


from common.dict_tools import merge_dicts

socketio = SocketIO(message_queue=f'redis://:{REDIS_PASSWORD}@{SOCKETIO_REDIS_HOST}:6379/{SOCKETIO_REDIS_CHANNEL}')

log = getLogger('thrusday.ext')
api_route_config = {
    'origin': '*',
    'methods': ['OPTIONS', 'GET', 'POST', 'PUT', 'DELETE'],
    'allow_header': ['Authorization', 'Content-Type']
}
PAGINATION_PARAMETERS = [
    {
        'name': 'start',
        'in': 'query',
        'type': 'int',
        'required': False,
        'description': 'starting record index for retrieval'
    }, {
        'name': 'length',
        'in': 'query',
        'type': 'int',
        'required': False,
        'description': 'number of records to show'
    }, {
        'name': 'sortBy',
        'in': 'query',
        'type': 'string',
        'required': False,
        'description': 'name of field to sort on'
    }, {
        'name': 'sortDesc',
        'in': 'query',
        'type': 'bool',
        'required': False,
        'description': 'if true, will sort the records in descending order'
    }, {
        'name': 'search[value]',
        'in': 'query',
        'type': 'string',
        'required': False,
        'description': 'a keyword to search on records'
    },
]
FILES_PARAMETERS = [
    {
        'in': 'formData',
        'name': 'media1',
        'type': 'file',
        'required': False,
        'description': 'Incident media'
    }, {
        'in': 'formData',
        'name': 'media2',
        'type': 'file',
        'required': False,
        'description': 'Incident media'
    }, {
        'in': 'formData',
        'name': 'media3',
        'type': 'file',
        'required': False,
        'description': 'Incident media'
    }, {
        'in': 'formData',
        'name': 'media4',
        'type': 'file',
        'required': False,
        'description': 'Incident media'
    },
    {
        'in': 'formData',
        'name': 'media5',
        'type': 'file',
        'required': False,
        'description': 'Incident media'
    }]


def add_api_url_rules(app, rules):
    for path, cls, method in rules:
        app.add_url_rule(path, view_func=cls.as_view(cls.getViewName()), methods=[method])
        app.view_functions[cls.getViewName()] = (app.view_functions[cls.getViewName()])
        #cross_origin(**api_route_config)(app.view_functions[cls.getViewName()])


def validateOID(value):
    if value is None:
        return None
    if isinstance(value, ObjectId):
        return value
    try:
        return ObjectId(value)
    except:
        abort(410, message='Invalid Object ID')


class ObjectIdField(fields.String):
    """ObjectId field."""

    default_error_messages = {"invalid_objectid": "Not a valid ObjectId."}

    def _validated(self, value):
        """Format the value or raise a :exc:`ValidationError` if an error occurs."""
        if value is None:
            return None
        if isinstance(value, ObjectId):
            return value
        try:
            return ObjectId(value)
        except (ValueError, AttributeError, TypeError, InvalidId) as error:
            self.fail('invalid_objectid')

    def _deserialize(self, value, attr, data, **kwargs):
        return self._validated(value)
fields.ObjectId = ObjectIdField


def jsonify(*args, **kwargs):
    return _jsonify(*args, **kwargs)


def abort(http_status_code, **kwargs):
    try:
        original_flask_abort(make_response(jsonify(kwargs), http_status_code))
    except Exception as ex:
        log.info('abort_exception: %s', ex)
        ex.data = kwargs
        raise
    except HTTPException as e:
        log.info("HTTPException: %s", e)
        if len(kwargs):
            e.data = kwargs
        raise

def parseValidationError(errors, schema):
    error_string = []
    log.info('schema: %s', schema)
    for key, value in errors.items():
        field = schema().fields.get(key, {}).get(metadata, {})
        row = f"{field.get('description', '')}: {','.join(value)}"
        error_string.append(row)
    return '. '.join(error_string)

class ExtSchema(Schema):
    _mapping = {}
    @classmethod
    def getmap(cls, field_name, target, schema_fields):
        schema_field = schema_fields[field_name]
        mapping = schema_field.metadata.get('mapping')
        v = target
        if mapping is None:
            mapping = field_name
        for el in mapping.split('.'):
            if el[-2:] in ('{}', '[]'):
                default = {} if el[-2:] == '{}' else []
                v = v.get(el[:-2], default)
            else:
                v = v.get(el, schema_field.default if schema_field.default != missing else None)
                if schema_field.__class__.__name__ != 'Nested':
                    try:
                        v = schema_field.deserialize(v)
                    except:
                        pass
        if schema_field.__class__.__name__ == 'Nested':
            if schema_field.many:
                v = [schema_field.nested.getmaps(sv) for sv in v]
            else:
                v = schema_field.nested.getmaps(v)
        return v

    @classmethod
    def getmaps(cls, target):
        schema_fields = cls().fields
        return {field: cls.getmap(field, target, schema_fields) for field, field_prop in schema_fields.items()}

    @classmethod
    def postmap(cls, input):
        output = {}
        schema_fields = cls().fields
        input = cls().load(input, unknown=EXCLUDE)
        # if input.errors != {}:
        if 'errors' in input:
            abort(400, message=input.errors)
        # for field_name, field_value in input.data.items():
        for field_name, field_value in input.items():
            schema_field = schema_fields[field_name]
            mapping = schema_field.metadata.get('mapping')
            if mapping is None:
                mapping = field_name
            v = output
            for el in mapping.split('.'):
                if el[-2:] in ['{}', '[]']:
                    default = {} if el[-2:] == '{}' else []
                    v[el[:-2]] = v.get(el[:-2], default)
                    v = v[el[:-2]]
                else:
                    if schema_field.__class__.__name__ == 'Nested':
                        if schema_field.many:
                            field_value = [schema_field.nested.postmap(sv) for sv in field_value]
                        else:
                            field_value = schema_field.nested.postmap(field_value)
                    v[el] = field_value
        return output


def DefaultResponsesWith(additional_responses):
    responses = {
        '401': {
            "description": "Authentication error message",
            "schema": PostErrorSchema
        },
        '400': {
            "description": "Validation error message",
            "schema": PostErrorSchema
        },
    }
    responses.update(additional_responses)
    return responses


class PostResultSchema(ExtSchema):
    id = fields.ObjectId(mapping='_id')


class PostErrorSchema(Schema):
    message = fields.Str()


class PostSuccessSchema(Schema):
    success = fields.Boolean()


class ReferencesDictSchema(Schema):
    references = fields.Dict()

class DatatableViewSchemaResponseSchema(ExtSchema):
    items = fields.Dict()
    total = fields.Int()
    filtered = fields.Int()

class DatatableViewSchema(ExtSchema):
    start = fields.Int()
    length = fields.Int()
    sortBy = fields.Str()
    sortDesc = fields.Bool()
    searchValue = fields.Str(mapping='search[value]')

class ExtSwaggerView(SwaggerView):
    @classmethod
    def getViewName(cls):
        return cls.__name__.lower()


class DeleteSelectedViewSchema(ExtSchema):
    selected_ids = fields.List(fields.Str(), required=True)
    