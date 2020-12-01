from flask_mongoengine import MongoEngine
from datetime import datetime

db = MongoEngine()


def initialize_db(app):
    db.init_app(app)


def update_payload(payload: dict, is_create: bool = False) -> dict:
    if is_create:
        payload["creation_date"] = datetime.utcnow()

    payload["update_date"] = datetime.utcnow()
    return payload
