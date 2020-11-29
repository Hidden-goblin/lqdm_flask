from flask import Response, request
from flasgger import validate
from flask_jwt_extended import create_access_token
from flask_bcrypt import generate_password_hash

from database.models import User
from flask_restful import Resource
from json import dumps
import datetime
import os

from utils.errors import schema_error, user_schema_validation


class SignupApi(Resource):
    def post(self):
        """
        Create a basic account to access the character creation
        ---
        tags:
            - users
        definitions:
            user:
                type: object
                properties:
                    email:
                        type: string
                        format: email
                        required: true
                    password:
                        type: string
                        format: password
                        required: true
        parameters:
            - name: body
              in: body
              schema:
                $ref: '#/definitions/user'
        responses:
            200:
                schema:
                    id: user-id
                    type: object
                    properties:
                        id:
                            type: string
            400:
                schema:
                    $ref: '#/definitions/error'
        """
        swagger_path = f"{os.getcwd()}/swagger/signup.yml"
        validate(request.json,
                 "user",
                 swagger_path,
                 validation_error_handler=schema_error,
                 validation_function=user_schema_validation
                 )
        body = request.get_json()
        user = User(**body)
        user.hash_password()
        user.save()
        id = user.id
        return Response({'id': str(id)}, mimetype="application/json", status=200)


class LoginApi(Resource):
    def post(self):
        """
        Log into the app by requesting a JWT
        ---
        tags:
            - users
        parameters:
            - name: body
              in: body
              schema:
                $ref: '#/definitions/user'
        responses:
            401:
                schema:
                    $ref: '#/definitions/error'
            400:
                schema:
                    $ref: '#/definitions/error'
            200:
                schema:
                    type: object
                    properties:
                        token:
                            type: string

        """
        swagger_path = f"{os.getcwd()}/swagger/signup.yml"
        validate(request.json,
                 "user",
                 swagger_path,
                 validation_error_handler=schema_error,
                 validation_function=user_schema_validation)
        body = request.get_json()
        user = User.objects.get(email=body.get('email'))
        authorized = user.check_password(body.get('password'))
        if not authorized:
            return Response(dumps({"message": "unrecognized credentials"}), mimetype="application/json", status=401)

        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return Response(dumps({'token': access_token}), mimetype="application/json", status=200)


def initialize_users():
    users = [{"email": "player@test.com",
              "password": generate_password_hash("player123").decode('utf8'),
              "role": "Player"},
             {"email": "writer@test.com",
              "password": generate_password_hash("writer123").decode('utf8'),
              "role": "Writer"}
             ]
    try:
        for user in users:
            try:
                if User.objects.get(email=user["email"]):
                    User(email=user["email"]).update(password=user["password"], upsert=True)
            except Exception:
                User(**user).update(**user, upsert=True)
    except Exception:
        print("User initit fail")
