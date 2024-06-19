import http_verbs


def send_response(request_handler, response: str, status_code: int = 200, headers: list[(str, str)] | None = None):
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


class PathRegEx:
    ID_REGEX = r"[0-9a-z]+"
    QUERY_REGEX = r"\?.+"
