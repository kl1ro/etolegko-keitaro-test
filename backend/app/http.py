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

            response.raise_for_status()
            return read_response_body(response)
    except (httpx.HTTPError, ValueError) as error:
        raise RequestFailedError(request) from error


class HttpRequest(TypedDict):
    method: Literal["GET", "POST", "PUT", "DELETE"]
    url: str
    headers: dict[str, str]
    body: Any


class RequestFailedError(Exception):
    def __init__(self, request: HttpRequest) -> None:
        super().__init__(f"Request {request['method']} {request['url']} failed")
        self.request = request


def read_response_body(response: httpx.Response) -> Any:
    if not response.content:
        return None

    return response.json()
