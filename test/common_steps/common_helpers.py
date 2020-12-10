# -*- coding:utf8 -*-
import base64


def common_exception(context, exception):
    """
    To be used in the 'except' clause of step definition.
    Raise an exception after adding the message into the history for evidence creation.
    :param context: the behave context object
    :param exception: the exception object
    :return: None
    :raise Exception: re-raise the received exception.
    """
    context.model.push_event(f"Exception raised: {exception.args[0]}")
    raise Exception(exception)


def most_recent(version1, version2):
    """
    Returns the most recent version between two versions given (format: 'x.y.z...' where x, y, z
    are int)
    :param version1: a string
    :param version2: a string
    :return: the most recent version
    """
    list_version1 = version1.split(".")
    list_version2 = version2.split(".")
    diff_size = len(list_version1) - len(list_version2)
    if diff_size == 0:
        for index, value in enumerate(list_version1):
            if int(value) > int(list_version2[index]):
                return True
            elif int(value) < int(list_version2[index]):
                return False
            else:
                pass
    elif diff_size > 0:
        list_version2.extend(["0"] * diff_size)
        return most_recent(version1, ".".join(list_version2))
    else:
        list_version1.extend(["0"] * -diff_size)
        return most_recent(".".join(list_version1), version2)


def last_version(versions_list):
    """
    Returns the last version among a list of versions (strings as seen in the function above)
    :param versions_list: a list of versions
    :return: the most recent version
    """
    last = versions_list[0]
    for version in versions_list:
        if most_recent(version, last):
            last = version
    return last


def string_to_bool(input_string: str) -> bool:
    if input_string.casefold() == 'True'.casefold():
        return True
    elif input_string.casefold() == 'False'.casefold():
        return False
    else:
        raise ValueError(f"Cannot convert {input_string} to a boolean."
                         f" Expecting only True or False")


def credentials_concat(username, password):
    """
    To use for creating Authorization header
    :param username: username to concatenate
    :param password: password to concatenate
    :return: concatenated credentials
    """
    concat_string = username + ":" + password
    return concat_string


def base_64_encoder(string_to_encode):
    """
    To use for encoding a string in Base64
    :param string_to_encode: string to be encoded
    :return: string encoded in Base64
    """
    string_bytes = string_to_encode.encode("ascii")
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string
