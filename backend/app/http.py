from __future__ import annotations

from typing import Any, Literal, TypedDict

import httpx


async def post(url: str, body: Any, headers: dict[str, str]) -> Any:
    request: HttpRequest = {
        "method": "POST",
        "url": url,
        "headers": headers,
        "body": body,
    }

    return await send_request(request)


async def get(url: str, headers: dict[str, str]) -> Any:
    request: HttpRequest = {
        "method": "GET",
        "url": url,
        "headers": headers,
        "body": None,
    }

    return await send_request(request)


async def put(url: str, body: Any, headers: dict[str, str]) -> Any:
    request: HttpRequest = {
        "method": "PUT",
        "url": url,
        "headers": headers,
        "body": body,
    }

    return await send_request(request)


async def send_request(request: HttpRequest) -> Any:
    try:
        async with open_client() as client:
            response = await client.request(
                request["method"],
                request["url"],
                headers=request["headers"],
                json=request["body"],
            )

            response.raise_for_status()
            return response.json()
    except (httpx.HTTPError, ValueError) as error:
        raise RequestFailedError(request) from error


class HttpRequest(TypedDict):
    method: Literal["GET", "POST", "PUT"]
    url: str
    headers: dict[str, str]
    body: Any


class RequestFailedError(Exception):
    def __init__(self, request: HttpRequest) -> None:
        super().__init__(f"Request {request['method']} {request['url']} failed")
        self.request = request


def open_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()
