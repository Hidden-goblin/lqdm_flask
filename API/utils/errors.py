from json import dumps, load

from jsonschema import validate
from flask import Response
from werkzeug.exceptions import abort


def schema_error(err, data, schema):
    print(err)
    print(data)
    print(schema)
    abort(Response(dumps({"message": "The body doesn't comply to the expected schema."}),
                   status=400))


def user_schema_validation(data, schema):
    print("in user_schema_validation")
    with open("schemas/user.json") as file:
        user_schema = load(file)
        validate(data, user_schema)
