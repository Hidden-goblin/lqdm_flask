from flask import Response, request
from flasgger import validate
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt_claims
from flask_bcrypt import generate_password_hash

from database.models import User, Session
from flask_restful import Resource
from json import dumps
import datetime
import os
import uuid
from logging import getLogger

from utils.errors import schema_error, user_schema_validation

log = getLogger(__name__)


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
                        message:
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
                example: {"message": "message example"}
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
        user_uuid = str(uuid.uuid4())
        Session(**{"user_hash": user_uuid}).save()
        access_token = create_access_token(identity=str(user.id), expires_delta=expires, user_claims={"hash": user_uuid})
        return Response(dumps({'token': access_token}), mimetype="application/json", status=200)


class UserApi(Resource):
    @jwt_required
    def get(self, user_id):
        """
        Retrieve a specific user.
        ---
        tags:
            - users
        security:
            - BearerAuth: []
        parameters:
            - name: Authorization
              in: header
              type: string
              description: "'Bearer JWT' value"
            - name: user_id
              in: path
              required: true
              type: string
        definitions:
            account:
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
                    role:
                        type: string
                        required: true
                        enum: ["Admin", "GM", "Player", "Writer"]
                    creation_date:
                        $ref: '#/definitions/date'
                        required: true
                    update_date:
                        $ref: '#/definitions/date'
                        required: true
        """
        print(f"user_id {user_id}")
        user_uuid = get_jwt_claims()["hash"]
        log.warning(f"user uuid {user_uuid}")
        user_session = Session.objects(user_hash=user_uuid)
        log.warning(f"user session {user_session}")
        if user_session:
            return Response(dumps({"message": "toto"}), 200)
        else:
            return Response(dumps({"message": "titi"}), 200)


class UsersApi(Resource):
    @jwt_required
    def get(self):
        pass


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
