from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from json import load, dumps

from database.models import Culture, User


class CultureApi(Resource):

    def get(self, name):
        print(f"get {name}")
        skill = Culture.objects.get(name=name).to_json()
        return Response(skill,  mimetype="application/json", status=200)


class CulturesApi(Resource):
    def get(self):
        query = Culture.objects()
        return Response(query.to_json(), mimetype="application/json", status=200)


def initialize_cultures():
    with open("cultures.json") as file:
        cultures = load(file)
        for culture in cultures:
            print(culture["name"])
            Culture(**culture).update(**culture, upsert=True)
