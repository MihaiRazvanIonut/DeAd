import json

from controller_utils import *
from exceptions import ServiceException
from http_verbs import *
import service


class Controller:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

    @request(rtype=HTTPVerbs.GET, path_regex=f'^/{PathRegEx.UUID_REGEX}$')
    def get_user_id_from_session(self, request_handler):
        try:
            response = service.get_user_id_from_session(get_id_from_path(request_handler.path))
            send_response(request_handler, json.dumps(response))
        except ServiceException as e:
            send_error_response(self.logger, request_handler, e)
