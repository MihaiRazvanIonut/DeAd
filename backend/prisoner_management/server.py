import logging
from http.server import ThreadingHTTPServer

import dispatcher


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class ServerFacade:
    def __init__(self, host: str, port: int, dispatcher_impl=dispatcher.Dispatcher):
        self.__host = host
        self.__port = port
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        self.__dispatcher = dispatcher_impl

    def run(self, server_class=ThreadingHTTPServer):
        server_address = (self.__host, self.__port)
        self.logger.info(f"Started server on http://{self.__host}:{self.__port}")
        try:
            dispatcher.load_controller_requests()
            httpd = server_class(server_address, self.__dispatcher)  # type: ignore
        except BaseException as e:
            self.logger.error(f"Error starting server, reason: {e}")
        else:
            httpd.serve_forever()
