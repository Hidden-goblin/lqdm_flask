from json import loads
from math import ceil


def paginate(page, per_page, db_collection) -> dict:
    max_object = db_collection.objects.count()
    if page is not None and per_page is not None:
        if ceil(max_object / per_page) <= page:
            query = db_collection.objects[(page - 1) * per_page: page * per_page]
            return loads(query.to_json())
        else:
            query = db_collection.objects[max_object - per_page:]
            return loads(query.to_json())
    else:
        query = db_collection.objects[0:]
        return loads(query.to_json())
