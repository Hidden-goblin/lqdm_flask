#
from copy import deepcopy


def id_to_name(payload):
    if isinstance(payload, dict):
        element = deepcopy(payload)
        if "_id" in element:
            element["name"] = element.pop("_id")
        return element
    elif isinstance(payload, list):
        return_list = list()
        for item in payload:
            return_list.append(id_to_name(item))
        return return_list
    else:
        return payload
