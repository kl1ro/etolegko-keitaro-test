from __future__ import annotations

from typing import Any, Literal, TypedDict

import httpx


async def send_request(request: HttpRequest) -> Any:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                request["method"],
                request["url"],
                headers=request["headers"],
                json=request["body"],
            )

            if response.is_error:
                raise get_request_rejection_error(request, response)

            return read_response_body(response)
    except (httpx.HTTPError, ValueError) as error:
        raise RequestFailedError(request) from error


class HttpRequest(TypedDict):
    method: Literal["GET", "POST", "PUT", "DELETE"]
    url: str
    headers: dict[str, str]
    body: Any


class RequestFailedError(Exception):
    def __init__(self, request: HttpRequest, message: str | None = None) -> None:
        default_message = f"Request {request['method']} {request['url']} failed"
        super().__init__(message or default_message)
        self.request = request


def get_request_rejection_error(
    request: HttpRequest,
    response: httpx.Response,
) -> RequestRejectedError:
    body = read_response_body(response)
    error = RequestRejectedError(request, response.status_code, body)
    return error


class RequestRejectedError(RequestFailedError):
    def __init__(self, request: HttpRequest, status_code: int, body: Any) -> None:
        super().__init__(
            request,
            f"Request {request['method']} {request['url']} was rejected "
            f"with {status_code}: {body}",
        )

        self.status_code = status_code
        self.body = body


def read_response_body(response: httpx.Response) -> Any:
    if not response.content:
        return None

    return response.json()
