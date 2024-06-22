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

    @request(rtype=HTTPVerbs.POST, path_regex=r'^/$')
    def register(self, request_handler):
        try:
            try:
                content_length = int(request_handler.headers.get('Content-Length'))
                body = json.loads(request_handler.rfile.read(content_length))

            except BaseException as e:
                raise ServiceException(400, f'Bad request: {e}')

            service.register(body)
            send_response(request_handler, json.dumps({'ok': 1}))

        except ServiceException as e:
            send_error_response(self.logger, request_handler, e)
