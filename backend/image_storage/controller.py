import json
import os

import uuid6

import constants
from controller_utils import *
from exceptions import ServiceException
from http_verbs import *


class Controller:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

    @request(rtype=HTTPVerbs.GET, path_regex=f'^/{PathRegEx.UUID_REGEX}$')
    def get_image(self, request_handler):
        try:
            image_uuid = get_id_from_path(request_handler.path)
            if not os.path.exists(constants.IMAGES_DIR_PATH):
                raise ServiceException(404, 'Not found')

            files = dict()
            for file_path in os.listdir(constants.IMAGES_DIR_PATH):
                file_path_split = file_path.split('.')
                files[file_path_split[0]] = file_path_split[1]

            if image_uuid not in files:
                raise ServiceException(404, 'Not found')

            image_bytes = open(f'{constants.IMAGES_DIR_PATH}/{image_uuid}.{files[image_uuid]}', "rb").read()
            request_handler.send_response(200)
            request_handler.send_header('Content-Type', f'image/{files[image_uuid]}')
            request_handler.send_header('Access-Control-Allow-Origin', '*')
            request_handler.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
            request_handler.send_header('Access-Control-Allow-Headers', 'Content-Type')
            request_handler.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')

            request_handler.end_headers()
            request_handler.wfile.write(image_bytes)

        except ServiceException as e:
            send_error_response(self.logger, request_handler, e)

    @request(rtype=HTTPVerbs.DELETE, path_regex=f'^/{PathRegEx.UUID_REGEX}$')
    def delete_image(self, request_handler):
        try:
            image_uuid = get_id_from_path(request_handler.path)
            if not os.path.exists(constants.IMAGES_DIR_PATH):
                raise ServiceException(404, 'Not found')

            files = dict()
            for file_path in os.listdir(constants.IMAGES_DIR_PATH):
                file_path_split = file_path.split('.')
                files[file_path_split[0]] = file_path_split[1]

            if image_uuid not in files:
                raise ServiceException(404, 'Not found')

            os.remove(f'{constants.IMAGES_DIR_PATH}/{image_uuid}.{files[image_uuid]}')

            send_response(request_handler, json.dumps({'ok': 1}))

        except ServiceException as e:
            send_error_response(self.logger, request_handler, e)

    @request(rtype=HTTPVerbs.POST, path_regex='^/$')
    def new_image(self, request_handler):
        try:
            try:
                content_length = int(request_handler.headers.get('Content-Length'))
                content_type: str = request_handler.headers.get('Content-Type')
                if not re.search('^image/.*', content_type):
                    raise ServiceException(400, 'Bad request: file is not an image')

                if content_length > constants.MAX_IMAGE_SIZE:
                    raise ServiceException(400, 'Bad request: image too large')

                image_bytes = request_handler.rfile.read(content_length)

                if not os.path.exists(constants.IMAGES_DIR_PATH):
                    os.mkdir(constants.IMAGES_DIR_PATH, mode=0o755)

                extension = content_type.split('/')[1]
                image_id = str(uuid6.uuid7())
                image_file = open(f'{constants.IMAGES_DIR_PATH}/{image_id}.{extension}', 'wb')
                image_file.write(image_bytes)
                image_file.close()

                new_image_url = constants.SERVICE_URI + '/' + image_id
                send_response(request_handler,
                              new_image_url, 201, [("Content-type", "text/uri-list")])

            except BaseException as e:
                raise ServiceException(400, f'Bad request: {e}')

        except ServiceException as e:
            send_error_response(self.logger, request_handler, e)
