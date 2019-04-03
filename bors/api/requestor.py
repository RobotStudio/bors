"""A requestor framework"""

import requests

from bors.common.singleton import Singleton
from bors.app import logger


class Req(metaclass=Singleton):
    """A requests adapter to take advantage of pooling features"""
    def __init__(self, url_base, payload, log):
        self.url_base = url_base
        self.payload = payload
        self.log = log
        self.session = requests.Session()

    def get_req_obj(self):
        """Return a requests implementation"""
        return self.session

    def call(self, callname, data=None, **args):
        """
        Generic interface to REST apiGeneric interface to REST api
        :param callname:  query name
        :param data:   dictionary of inputs
        :param args:    keyword arguments added to the payload
        :return:
        """
        url = f"{self.url_base}/{callname}"
        payload = self.payload.copy()
        payload.update(**args)

        if data is not None:
            payload.update(data)

        res = self.session.post(url, data=payload)

        if res.status_code > 299:
            logger.error(f"URL: {url}")
            logger.error(f"Payload: {payload}")
            logger.error(f"STATUS: {res.status_code}")
            logger.error(f"RESPONSE: {res.text}")
            return
        elif 'error' in res.json():
            logger.error(res.json()['error'])
            return

        return res.json()
