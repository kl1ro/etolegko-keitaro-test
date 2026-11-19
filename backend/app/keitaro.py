from __future__ import annotations

from typing import Annotated, Any, Literal

import httpx
from pydantic import BaseModel, ConfigDict, Field, PlainSerializer

from app.settings import Settings


class Keitaro:
    def __init__(self, settings: Settings) -> None:
        self._url = settings.keitaro_url
        self._api_key = settings.keitaro_api_key

    async def create_campaign(self, draft: CampaignDraft) -> Campaign:
        return await self._post("/campaigns", draft, Campaign)

    async def load_campaign(self, campaign_id: int) -> Campaign:
        return await self._get(f"/campaigns/{campaign_id}", Campaign)

    async def load_campaign_streams(self, campaign_id: int) -> list[Stream]:
        return await self._get_list(f"/campaigns/{campaign_id}/streams", Stream)

    async def create_stream(self, draft: StreamDraft) -> Stream:
        return await self._post("/streams", draft, Stream)

    async def update_stream_offers(
        self,
        stream_id: int,
        offers: list[StreamOffer],
    ) -> Stream:
        update = StreamOffersUpdate(offers=offers)
        return await self._put(f"/streams/{stream_id}", update, Stream)

    async def load_offers(self) -> list[Offer]:
        return await self._get_list("/offers", Offer)

    async def load_domains(self) -> list[Domain]:
        return await self._get_list("/domains", Domain)

    async def load_campaign_groups(self) -> list[CampaignGroup]:
        return await self._get_list("/groups?type=campaigns", CampaignGroup)

    async def load_traffic_sources(self) -> list[TrafficSource]:
        return await self._get_list("/traffic_sources", TrafficSource)

    async def _post[Result: BaseModel](
        self,
        path: str,
        body: BaseModel,
        result_type: type[Result],
    ) -> Result:
        result = await self._send("POST", path, json=body.model_dump(by_alias=True))
        return result_type.model_validate(result)

    async def _get[Result: BaseModel](
        self,
        path: str,
        result_type: type[Result],
    ) -> Result:
        result = await self._send("GET", path)
        return result_type.model_validate(result)

    async def _get_list[Item: BaseModel](
        self,
        path: str,
        item_type: type[Item],
    ) -> list[Item]:
        items = await self._send("GET", path)
        validated_items = [item_type.model_validate(item) for item in items]
        return validated_items

    async def _put[Result: BaseModel](
        self,
        path: str,
        body: BaseModel,
        result_type: type[Result],
    ) -> Result:
        result = await self._send("PUT", path, json=body.model_dump(by_alias=True))
        return result_type.model_validate(result)

    async def _send(self, method: str, path: str, **options: Any) -> Any:
        try:
            async with self._open_client() as client:
                response = await client.request(method, path, **options)
                response.raise_for_status()
                return response.json()
        except (httpx.HTTPError, ValueError) as error:
            raise KeitaroRequestFailedError(method=method, path=path) from error

    def _open_client(self) -> httpx.AsyncClient:
        headers = {"Api-Key": self._api_key}
        return httpx.AsyncClient(base_url=self._url, headers=headers)


class StreamOffersUpdate(BaseModel):
    offers: list[StreamOffer]


class KeitaroRequestFailedError(Exception):
    def __init__(self, *, method: str, path: str) -> None:
        super().__init__(f"Keitaro request {method} {path} failed")
        self.method = method
        self.path = path


class CampaignDraft(BaseModel):
    name: str
    type: Literal["position", "weight"]
    group_id: Annotated[int, PlainSerializer(str)]
    traffic_source_id: int
    domain_id: int


class Campaign(BaseModel):
    id: int
    name: str


class StreamDraft(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    campaign_id: int
    type: Literal["forced", "regular", "default"]
    name: str
    position: int
    action_schema: Literal["landings", "redirect", "action"] = Field(alias="schema")
    action_type: str
    action_payload: str | None = None
    filters: list[StreamFilter] = []
    offers: list[StreamOffer] = []


class Stream(StreamDraft):
    id: int


class StreamFilter(BaseModel):
    name: str
    mode: Literal["accept", "reject"]
    payload: list[str]


class StreamOffer(BaseModel):
    offer_id: int
    share: int
    state: Literal["active", "disabled"] = "active"


class Offer(BaseModel):
    id: int
    name: str


class Domain(BaseModel):
    id: int
    name: str


class CampaignGroup(BaseModel):
    id: int
    name: str


class TrafficSource(BaseModel):
    id: int
    name: str
