# -*- coding: utf-8 -*-
import argparse
import logging
import os
import shutil
import sys
import webbrowser
import re
from behave.__main__ import main as behave_main


def run_once(behave_argument: list):
    """
    Run Behave once using the provided argument
    :param behave_argument:
    :return:
    """
    result = behave_main(behave_argument)
    with open('output.html', 'r+') as replace:
        text = replace.read()
        text = re.sub('&gt;', '>', text)
        text = re.sub('&lt;', '<', text)
        text = re.sub('&amp;', '&', text)
        replace.seek(0)
        replace.write(text)
        replace.truncate()
    shutil.copy("output.html", "evidence")
    return result


def prepare_behave_args(args):
    behave_arguments = [
                "-f",
                "html",
                "-ooutput.html",
                "--junit",
                "--junit-directory=junit_report",
                "-fplain",
                "-oplain_output.txt",
                "--no-capture",
                "--no-logcapture",
                "-D",
                f"url={args.environment}",
                f"./api_features",
                "-D",
                f"modeDebug={args.debug}",
            ]  # List of  behave arguments
    if args.tags:
        for tags in args.tags:
            behave_arguments.append("-t {}".format(",".join(tags)))
    return behave_arguments

def main():
    """
    Run behave with a log rolling.
    As default create output.html report, a plain text plain_output.txt and JUnit report files in
    junit_report folder.

    By default run in non debug mode.

    Controls the run behaviour using tags and other sets
    :return: 0 if everything is fine, 1 or number of Assertion Failed found in plain_output.txt
    """
    # Keeping the last execution log.
    if os.path.exists("test_log.log"):
        if os.path.exists("test_log_back.log"):
            os.remove("test_log_back.log")
        os.rename("test_log.log", "test_log_back.log")

    # Logger definition
    logging.basicConfig(level=logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s -- %(filename)s.%(funcName)s-- %(levelname)s -- %(message)s")
    handler = logging.FileHandler("test_log.log", mode="a", encoding="utf-8")
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logging.getLogger("xmlschema").setLevel(level=logging.WARNING)
    logging.getLogger("jsonschema").setLevel(level=logging.WARNING)
    logging.getLogger("dpath").setLevel(level=logging.WARNING)
    logging.getLogger("parse").setLevel(level=logging.WARNING)
    logging.getLogger("behave").setLevel(level=logging.WARNING)
    logging.getLogger("resquests").setLevel(level=logging.WARNING)
    logging.getLogger("urllib3").setLevel(level=logging.WARNING)

    logging.getLogger(__name__).debug("Main started")

    # Prepare run
    logging.getLogger(__name__).debug("Preparing run")
    # Get options from command line input
    parser = argparse.ArgumentParser()
    parser.add_argument("-e",
                        "--environment",
                        type=str,
                        help="The environment where to run the tests",
                        default='http://localhost:5000')
    parser.add_argument("-t",
                        "--tags",
                        type=str,
                        help="The scenario tags to run",
                        action="append",
                        nargs='+')
    # parser.add_argument("-a",
    #                     "--api",
    #                     type=str,
    #                     help="The API you want to test",
    #                     choices=api_list,
    #                     default="disrupt")
    parser.add_argument("--debug",
                        help="Set the logs to debug. Otherwise the logs are at warning level ",
                        action="store_true")
    parser.add_argument("--display",
                        help=("Display the html report after the "
                              "execution using the default browser"),
                        action="store_true")
    parser.add_argument("-v",
                        "--version",
                        type=str,
                        help="Set the version of the API you want to test")
    args = parser.parse_args()

    results = run_once(prepare_behave_args(args))

    if args.display:
        webbrowser.open_new_tab(f"file:///{os.getcwd()}/evidence/output.html")

    # Result management: return value is 0 if everything is fine
    # 1 or the number of 'Assertion Failed' found in the plain text output

    logger.info(f"End run  Retrieve '{results}' errors")

    sys.exit(results)


if __name__ == "__main__":
    main()
