import unidecode
from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from json import load, dumps, loads
from utils.middle import is_access_granted, error_message

from mongoengine.errors import DoesNotExist
from database.models import Skill, User
from database.db import update_payload
from database.utilities import db_key_to_field_name


from utils.middle import paginate


class SkillApi(Resource):

    def get(self, name):
        """
        Retrieve one skill by its name
        ---
        tags:
            - skills
        parameters:
            - name: name
              in: path
              required: true
              type: string
              description: "The skill's name"
        definitions:
            error:
                type: object
                properties:
                    message:
                        type: string
                        description: "The error cause"
        responses:
            200:
                schema:
                    $ref: '#/definitions/skill'
            404:
                schema:
                    $ref: '#/definitions/error'
        """
        try:
            print(f"get {name}")
            skill = Skill.objects.get(name=name).to_json(use_db_field=False)
            return Response(skill,  mimetype="application/json", status=200)
        except DoesNotExist as donot:
            return Response(dumps({"message": f"'{name}' not found"}), mimetype="application/json", status=404)

    @jwt_required
    def put(self, name):
        """
        Update a skill
        ---
        tags:
            - skills
        security:
            - BearerAuth: []
        parameters:
            - name: name
              in: path
              type: string
              description: "The skill to update name"
            - name: Authorization
              in: header
              type: string
              description: "'Bearer JWT' value"
            - name: body
              in: body
              schema:
                $ref: '#/definitions/dateless_skill'
        definitions:
            dateless_skill:
                type: object
                properties:
                    name:
                        type: string
                        required: true
                    uni_name:
                        type: string
                        required: false
                        description: 'the unaccented name. It will be the base name'
                    domaines:
                        type: array
                        required: true
                        items:
                            $ref: '#/definitions/domaine'
                    description:
                        type: string
                        required: true
                    category:
                        type: string
                        enum: ["general", "specialisation", "don"]
                        required: true
                    optional_category:
                        type: object
        """
        try:
            access, status = is_access_granted(get_jwt_identity(), get_jwt_claims(), level=["Writer"])
            if access:
                skill = Skill.objects.get(uni_name=name)
                req = request.get_json()
                if "uni_name" in req:
                    req.pop("uni_name")
                req = update_payload(req)
                skill.update(**req)
                return Response(dumps({"name": name, "message": "Skill updated"}),
                                mimetype="application/json",
                                status=200)
            else:
                return Response(dumps({"name": name,
                                       "message": "Update forbidden"}),
                                mimetype="application/json",
                                status=status)
        except DoesNotExist as done:
            return error_message("Skill to update not found", 404)


class SkillsApi(Resource):
    def get(self):
        """
        Retrieve all skills
        ---
        tags:
            - skills
        parameters:
            - name: page
              in: query
              required: false
              type: integer
            - name: per_page
              in: query
              required: false
              type: integer
        definitions:
            skills:
                type: array
                items:
                    $ref: '#/definitions/skill'
            skill:
                type: object
                properties:
                    name:
                        type: string
                        required: true
                    uni_name:
                        type: string
                        required: false
                        description: 'the unaccented name. It will be the base name'
                    domaines:
                        type: array
                        required: true
                        items:
                            $ref: '#/definitions/domaine'
                    description:
                        type: string
                        required: true
                    category:
                        type: string
                        enum: ["general", "specialisation", "don"]
                        required: true
                    optional_category:
                        type: object
                    creation_date:
                        $ref: '#/definitions/date'
                        required: true
                    update_date:
                        $ref: '#/definitions/date'
                        required: true
            domaine:
                type: string
                enum: ["basique", "arts et artisanats", "sciences du combat", "developpement corporel", "sciences et humanités", "occulte et religions", "sciences et techniques", "don"]
            date:
                type: object
                properties:
                    $date:
                        type: integer
                        comment: date timestamp rounded to the millisecond
        responses:
            200:
                descriptions: "The full list of skills"
                schema:
                    $ref: '#/definitions/skills'

        """
        # TODO check this. Please mind that 0 is a falsy value
        page = int(request.args.get('page')) if request.args.get('page') else None
        per_page = int(request.args.get('per_page')) if request.args.get('per_page') else None
        query = paginate(page, per_page, Skill, "+uni_name")
        query = db_key_to_field_name(query, "uni_name")
        query = dumps(query)
        return Response(query, mimetype="application/json", status=200)

    @jwt_required
    def post(self):
        """
        Create a new skill
        ---
        tags:
            - skills
        security:
            - BearerAuth: []
        parameters:
            - name: Authorization
              in: header
              type: string
              description: "'Bearer JWT' value"
            - name: body
              in: body
              schema:
                $ref: '#/definitions/skill'
        responses:
            200:
                schema:
                    $ref: '#/definitions/skill'
        """
        pass


def initialize_skills():
    if Skill.objects().count():
        Skill.drop_collection()
    with open("skills.json") as file:
        skills = load(file)
        add = list()
        for skill in skills:
            print(skill["name"])
            skill["uni_name"] = unidecode.unidecode(skill["name"])
            skill = update_payload(skill, True)
            Skill(**skill).update(**skill, upsert=True)
