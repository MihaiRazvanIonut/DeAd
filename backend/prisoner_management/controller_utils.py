import re

import http_verbs
import exceptions


def send_response(request_handler, response: str | None = None, status_code: int = 200,
                  headers: list[(str, str)] | None = None):
    if headers is None:
        headers = [("Content-type", "application/json")]

    request_handler.send_response(status_code)
    for header in headers:
        request_handler.send_header(*header)

    request_handler.end_headers()
    request_handler.wfile.write(response.encode('utf-8'))


def request(rtype: http_verbs.HTTPVerbs, path_regex: str):
    def decorator(func):
        func.request_type = rtype
        func.path_regex = path_regex
        return func

    return decorator


def get_id_from_path(path: str) -> str:
    try:
        return re.search(f"{PathRegEx.ID_REGEX}$", path).group()
    except BaseException:
        raise exceptions.ServiceException(400, "Id cannot be parsed")


class PathRegEx:
    ID_REGEX = r"[0-9a-z]+"
    QUERY_REGEX = r"\?.+"
