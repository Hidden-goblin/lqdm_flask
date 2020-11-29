from flask_mongoengine import MongoEngine
from datetime import datetime

db = MongoEngine()


def initialize_db(app):
    db.init_app(app)


def update_payload(payload: dict) -> dict:
    payload["update_date"] = datetime.utcnow()
    return payload
