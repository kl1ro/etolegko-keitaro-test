from __future__ import annotations

from typing import Any, TypedDict

import httpx
from pydantic import BaseModel


async def post[Result: BaseModel](
    url: str,
    body: BaseModel,
    result_type: type[Result],
    deps: PostDeps,
) -> Result:
    result = await send_request("POST", url, deps, json=body.model_dump(by_alias=True))
    return result_type.model_validate(result)


class PostDeps(TypedDict):
    headers: dict[str, str]


async def get[Result: BaseModel](
    url: str,
    result_type: type[Result],
    deps: GetDeps,
) -> Result:
    result = await send_request("GET", url, deps)
    return result_type.model_validate(result)


class GetDeps(TypedDict):
    headers: dict[str, str]


async def get_list[Item: BaseModel](
    url: str,
    item_type: type[Item],
    deps: GetListDeps,
) -> list[Item]:
    items = await send_request("GET", url, deps)
    validated_items = [item_type.model_validate(item) for item in items]
    return validated_items


class GetListDeps(TypedDict):
    headers: dict[str, str]


async def put[Result: BaseModel](
    url: str,
    body: BaseModel,
    result_type: type[Result],
    deps: PutDeps,
) -> Result:
    result = await send_request("PUT", url, deps, json=body.model_dump(by_alias=True))
    return result_type.model_validate(result)


class PutDeps(TypedDict):
    headers: dict[str, str]


async def send_request(
    method: str,
    url: str,
    deps: SendRequestDeps,
    *,
    json: Any = None,
) -> Any:
    try:
        async with open_client(deps) as client:
            response = await client.request(method, url, json=json)
            response.raise_for_status()
            return response.json()
    except (httpx.HTTPError, ValueError) as error:
        raise RequestFailedError(method=method, url=url) from error


class SendRequestDeps(TypedDict):
    headers: dict[str, str]


class RequestFailedError(Exception):
    def __init__(self, *, method: str, url: str) -> None:
        super().__init__(f"Request {method} {url} failed")
        self.method = method
        self.url = url


def open_client(deps: OpenClientDeps) -> httpx.AsyncClient:
    return httpx.AsyncClient(headers=deps["headers"])


class OpenClientDeps(TypedDict):
    headers: dict[str, str]
