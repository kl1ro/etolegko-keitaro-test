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
        campaign = await self._send("POST", "/campaigns", json=draft.model_dump())
        return Campaign.model_validate(campaign)

    async def load_campaign(self, campaign_id: int) -> Campaign:
        campaign = await self._send("GET", f"/campaigns/{campaign_id}")
        return Campaign.model_validate(campaign)

    async def load_campaign_streams(self, campaign_id: int) -> list[Stream]:
        return await self._load_items(f"/campaigns/{campaign_id}/streams", Stream)

    async def create_stream(self, draft: StreamDraft) -> Stream:
        body = draft.model_dump(by_alias=True)
        stream = await self._send("POST", "/streams", json=body)
        return Stream.model_validate(stream)

    async def update_stream_offers(
        self,
        stream_id: int,
        offers: list[StreamOffer],
    ) -> Stream:
        body = {"offers": [offer.model_dump() for offer in offers]}
        stream = await self._send("PUT", f"/streams/{stream_id}", json=body)
        return Stream.model_validate(stream)

    async def load_offers(self) -> list[Offer]:
        return await self._load_items("/offers", Offer)

    async def load_domains(self) -> list[Domain]:
        return await self._load_items("/domains", Domain)

    async def load_campaign_groups(self) -> list[CampaignGroup]:
        params = {"type": "campaigns"}
        return await self._load_items("/groups", CampaignGroup, params=params)

    async def load_traffic_sources(self) -> list[TrafficSource]:
        return await self._load_items("/traffic_sources", TrafficSource)

    async def _load_items[Item: BaseModel](
        self,
        path: str,
        item_type: type[Item],
        params: dict[str, str] | None = None,
    ) -> list[Item]:
        items = await self._send("GET", path, params=params)
        validated_items = [item_type.model_validate(item) for item in items]
        return validated_items

    async def _send(self, method: str, path: str, **options: Any) -> Any:
        try:
            async with httpx.AsyncClient(
                base_url=self._url,
                headers={"Api-Key": self._api_key},
            ) as client:
                response = await client.request(method, path, **options)
                response.raise_for_status()
                return response.json()
        except (httpx.HTTPError, ValueError) as error:
            raise KeitaroRequestFailedError(method=method, path=path) from error


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
