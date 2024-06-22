import service
from controller_utils import *
from http_verbs import *


class Controller:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

    @request(rtype=HTTPVerbs.GET, path_regex=f'^/moods{PathRegEx.QUERY_REGEX}$')
    def get_moods(self, request_handler):
        try:
            query_params = get_query_params_from_path(request_handler.path)
            stats = service.get_moods(query_params)
            export_file(request_handler, stats, query_params['format'])

        except exceptions.ServiceException as e:
            send_error_response(self.logger, request_handler, e)

    @request(rtype=HTTPVerbs.GET, path_regex=f'^/moods/{PathRegEx.ID_REGEX}{PathRegEx.QUERY_REGEX}$')
    def get_mood(self, request_handler):
        try:
            query_params = get_query_params_from_path(request_handler.path)
            path_id = get_id_from_path(request_handler.path)
            stats = service.get_moods_specific(path_id, query_params)
            export_file(request_handler, stats, query_params['format'])

        except exceptions.ServiceException as e:
            send_error_response(self.logger, request_handler, e)

    @request(rtype=HTTPVerbs.GET, path_regex=f'^/items{PathRegEx.QUERY_REGEX}$')
    def get_items(self, request_handler):
        try:
            query_params = get_query_params_from_path(request_handler.path)
            stats = service.get_items(query_params)
            export_file(request_handler, stats, query_params['format'])

        except exceptions.ServiceException as e:
            send_error_response(self.logger, request_handler, e)

    @request(rtype=HTTPVerbs.GET, path_regex=f'^/items/{PathRegEx.ID_REGEX}{PathRegEx.QUERY_REGEX}$')
    def get_item(self, request_handler):
        try:
            query_params = get_query_params_from_path(request_handler.path)
            path_id = get_id_from_path(request_handler.path)
            stats = service.get_items_specific(path_id, query_params)
            export_file(request_handler, stats, query_params['format'])

        except exceptions.ServiceException as e:
            send_error_response(self.logger, request_handler, e)
