import json
import logging

import requests
from requests.auth import HTTPBasicAuth

from importerlibs.utils.constants import Constants

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Request:
    """
    Request Class to call GET, POST requests for importer
    """
    @staticmethod
    def get_request(url, params, **kwargs):
        """
        Send a GET request to target URL
        :param url: string
        :param params: dict
        :param kwargs: dict, expected kwargs {username: "", password:""} else None
        :return: dict
        """
        header_accept = Constants.HEADER_ACCEPT_JSON
        authentication = HTTPBasicAuth(kwargs.get("username", None), kwargs.get("password", None))

        try:
            response = requests.get(url,
                                    auth=authentication,
                                    headers=header_accept,
                                    params=params,
                                    timeout=(Constants.TIMEOUT_CONNECT, Constants.TIMEOUT_READ))

            if response.status_code != 200:
                logger.error(response.text)
                return

            res_dict = json.loads(response.text)
            return res_dict

        except Exception as e:
            logger.error("Error in requesting url: {} params: {}\n{}".format(url, params, str(e)))

    @staticmethod
    def post_request(url, data):
        """
        Send a POST request to target URL
        :param url: str
        :param data: dict
        :return: dict
        """
        header_accept = Constants.HEADER_ACCEPT_JSON

        try:
            response = requests.post(url,
                                     headers=header_accept,
                                     data=data,
                                     timeout=(Constants.TIMEOUT_CONNECT, Constants.TIMEOUT_READ))

            if response.status_code != 200:
                logger.error(response.text)
                return

            res_dict = json.loads(response.text)
            return res_dict

        except Exception as e:
            logger.error(f"Error in requesting url: {url}\n{str(e)}")

    @staticmethod
    def pagination(first, batch_size, total):
        """
        Generator for Pagination
        :param first: int
        :param batch_size: int
        :param total: int
        :return: dict
        """
        for start in range(first, total + 1, batch_size):
            end = start + batch_size - 1
            if end > total:
                end = total
            params = {"start": start, "end": end}
            yield params

    @classmethod
    def fetch_paginated_list(cls, url, data_key, batch_size, params=None):
        """
        Generator for fetching data from target url with pagination
        :param url: str
        :param data_key: str
        :param batch_size: int
        :param params: dict
        :return: list
        """
        if params is None:
            params = {}

        res_dict = cls.get_request(url, params)
        if res_dict is None:
            yield []
        else:
            yield res_dict[data_key]

        end = int(res_dict['end'])
        total = int(res_dict['total'])

        for page_params in cls.pagination(end + 1, batch_size, total):
            params.update(page_params)

            res_dict = cls.get_request(url, params)
            if res_dict is None:
                yield []
            else:
                yield res_dict[data_key]

            logger.info(f"{params['end']} of {total} items imported")
