from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from database.db import initialize_db
from resources.childhood import initialize_childhood
from resources.routes import initialize_routes
from resources.skills import initialize_skills
from resources.cultures import initialize_cultures
from resources.auth import initialize_users
from dotenv import load_dotenv
from flasgger import Swagger
import os

from utils.errors import schema_error


def create():
    load_dotenv()

    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    #app.config["host"] = os.getenv("BACKEND_HOST")
    # app.config.from_envvar('ENV_FILE_LOCATION')
    # app.config['SWAGGER'] = {
    #     'openapi': '3.0.2',
    #     'uiversion': 3
    # }
    api = Api(app)

    app.config['MONGODB_SETTINGS'] = {
        'host': 'db',
        'db': 'lqdm',
        'port': 27017,
        'username': "lqdm",
        'password': "lqdm",
        'authentication_source': "lqdm"
    }

    swagger_template = {
        "info": {
            "title": "LQDM API",
            "description": "LQDM characters management.",
            "contact": {
                "responsibleOrganization": "ME",
                "responsibleDeveloper": "Me",
                "email": "me@me.com",
                "url": "www.me.com",
            },
            # "termsOfService": "http://me.com/terms",
            "version": "0.1"
        },
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "in": "header",
                }
            }
        }
    }
    swagger = Swagger(app, template=swagger_template, validation_error_handler=schema_error)

    jwt = JWTManager(app)
    initialize_db(app)
    initialize_routes(api)
    initialize_skills()
    initialize_cultures()
    initialize_childhood()
    initialize_users()

    return app
# app.run(host="0.0.0.0")

