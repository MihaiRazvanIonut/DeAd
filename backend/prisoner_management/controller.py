import json
import logging

import service
from controller_utils import *
from exceptions import ServiceException
from http_verbs import *


class Controller:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

    @request(rtype=HTTPVerbs.GET, path_regex=f"/{PathRegEx.ID_REGEX}")
    def get_prisoner(self, request_handler):
        try:
            prisoner_id = get_id_from_path(request_handler.path)
            response = service.get_prisoner(prisoner_id)

            send_response(request_handler, json.dumps(response))

        except ServiceException as e:
            send_response(request_handler, e.message, e.status_code, [("Content-type", "text/html")])
            self.logger.error(f"Error encountered: {e.message}")
