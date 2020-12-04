# -*- coding:utf8 -*-
import logging

from datetime import date, datetime
from time import altzone

log = logging.getLogger(__name__)


class ApiAbstraction:
    """Base class of all APIs
    Provide the default mechanism for handling url, lang, step and history of call
    """

    def __init__(self, url):
        self.__url = url
        self.__step = None
        self.__history = list()

    @property
    def url(self):
        return self.__url

    @property
    def step(self):
        return self.__step

    @step.setter
    def step(self, step):
        self.__step = step

    @property
    def history(self):
        return self.__history

    @history.setter
    def history(self, event):
        self.__history.append(event)

    def history_reset(self):
        self.__history = list()

    def push_event(self, event):
        self.history = (self.step, event)


class DateHelper:
    """Provide some date tools in order to ease the request building"""
    @staticmethod
    def current_date(returned_format: str = "%Y-%m-%d"):
        """Returns today as string %Y-%m-%d"""
        return date.today().strftime(returned_format)

    @staticmethod
    def current_date_time(returned_format: str = "%Y-%m-%dT%H:%M:%S"):
        """Returns now as string %Y-%m-%dT%H:%M:%S using datime"""
        return datetime.today().strftime(returned_format)

    @staticmethod
    def current_date_time_effective(returned_format: str = "%Y-%m-%dT%H:%M:%S"):
        """Returns now as string %Y-%m-%dT%H:%M:%S using date"""
        return date.today().strftime(returned_format)

    @staticmethod
    def date_date(date_string, input_format: str = "%Y-%m-%d") -> datetime:
        """Returns datetime from date string"""
        return datetime.strptime(date_string, input_format)

    @staticmethod
    def date_date_time(date_time_string, input_format: str = "%Y-%m-%dT%H:%M:%S") -> datetime:
        """Returns datetime from date & time string"""
        return datetime.strptime(date_time_string, input_format)

    @staticmethod
    def convert_date_format(date_time_string: str, input_format: str, output_format: str) -> str:
        """
        Convert a date time in a string format to another
        :param date_time_string: date_time as a string
        :param input_format: string date format input
        :param output_format: string date format output
        :return: a string with the requested format
        """
        temp_date = DateHelper.__to_datetime(date_string=date_time_string,
                                             date_format=input_format)
        return temp_date.strftime(output_format)

    @staticmethod
    def __to_datetime(date_string, date_format) -> datetime:
        """Convert a date as a string to a date_time using in package methods.
        Handle the situation where the date is a date & time format.
        """
        try:
            result = None
            log.debug("one")
            result = DateHelper.date_date(date_string, date_format)
            log.debug("two")
        except Exception as exception:
            log.warning(f"DateHelper.date_date raise {exception.args[0]}")
            result = DateHelper.date_date_time(date_string, date_format)
        finally:
            log.debug("In finally clause")
            return result

    @staticmethod
    def json_date_time(date_datetime: datetime = None,
                       date_string: str = None,
                       date_formats: list = None) -> str:
        """
        Capture a date or date-time and return a Json date
        ref https://stackoverflow.com/questions/5786448/date-conversion-net-json-to-iso

        :param date_datetime: a datetime date to convert to ASP.NET JSon Date
        :param date_string: a date as a string
        :param date_formats: a list of possible date format in order to convert to datetime
        :return str: an ASP.NET JSon Date \\/Date(time_from_epoc_in_ms+-hourminutes_time_zone)\\/
                     Please note that this notation is no longer used by Microsoft
        :raise AttributeError: where no datetime or no date strings and format are provided
        """
        if date_datetime is not None:
            local_time = int(date_datetime.timestamp() * 1000)
            hour_offset = abs(altzone) // 3600
            min_offset = (abs(altzone) - hour_offset * 3600) // 60
            hour_offset = str(hour_offset).zfill(2)
            if altzone < 0:
                hour_offset = f"-{hour_offset}"
            return "\\/Date({}{}{})\\/".format(local_time,
                                               hour_offset,
                                               str(min_offset).zfill(2))
        elif date_string is not None and date_formats is not None and date_formats:
            for date_format in date_formats:
                result = DateHelper.__to_datetime(date_string, date_format)
                if result is not None:
                    break
            return DateHelper.json_date_time(date_datetime=result)
        else:
            raise AttributeError("You must provide either a datetime or "
                                 "a date string and list of possible format")


def int_list_to_str_list(int_list: list) -> list:
    """
    Transform a list in a list of string

    :param int_list: the input list (formerly a list of int)
    :return: a list of string
    """
    return [str(item) for item in int_list]


def list_to_pipe_separated_list(input_list: list) -> str:
    """
    Transform a list in a string with pipe separated element
    :param input_list: the input list
    :return: a string
    """

    return "|".join(int_list_to_str_list(input_list))


def pipe_separated_list_to_list(input_list: str) -> list:
    """
    Transform a string to a list splitting on pipe symbol '|'
    :param input_list: the pipe separated list string
    :return: a list
    """
    return input_list.split("|")


def argument_unpack(arguments: dict, to_pop: list = None) -> dict:
    """Return the arguments in order to unpack them in method or function easily.

    Clean the dictionary from unneeded keys.

    To use where methods have a lot of argument.
    :param arguments: the argument dictionary often retrieved via locals() function
    :param to_pop: dictionary's key to pop in order to make the call valid. Defaulted to 'self'

    :return arguments as a dictionary
    """
    pop_list = ['self']
    if to_pop is not None:
        pop_list.extend(to_pop)
    return {item[0]: item[1] for item in arguments.items() if item[0] not in pop_list}


class NotInVersion(Exception):
    """Exception raised if the operation does not belong to the version

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super().__init__(message)


class NotSetInProject(Exception):
    """Exception raised if the operation is not meant to belong to this project
    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        super().__init__(message)
