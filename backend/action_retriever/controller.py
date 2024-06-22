import json

import service
from controller_utils import *
from exceptions import ServiceException
from http_verbs import *


class Controller:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

    @request(rtype=HTTPVerbs.GET, path_regex=f'^/$')
    def get_actions(self, request_handler):
        try:
            actions = service.get_actions()
            send_response(request_handler, json.dumps(actions))

        except ServiceException as e:
            send_error_response(self.logger, request_handler, e)

    @request(rtype=HTTPVerbs.GET, path_regex=f'^/{PathRegEx.ID_REGEX}$')
    def get_user_actions(self, request_handler):
        try:
            user_id = get_id_from_path(request_handler.path)
            actions = service.get_user_actions(user_id)

            send_response(request_handler, json.dumps(actions))
        except ServiceException as e:
            send_error_response(self.logger, request_handler, e)
