import logging
import re

import exceptions
import http_verbs


def send_response(request_handler, response: str | None = None, status_code: int = 200,
                  headers: list[(str, str)] | None = None):
    if headers is None:
        headers = [("Content-type", "application/json")]

    request_handler.send_response(status_code)
    for header in headers:
        request_handler.send_header(*header)

    request_handler.send_header('Access-Control-Allow-Origin', '*')
    request_handler.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
    request_handler.send_header('Access-Control-Allow-Headers', 'Content-Type')
    request_handler.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')

    request_handler.end_headers()
    request_handler.wfile.write(response.encode('utf-8'))


def request(rtype: http_verbs.HTTPVerbs, path_regex: str):
    def decorator(func):
        func.request_type = rtype
        func.path_regex = path_regex
        return func

    return decorator


def get_query_params_from_path(path: str) -> dict:
    query_params = dict()
    try:
        unparsed_query_params = re.search(PathRegEx.QUERY_REGEX, path).group().replace('?', '').split('&')
        for unparsed_query_param in unparsed_query_params:
            query = unparsed_query_param.split('=')
            query_params[query[0]] = query[1]

    except BaseException:
        raise exceptions.ServiceException(400, f'Bad request: invalid query params')

    return query_params


def get_id_from_path(path: str) -> str:
    try:
        return re.search(f"{PathRegEx.UUID_REGEX}$", path).group()
    except BaseException:
        raise exceptions.ServiceException(400, "Id cannot be parsed")


def send_error_response(logger: logging.Logger, request_handler, e: exceptions.ServiceException):
    send_response(request_handler, e.message, e.status_code, [("Content-type", "text/html")])
    logger.error(f"Error encountered: {e.message}")


class PathRegEx:
    ID_REGEX = r"[0-9a-zA-z]+"
    QUERY_REGEX = r"\?.+"
    UUID_REGEX = r'\b[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}\b'
