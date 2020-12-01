from json import load, dumps

from flask import Response
from flask_restful import Resource

from database.models import Childhood
from database.db import update_payload


class ChildhoodAPI(Resource):
    def get(self, name):
        childhood = Childhood.objects.get(name=name).to_json()
        return Response(response=childhood, status=200, content_type="application/json")


class ChildhoodsApiList(Resource):
    def get(self):
        """
        Retrieve all existing childhoods
        ---
        tags:
            - childhood
        definitions:
            childhoods_name:
                type: array
                items:
                    $ref: '#/definitions/basic-ref'
        responses:
            200:
                description: "The list of childhood'names"
                schema:
                    $ref: '#/definitions/childhoods_name'
        """
        childhoods = Childhood.objects.only("name")
        names = [item["name"] for item in childhoods]
        return Response(response=dumps(names), status=200)


class ChildhoodsApiFull(Resource):
    def get(self):
        """
        Retrieve all childhoods data
        ---
        tags:
            - childhood
        definitions:
            childhoods:
                type: array
                items:
                    $ref: '#/definitions/childhood'
            childhood:
                type: object
                properties:
                    name:
                        type: string
                        required: true
                    description:
                        type: string
                        required: true
                    innate:
                        type: array
                        items:
                            $ref: '#/definitions/basic-ref'
            basic-ref:
                type: string

        responses:
            200:
                description: "The childhoods full data"
                schema:
                    $ref: '#/definitions/childhoods'

        """

        childhoods = Childhood.objects().to_json()
        return Response(response=childhoods, status=200)


def initialize_childhood():
    with open("childhood.json") as file:
        childhoods = load(file)
        for childhood in childhoods:
            print(childhood["name"])
            childhood = update_payload(childhood, True)
            Childhood(**childhood).update(**childhood, upsert=True)
