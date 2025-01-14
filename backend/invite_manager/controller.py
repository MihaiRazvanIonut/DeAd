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

    @request(rtype=HTTPVerbs.POST, path_regex=f'^/{PathRegEx.QUERY_REGEX}$')
    def new_invite(self, request_handler):
        try:
            user_id = request_handler.headers.get('x-user-id')
            query_param = get_query_params_from_path(request_handler.path)
            new_invite = service.new_invite(user_id, query_param)

            send_response(request_handler, json.dumps(new_invite), 201)

        except ServiceException as e:
            send_error_response(self.logger, request_handler, e)

    @request(rtype=HTTPVerbs.GET, path_regex=f'^/{PathRegEx.ID_REGEX}$')
    def get_invites(self, request_handler):
        try:
            user_id = get_id_from_path(request_handler.path)
            invites = service.get_invites(user_id)

            send_response(request_handler, json.dumps(invites))

        except ServiceException as e:
            send_error_response(self.logger, request_handler, e)