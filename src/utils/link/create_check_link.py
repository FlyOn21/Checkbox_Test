from pprint import pprint
from uuid import UUID

from pydantic_core import Url

from src.settings.checkbox_settings import settings
from starlette.requests import Request


async def get_check_link(check_identifier: UUID, request: Request) -> Url:
    """
    Get check link by check identifier.

    :param check_identifier: UUID: Check identifier.
    :param request: Request: Request object.
    :return: str: Check link.
    """
    pprint(request.scope.get("router").__dict__.get("routes"))
    root_path = request.scope.get("root_path")
    check_endpoint_path = None
    for route in request.scope.get("router").__dict__.get("routes"):
        if route.name == settings.print_check_endpoint_name:
            check_endpoint_path = route.path
            break
        else:
            continue
    if not check_endpoint_path:
        raise ValueError("Check endpoint path not found")
    host = request.url.scheme + "://" + request.url.netloc
    str_length_q = f"{settings.str_length}={settings.check_default_line_width}"
    check_identifier_q = f"{settings.check_identifier}={check_identifier}"
    url_str = f"{host}{root_path}{check_endpoint_path}?{check_identifier_q}&{str_length_q}"
    return Url(url_str)
