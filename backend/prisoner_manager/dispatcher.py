import re
from http.server import BaseHTTPRequestHandler

from controller import Controller
from http_verbs import HTTPVerbs

controller = Controller()

request_mappings: dict[HTTPVerbs, dict] = {
    HTTPVerbs.GET: {},
    HTTPVerbs.POST: {},
    HTTPVerbs.PUT: {},
    HTTPVerbs.DELETE: {},
}


def load_controller_requests():
    for attr_name in dir(Controller)[::-1]:
        attr = getattr(Controller, attr_name)
        if callable(attr) and hasattr(attr, 'request_type') and hasattr(attr, 'path_regex'):
            request_mappings[attr.request_type][attr.path_regex] = attr


class Dispatcher(BaseHTTPRequestHandler):

    def __generic_request_mathing(self, request_type: HTTPVerbs):
        for path_regex, method in request_mappings[request_type].items():
            if re.search(path_regex, self.path):
                method(controller, self)

    def do_GET(self):
        self.__generic_request_mathing(HTTPVerbs.GET)

    def do_POST(self):
        self.__generic_request_mathing(HTTPVerbs.POST)

    def do_PUT(self):
        self.__generic_request_mathing(HTTPVerbs.PUT)

    def do_DELETE(self):
        self.__generic_request_mathing(HTTPVerbs.DELETE)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.end_headers()