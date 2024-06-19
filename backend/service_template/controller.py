from controller_utils import *
from http_verbs import *


class Controller:

    @request(rtype=HTTPVerbs.GET, path_regex=r"")
    def hello_world(self, request_handler):
        send_response(request_handler, "{\"hello\": \"world!\"}")
