from __future__ import annotations

from typing import Any, Literal, TypedDict

import httpx


async def post(url: str, body: Any, deps: PostDeps) -> Any:
    request: HttpRequest = {"method": "POST", "url": url, "body": body}
    return await send_request(request, deps)


class PostDeps(TypedDict):
    headers: dict[str, str]


async def get(url: str, deps: GetDeps) -> Any:
    request: HttpRequest = {"method": "GET", "url": url, "body": None}
    return await send_request(request, deps)


class GetDeps(TypedDict):
    headers: dict[str, str]


async def put(url: str, body: Any, deps: PutDeps) -> Any:
    request: HttpRequest = {"method": "PUT", "url": url, "body": body}
    return await send_request(request, deps)


class PutDeps(TypedDict):
    headers: dict[str, str]


async def send_request(request: HttpRequest, deps: SendRequestDeps) -> Any:
    try:
        async with open_client(deps) as client:
            response = await client.request(
                request["method"],
                request["url"],
                json=request["body"],
            )

            response.raise_for_status()
            return response.json()
    except (httpx.HTTPError, ValueError) as error:
        raise RequestFailedError(request) from error


class HttpRequest(TypedDict):
    method: Literal["GET", "POST", "PUT"]
    url: str
    body: Any


class SendRequestDeps(TypedDict):
    headers: dict[str, str]


class RequestFailedError(Exception):
    def __init__(self, request: HttpRequest) -> None:
        super().__init__(f"Request {request['method']} {request['url']} failed")
        self.request = request


def open_client(deps: OpenClientDeps) -> httpx.AsyncClient:
    return httpx.AsyncClient(headers=deps["headers"])


class OpenClientDeps(TypedDict):
    headers: dict[str, str]
