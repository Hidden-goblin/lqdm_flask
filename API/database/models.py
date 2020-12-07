from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime


class Session(db.Document):
    logged = db.DateTimeField(default=datetime.utcnow)
    user_hash = db.StringField(required=True)
    meta = {
        'indexes': [
            {'fields': ['logged'], 'expireAfterSeconds': 120}
        ]
    }


class Skill(db.Document):
    name = db.StringField(required=True)
    uni_name = db.StringField(required=True, primary_key=True)
    domaines = db.ListField(db.StringField(choices=["basique",
                                                    "arts et artisanats",
                                                    "sciences du combat",
                                                    "developpement corporel",
                                                    "sciences et humanités",
                                                    "occulte et religions",
                                                    "sciences et techniques",
                                                    "don"]), required=True)
    description = db.StringField(required=True)
    category = db.StringField(choices=["general", "specialisation", "don", "passion"], required=True)
    creation_date = db.DateTimeField(default=datetime.utcnow, db_field="creation_date")
    update_date = db.DateTimeField(default=datetime.utcnow, db_field="update_date")
    optional_mechanism = db.DynamicField()


class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    role = db.StringField(choices=("Admin", "GM", "Player", "Writer"), default="Player")
    creation_date = db.DateTimeField(default=datetime.utcnow)
    update_date = db.DateTimeField(default=datetime.utcnow)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def get_roles():
        return "Admin", "GM", "Player", "Writer"


class Culture(db.Document):
    name = db.StringField(required=True, primary_key=True)
    description = db.StringField(required=True)
    gabarit = db.IntField(required=True)
    innate = db.ListField(db.StringField(), required=True)
    gift = db.ListField(db.StringField())
    creation_date = db.DateTimeField(default=datetime.utcnow)
    update_date = db.DateTimeField(default=datetime.utcnow)


class Childhood(db.Document):
    name = db.StringField(required=True, primary_key=True)
    description = db.StringField(required=True)
    innate = db.ListField(db.StringField(), required=True)
    creation_date = db.DateTimeField(default=datetime.utcnow)
    update_date = db.DateTimeField(default=datetime.utcnow)


class Career(db.Document):
    name = db.StringField(required=True, primary_key=True)
    description = db.StringField(required=True)
    skills = db.ListField(db.StringField(), required=True)
    domaine = db.StringField(required=True)
    dotation = db.ListField(db.StringField())
    creation_date = db.DateTimeField(default=datetime.utcnow)
    update_date = db.DateTimeField(default=datetime.utcnow)


class Character(db.Document):
    pass
