from json import loads, dumps
from math import ceil
from datetime import datetime

from flask import Response

from database.models import Session, User
from logging import getLogger

log = getLogger(__name__)


def paginate(page, per_page, db_collection, order=None) -> dict:
    max_object = db_collection.objects.count()
    if page is not None and per_page is not None:
        if ceil(max_object / per_page) >= page:
            log.warning(f"Count: {max_object}, limit {per_page}, skip {(page-1)*per_page}")
            query = db_collection.objects.order_by(order).limit(per_page).skip((page-1)*per_page)
            # [(page - 1) * per_page: page * per_page]
            # query = query
            return loads(query.to_json())
        else:
            query = db_collection.objects().order_by(order)
            query = query[max_object - per_page:]
            return loads(query.to_json())
    else:
        query = db_collection.objects().order_by(order)
        return loads(query.to_json())


def error_message(message, status_code):
    if isinstance(message, dict):
        return Response(dumps(message), mimetype="application/json", status=status_code)
    else:
        return Response(dumps({"message": message}), mimetype="application/json", status=status_code)


def is_access_granted(user_id, claims, level=("Player",)):
    user_uuid = claims["hash"]
    log.warning(f"user uuid {user_uuid}")
    user_session = Session.objects(user_hash=user_uuid)
    log.warning(f"user session {user_session}")
    if user_session:
        user_session.update(logged=datetime.utcnow())
    else:
        return False, 401

    user = User.objects.get(id=user_id)
    if user.role in level:
        return True, 200
    else:
        return False, 403
