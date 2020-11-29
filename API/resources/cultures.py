from flask import Response
from flask_restful import Resource
from json import load

from database.models import Culture


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
