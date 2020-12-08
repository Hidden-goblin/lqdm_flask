# -*- coding:utf8 -*-
import logging
import os
import re

from shutil import rmtree, copytree
from logging import getLogger
from json import dumps, load, JSONDecodeError
from behave.model_core import Status
from requests.models import Response
from .common_helpers import string_to_bool

log = getLogger(__name__)

"""
Generic functions applicable to all 'environment.py'. Ease the creation of before/after step
"""


def set_logger(log_name: str, is_debug: bool = False):
    logging.basicConfig(level=logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s -- %(filename)s.%(funcName)s-- %(levelname)s -- %(message)s")
    handler = logging.FileHandler(f"{log_name}_log.log", mode="w", encoding="utf-8")
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    logging.getLogger("behave").setLevel(level=logging.WARNING)
    logging.getLogger("xmlschema").setLevel(level=logging.WARNING)
    logging.getLogger("jsonschema").setLevel(level=logging.WARNING)
    logging.getLogger("dpath").setLevel(level=logging.WARNING)
    logging.getLogger("parse").setLevel(level=logging.WARNING)
    logging.getLogger("resquests").setLevel(level=logging.WARNING)
    logging.getLogger("urllib3").setLevel(level=logging.WARNING)
    if is_debug:
        logging.getLogger("models").setLevel(logging.DEBUG)
        logging.getLogger("builtins").setLevel(logging.DEBUG)
        logging.getLogger("common_steps").setLevel(logging.DEBUG)
        logging.getLogger("ctwformatter").setLevel(logging.DEBUG)
    else:
        logging.getLogger("models").setLevel(logging.WARNING)
        logging.getLogger("builtins").setLevel(logging.WARNING)
        logging.getLogger("common_steps").setLevel(logging.WARNING)
        logging.getLogger("ctwformatter").setLevel(logging.WARNING)


def folder_file_name_cleaning(name: str) -> str:
    """
    Clean the name from spaces and special characters
    :param name: the name to clean
    :return: a string
    """
    return name.replace(" ", "_").replace(",", "_").replace("'", "_").replace("@", "-")


def create_evidence(scenario, history):
    """Build the evidence file for the 'scenario' and the 'history' of actions"""
    evidence_folder = f"evidence/{folder_file_name_cleaning(scenario.feature.name)}"
    log.debug(f"evidence folder {evidence_folder}")
    os.makedirs(evidence_folder, exist_ok=True)
    sc_name = folder_file_name_cleaning(str(scenario.name))

    with open(f"{evidence_folder}/{sc_name}-{scenario.status}.txt",
              "w", encoding="utf-8") as file:
        # Evidence title and status
        file.write(f"Evidence for scenario {scenario.name}\n\n")
        file.write(f"Scenario {scenario.status}\n\n")
        # Add the skip reason
        # TODO add the failure reason??
        if scenario.status is not Status.passed:
            file.write(f"\t Reason: {scenario.skip_reason}\n\n")

        # Evidence history writing
        for event in history:
            # Event is composed of 'step' object and object
            # Write the 'step' data. This is retrieved from feature files
            file.write(f"{event[0].keyword} {event[0].name}\n")
            # Write the data related to the step
            if isinstance(event[1], list):
                for req in event[1]:
                    response_to_evidence(file, req)
            else:
                response_to_evidence(file, event[1])


def request_response_to_evidence(file, response):
    file.write(f"Request:\n \t Method: {response.request.method}")
    file.write(f"\n\t Url: {response.request.url}")
    file.write(f"\n\t Headers: {response.request.headers}")
    if response.request.method == 'POST':
        file.write(f"\n\t Body: {response.request.body}")
    file.write(f"\n\n Response: \n\t Status: {response.status_code}")
    file.write(f"\n\t Response Time: {response.elapsed.total_seconds()} second")
    try:
        file.write(f"\n\t Content: \n {dumps(response.json(), indent=4)}")
    except JSONDecodeError:
        # TODO look if xml pretty print is needed here
        file.write(f"\n\t Content: \n {response.text}")


def response_to_evidence(file, response):
    """Write the data to the file depending the type of the data"""
    try:
        # the data are a Requests's Response object
        if isinstance(response, Response):
            request_response_to_evidence(file, response)
        # write the dictionary as a key/value list
        elif isinstance(response, dict):
            file.write("Data:")
            for key, value in response.items():
                if isinstance(value, Response):
                    file.write(f"\n\t {key}:\n")
                    request_response_to_evidence(file, value)
                else:
                    file.write(f"\n\t {key}: {str(value)}")
            file.write("\n")
        # write data with no formatting
        else:
            file.write(f"Raw Data:\n {response}\n")
        file.write("\n\n\n")
    except Exception as exception:
        log.error(f"Get the following error when creating the evidence\n {exception.args}")


def make_evidence_rotation(max_keep: int):
    """
    Delete the oldest and make the rotation
    :param max_keep: the max number of evidence to keep i.e. 0 is no conservation , 1 is keep one
    :return:
    """
    try:

        def increase_number(folder):
            folder_name, number = re.search("([a-zA-Z]*)([0-9]*)", folder).groups()
            return f"{folder_name}{int(number) + 1}"

        if max_keep != 0:
            folders = [f for f in os.listdir("")
                       if os.path.isdir(os.path.join("", f))
                       and re.match(r"^evidence[0-9]+$", f)
                       and int(re.search("evidence([0-9]+)", f).groups()[0]) <= max_keep]
            folders.reverse()
            # last = max([int(item.replace("evidence", "")) for item in folders if folders])
            process = [(folder, increase_number(folder)) for folder in folders
                       if folder != f"evidence{max_keep}"]

            for evidence in process:
                rmtree(evidence[1], ignore_errors=True)
                copytree(evidence[0], evidence[1])
            rmtree("evidence1", ignore_errors=True)
            if os.path.exists("evidence") and os.path.isdir("evidence"):
                log.debug("evidence folder exists")
                copytree("evidence", "evidence1")
            elif os.path.exists("evidence") and not os.path.isdir("evidence"):
                log.debug("evidence exists and is not a folder. Try to delete")
                os.remove("evidence")
            else:
                log.warning("No evidence folder")
    except Exception as exception:
        log.error(f"Passing the evidence rotation. Receive error message {exception.args[0]}")


def request_list_saving(context, scenario, filename: str = "requests.txt"):
    """
    Save requests to file
    :param context: the behave context object
    :param scenario: the behave scenario object
    :param filename: the file filename where to save the request defaulted to "requests.txt"
    :return: None
    """
    with open(filename, "a+") as file:
        if context.response is not None and isinstance(context.response, Response):
            file.write(f"Request for {scenario.name}:\n \t"
                       f" Method: {context.response.request.method}")
            file.write(f"\n Url: {context.response.request.url}")
            file.write(f"\n Headers: {context.response.request.headers}\n")
            if context.response.request.method == 'POST':
                file.write(f"\n Body: {context.response.request.body}\n")


def common_before_all(context, model: object, is_data_load: bool = False):
    """
    Retrieve the environment & schemas for the run.
    Set the model to use for the run.
    Load specific data if needed
    :param context: the magic variable context
    :param model: the models version-model to use for the run
    :param is_data_load: flag to load data or not. Default is False
    :return: none
    """
    # Set logging
    set_logger("api",
               string_to_bool(context.config.userdata["modeDebug"]))

    # Load environments
    log.debug("Start loading environment")
    # Load model
    context.model = model(context.config.userdata["url"])

    # Load data
    # and api != 'journey_planner'
    if is_data_load:
        with open(context.data_filename, encoding="utf-8") as data:
            context.data = load(data)
    else:
        context.data = None

    # Evidence folder handling
    log.debug("Before evidence")
    if os.path.exists("evidence"):
        make_evidence_rotation(3)
        rmtree("evidence")
    os.makedirs("evidence", exist_ok=True)


def common_after_all(context):
    """Add the data used in the test to the evidence folder. It's a raw data"""
    log.debug("AfterALL")
    if context.data:
        with open("evidence/static_data_used_in_run.txt", "w", encoding="utf-8") as file:
            file.write(dumps(context.data, ensure_ascii=False, indent=2))
