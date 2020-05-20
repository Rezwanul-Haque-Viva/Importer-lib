import json
import logging

import requests
from requests.auth import HTTPBasicAuth

from importerlibs.utils.constants import Constants

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Request:
    def __init__(self, config=None):
        self._config = config

    def get_request(self, url, params):
        authentication = HTTPBasicAuth(self._config.ONET_USER_NAME, self._config.ONET_PASSWORD)
        header_accept = Constants.HEADER_ACCEPT_JSON

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
    def pagination(first, batch_size, total):
        for start in range(first, total + 1, batch_size):
            end = start + batch_size - 1
            if end > total:
                end = total
            params = {"start": start, "end": end}
            yield params

    def fetch_paginated_list(self, url, data_key, batch_size, params=None):
        if params is None:
            params = {}

        res_dict = self.get_request(url, params)
        if res_dict is None:
            yield []
        else:
            yield res_dict[data_key]

        end = int(res_dict['end'])
        total = int(res_dict['total'])

        for page_params in self.__class__.pagination(end + 1, batch_size, total):
            params.update(page_params)

            res_dict = self.get_request(url, params)
            if res_dict is None:
                yield []
            else:
                yield res_dict[data_key]

            logger.info(f"{params['end']} of {total} items imported")
            if not self._config.FULL_DATA_MODE:
                break
