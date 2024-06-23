import re
from http.server import SimpleHTTPRequestHandler

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


class Dispatcher(SimpleHTTPRequestHandler):

    def __generic_request_matching(self, request_type: HTTPVerbs):
        found_page = False
        for path_regex, method in request_mappings[request_type].items():
            if re.search(path_regex, self.path):
                found_page = True
                method(controller, self)

        if not found_page:
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write('<h1>Error: 404 Not Found<h1>'.encode('utf-8'))

    def do_GET(self):
        self.__generic_request_matching(HTTPVerbs.GET)
        return super().do_GET()

    def do_POST(self):
        self.__generic_request_matching(HTTPVerbs.POST)

    def do_PUT(self):
        self.__generic_request_matching(HTTPVerbs.PUT)

    def do_DELETE(self):
        self.__generic_request_matching(HTTPVerbs.DELETE)

    def translate_path(self, path):
        return path
