import json

import sqids

import service
from controller_utils import *
from exceptions import ServiceException
from http_verbs import *

short_id = sqids.Sqids(min_length=8)


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
            send_error_response(self.logger, request_handler, e)

    @request(rtype=HTTPVerbs.PUT, path_regex=f"{PathRegEx.ID_REGEX}")
    def update_prisoner(self, request_handler):
        try:
            prisoner_id = get_id_from_path(request_handler.path)
            try:
                content_length = int(request_handler.headers.get('Content-Length'))
                body = json.loads(request_handler.rfile.read(content_length))

            except BaseException as e:
                raise ServiceException(400, f'Bad request: {e}')

            service.update_prisoner(prisoner_id, body)
            send_response(request_handler, '')

        except ServiceException as e:
            send_error_response(self.logger, request_handler, e)

    @request(rtype=HTTPVerbs.POST, path_regex=f"")
    def new_prisoner(self, request_handler):
        try:
            try:
                content_length = int(request_handler.headers.get('Content-Length'))
                body = json.loads(request_handler.rfile.read(content_length))

            except BaseException as e:
                raise ServiceException(400, f'Bad request: {e}')

            new_resource_url = service.new_prisoner(body)
            send_response(request_handler, new_resource_url, 201, [("Content-type", "text/uri-list")])

        except ServiceException as e:
            send_error_response(self.logger, request_handler, e)

    @request(rtype=HTTPVerbs.GET, path_regex=f"{PathRegEx.QUERY_REGEX}")
    def get_prisoners(self, request_handler):
        pass
