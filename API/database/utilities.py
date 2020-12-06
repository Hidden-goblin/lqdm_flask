#
from copy import deepcopy


def db_key_to_field_name(payload, field_name):
    if isinstance(payload, dict):
        element = deepcopy(payload)
        if "_id" in element:
            element[field_name] = element.pop("_id")
        return element
    elif isinstance(payload, list):
        return_list = list()
        for item in payload:
            return_list.append(db_key_to_field_name(item, field_name))
        return return_list
    else:
        return payload
