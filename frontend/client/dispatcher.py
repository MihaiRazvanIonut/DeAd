import re
from http.server import SimpleHTTPRequestHandler

import constants
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


def parse_cookies(cookies: str) -> dict:
    cookies_dict = dict()
    split_cookies = cookies.split(';')
    for cookie in split_cookies:
        split_cookie = cookie.split('=')
        cookies_dict[split_cookie[0].strip()] = split_cookie[1].strip()

    return cookies_dict


class Dispatcher(SimpleHTTPRequestHandler):

    def __generic_request_matching(self, request_type: HTTPVerbs) -> bool | None:
        found_page = False
        cookies = self.headers.get('Cookie')
        if not re.search('^/register$', self.path) \
                and not re.search('^/login$', self.path) \
                and not re.search('.js', self.path) \
                and not re.search('.css', self.path) \
                and not re.search('.ico', self.path):
            if cookies:
                cookies = parse_cookies(cookies)
                if not cookies.get(constants.SESSION_ID_IDENTIFIER):
                    self.send_response(302)
                    self.send_header('Location', '/login')
                    self.end_headers()
                    return False

            else:
                self.send_response(302)
                self.send_header('Location', '/login')
                self.end_headers()
                return False
        for path_regex, method in request_mappings[request_type].items():
            if re.search(path_regex, self.path):
                found_page = True
                method(controller, self)
                break

        if not found_page:
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write('<h1>Error: 404 Not Found<h1>'.encode('utf-8'))

    def do_GET(self):
        flag = self.__generic_request_matching(HTTPVerbs.GET)
        if flag is None:
            return super().do_GET()

    def do_POST(self):
        self.__generic_request_matching(HTTPVerbs.POST)

    def do_PUT(self):
        self.__generic_request_matching(HTTPVerbs.PUT)

    def do_DELETE(self):
        self.__generic_request_matching(HTTPVerbs.DELETE)

    def translate_path(self, path):
        return path
