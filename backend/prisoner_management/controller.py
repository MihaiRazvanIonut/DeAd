import json

import service
from controller_utils import *
from http_verbs import *


class Controller:

    @request(rtype=HTTPVerbs.GET, path_regex=r"")
    def hello_world(self, request_handler):
        results = service.get_all_prisoners()
        prisoners = [{"id": result["id"], "first_name": result["first_name"]} for result in results]
        send_response(request_handler, json.dumps({"prisoners": prisoners}))
