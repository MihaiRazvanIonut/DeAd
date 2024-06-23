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

    @request(rtype=HTTPVerbs.GET, path_regex=f"^/{PathRegEx.ID_REGEX}$")
    def get_visit(self, request_handler):
        try:
            visit_id = get_id_from_path(request_handler.path)
            response = service.get_visit(visit_id)

            send_response(request_handler, json.dumps(response))

        except ServiceException as e:
            send_error_response(self.logger, request_handler, e)

    @request(rtype=HTTPVerbs.PUT, path_regex=f"^/{PathRegEx.ID_REGEX}$")
    def update_visit(self, request_handler):
        try:
            visit_id = get_id_from_path(request_handler.path)
            try:
                user_id = request_handler.headers.get('x-user-id')
                content_length = int(request_handler.headers.get('Content-Length'))
                body = json.loads(request_handler.rfile.read(content_length))

            except BaseException as e:
                raise ServiceException(400, f'Bad request: {e}')

            service.update_visit(visit_id, user_id, body)
            send_response(request_handler, json.dumps({'ok': 1}))

        except ServiceException as e:
            send_error_response(self.logger, request_handler, e)

    @request(rtype=HTTPVerbs.POST, path_regex=f"^/$")
    def new_visit(self, request_handler):
        try:
            try:
                user_id = request_handler.headers.get('x-user-id')
                content_length = int(request_handler.headers.get('Content-Length'))
                body = json.loads(request_handler.rfile.read(content_length))

            except BaseException as e:
                raise ServiceException(400, f'Bad request: {e}')

            new_resource_url = service.new_visit(user_id, body)
            send_response(request_handler, new_resource_url, 201, [("Content-type", "text/uri-list")])

        except ServiceException as e:
            send_error_response(self.logger, request_handler, e)

    @request(rtype=HTTPVerbs.GET, path_regex=f"^/{PathRegEx.QUERY_REGEX}$")
    def get_visits_search(self, request_handler):
        try:
            try:
                query_params = get_query_params_from_path(request_handler.path)
                query_params[query_params['field']] = query_params['value']
                query_params.pop('field')
                query_params.pop('value')

            except BaseException:
                raise ServiceException(400, 'Bad request: invalid query params')

            visits = service.get_visit_search(query_params)
            send_response(request_handler, json.dumps(visits), 200)
        except ServiceException as e:
            send_error_response(self.logger, request_handler, e)

    @request(rtype=HTTPVerbs.GET, path_regex='^/$')
    def get_visits(self, request_handler):
        try:
            visits = service.get_visits()
            send_response(request_handler, json.dumps(visits), 200)
        except ServiceException as e:
            send_error_response(self.logger, request_handler, e)
