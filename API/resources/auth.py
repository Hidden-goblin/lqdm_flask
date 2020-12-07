from flask import Response, request
from flasgger import validate
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt_claims
from flask_bcrypt import generate_password_hash
from mongoengine import DoesNotExist, MultipleObjectsReturned

from database.db import update_payload
from database.models import User, Session
from flask_restful import Resource
from json import dumps
import datetime
import os
import uuid
from logging import getLogger

from utils.errors import schema_error, user_schema_validation
from utils.middle import is_access_granted, error_message

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


class LogoutApi(Resource):
    @jwt_required
    def post(self):
        """
        Log into the app by requesting a JWT
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
        parameters:
            - name: body
              in: body
              schema:
                type: object
                properties:
                    email:
                        type: string
                        example: 'user@lqdm.com'
        responses:
            401:
                schema:
                    $ref: '#/definitions/error'
                example: {"message": "Cannot terminate the session"}
            400:
                schema:
                    $ref: '#/definitions/error'
                example: {"message": "Cannot terminate the session"}
            200:
                schema:
                    $ref: '#/definitions/error'
                example: {"message": "Session ended"}
        """
        body = request.get_json()
        user = User.objects.get(email=body.get("email"))
        session, error = is_access_granted(get_jwt_identity(), get_jwt_claims(), User.get_roles())
        if session and user.email == User.objects.get(id=get_jwt_identity()):
            Session.objects.delete(user_hash=get_jwt_claims()["hash"])
            return error_message("Session ended", 200)
        else:
            return error_message("Cannot terminate the session", error)


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
        responses:
            200:
                schema:
                    $ref: '#/definitions/account'
        """
        user_session, status_code = is_access_granted(get_jwt_identity(), get_jwt_claims(), ("Admin",))
        if user_session:
            try:
                return Response(User.objects.get(email=user_id).to_json(use_db_field=False),
                                mimetype="application/json", status=200)
            except DoesNotExist as done:
                return error_message(done.args, 404)
            except MultipleObjectsReturned as mor:
                return error_message(mor.args, 404)
        else:
            return error_message("Your are not allowed to access this resource", status_code)

    @jwt_required
    def put(self, user_id):
        """
        Update a specific user.
        ---
        tags:
            - users
        security:
            - BearerAuth: []
        definitions:
            dateless_account:
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
        parameters:
            - name: Authorization
              in: header
              type: string
              description: "'Bearer JWT' value"
            - name: user_id
              in: path
              required: true
              type: string
            - name: body
              in: body
              schema:
                $ref: '#/definitions/dateless_account'
        responses:
            200:
                schema:
                    $ref: '#/definitions/account'
            401:
                schema:
                    $ref: '#/definitions/error'
            403:
                schema:
                    $ref: '#/definitions/error'
            404:
                schema:
                    $ref: '#/definitions/error'
        """
        user_session, status_code = is_access_granted(get_jwt_identity(), get_jwt_claims(), ("Admin",))
        if user_session:
            try:
                user = User.objects.get(email=user_id)
                req = request.get_json()
                if "email" in req:
                    req.pop("email")
                req = update_payload(req)
                user.update(**req)
                return Response()
            except DoesNotExist as done:
                return error_message(done.args, 404)
            except MultipleObjectsReturned as mor:
                return error_message(mor.args, 404)
        else:
            return error_message("Your are not allowed to access this resource", status_code)

    @jwt_required
    def delete(self, user_id):
        """
        Delete a specific user. Could be self.
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
        responses:
            204:
                description: "The user has been successfully deleted"
            401:
                schema:
                    $ref: '#/definitions/error'
            403:
                schema:
                    $ref: '#/definitions/error'
            404:
                schema:
                    $ref: '#/definitions/error'
        """
        user = User.objects.get(email=user_id)
        if user == User.objects.get(id=get_jwt_identity()):
            user_session, status_code = is_access_granted(get_jwt_identity(),
                                                          get_jwt_claims(),
                                                          (user.role,))
            if user_session:
                user.delete()
                return Response(status=204)
            else:
                return error_message("Cannot delete account", status_code=status_code)
        else:
            user_session, status_code = is_access_granted(get_jwt_identity(),
                                                          get_jwt_claims(),
                                                          ('Admin',))
            if user_session:
                user.delete()
                return Response(status=204)
            else:
                return error_message("Cannot delete account", status_code)


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
              "role": "Writer"},
             {"email": "bobadmin@test.com",
              "password": generate_password_hash("bob!123").decode('utf8'),
              "role": "Admin"},
             {"email": "elsawriter@pencil.edu",
              "password": generate_password_hash("elsa!123").decode('utf8'),
              "role": "Writer"},
             {"email": "robinplayer@test.com",
              "password": generate_password_hash("robin!123").decode('utf8'),
              "role": "Player"}
             ]
    try:
        for user in users:
            log.warning(f"process {user['email']} user")
            try:
                db_user = User.objects.get(email=user["email"])
                db_user.update(password=user["password"], upsert=True)
                db_user.save()
            except Exception as exception_one:
                log.error(f"Exception when updating user\n {exception_one}")
                User(**user).update(**user, upsert=True)
    except Exception as exception_tow:
        log.error(f"User init fail\n {exception_tow}")
