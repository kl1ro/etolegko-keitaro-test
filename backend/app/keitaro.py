from __future__ import annotations

from typing import Annotated, Literal, TypedDict

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer

from app import http
from app.settings import Settings


class Keitaro:
    def __init__(self, settings: Settings) -> None:
        self._url = settings.keitaro_url
        self._deps: KeitaroDeps = {"headers": {"Api-Key": settings.keitaro_api_key}}

    async def create_campaign(self, draft: CampaignDraft) -> Campaign:
        url = f"{self._url}/campaigns"
        return await http.post(url, draft, Campaign, self._deps)

    async def load_campaign(self, campaign_id: int) -> Campaign:
        url = f"{self._url}/campaigns/{campaign_id}"
        return await http.get(url, Campaign, self._deps)

    async def load_campaign_streams(self, campaign_id: int) -> list[Stream]:
        url = f"{self._url}/campaigns/{campaign_id}/streams"
        return await http.get_list(url, Stream, self._deps)

    async def create_stream(self, draft: StreamDraft) -> Stream:
        url = f"{self._url}/streams"
        return await http.post(url, draft, Stream, self._deps)

    async def update_stream_offers(
        self,
        stream_id: int,
        offers: list[StreamOffer],
    ) -> Stream:
        url = f"{self._url}/streams/{stream_id}"
        update = StreamOffersUpdate(offers=offers)
        return await http.put(url, update, Stream, self._deps)

    async def load_offers(self) -> list[Offer]:
        url = f"{self._url}/offers"
        return await http.get_list(url, Offer, self._deps)

    async def load_domains(self) -> list[Domain]:
        url = f"{self._url}/domains"
        return await http.get_list(url, Domain, self._deps)

    async def load_campaign_groups(self) -> list[CampaignGroup]:
        url = f"{self._url}/groups?type=campaigns"
        return await http.get_list(url, CampaignGroup, self._deps)

    async def load_traffic_sources(self) -> list[TrafficSource]:
        url = f"{self._url}/traffic_sources"
        return await http.get_list(url, TrafficSource, self._deps)


class KeitaroDeps(TypedDict):
    headers: dict[str, str]


class StreamOffersUpdate(BaseModel):
    offers: list[StreamOffer]


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
