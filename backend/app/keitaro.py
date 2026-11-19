from __future__ import annotations

from typing import Annotated, Literal, TypedDict

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer

from app import http


async def create_campaign(draft: CampaignDraft, deps: CreateCampaignDeps) -> Campaign:
    url = f"{deps['keitaro_url']}/campaigns"
    request_deps = create_request_deps(deps)
    return await http.post(url, draft, Campaign, request_deps)


class CreateCampaignDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_campaign(campaign_id: int, deps: LoadCampaignDeps) -> Campaign:
    url = f"{deps['keitaro_url']}/campaigns/{campaign_id}"
    request_deps = create_request_deps(deps)
    return await http.get(url, Campaign, request_deps)


class LoadCampaignDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_campaign_streams(
    campaign_id: int,
    deps: LoadCampaignStreamsDeps,
) -> list[Stream]:
    url = f"{deps['keitaro_url']}/campaigns/{campaign_id}/streams"
    request_deps = create_request_deps(deps)
    return await http.get_list(url, Stream, request_deps)


class LoadCampaignStreamsDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def create_stream(draft: StreamDraft, deps: CreateStreamDeps) -> Stream:
    url = f"{deps['keitaro_url']}/streams"
    request_deps = create_request_deps(deps)
    return await http.post(url, draft, Stream, request_deps)


class CreateStreamDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def update_stream_offers(
    stream_id: int,
    offers: list[StreamOffer],
    deps: UpdateStreamOffersDeps,
) -> Stream:
    url = f"{deps['keitaro_url']}/streams/{stream_id}"
    update = StreamOffersUpdate(offers=offers)
    request_deps = create_request_deps(deps)
    return await http.put(url, update, Stream, request_deps)


class UpdateStreamOffersDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


class StreamOffersUpdate(BaseModel):
    offers: list[StreamOffer]


async def load_offers(deps: LoadOffersDeps) -> list[Offer]:
    url = f"{deps['keitaro_url']}/offers"
    request_deps = create_request_deps(deps)
    return await http.get_list(url, Offer, request_deps)


class LoadOffersDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_domains(deps: LoadDomainsDeps) -> list[Domain]:
    url = f"{deps['keitaro_url']}/domains"
    request_deps = create_request_deps(deps)
    return await http.get_list(url, Domain, request_deps)


class LoadDomainsDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_campaign_groups(deps: LoadCampaignGroupsDeps) -> list[CampaignGroup]:
    url = f"{deps['keitaro_url']}/groups?type=campaigns"
    request_deps = create_request_deps(deps)
    return await http.get_list(url, CampaignGroup, request_deps)


class LoadCampaignGroupsDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_traffic_sources(deps: LoadTrafficSourcesDeps) -> list[TrafficSource]:
    url = f"{deps['keitaro_url']}/traffic_sources"
    request_deps = create_request_deps(deps)
    return await http.get_list(url, TrafficSource, request_deps)


class LoadTrafficSourcesDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


def create_request_deps(deps: CreateRequestDepsDeps) -> RequestDeps:
    return {"headers": {"Api-Key": deps["keitaro_api_key"]}}


class CreateRequestDepsDeps(TypedDict):
    keitaro_api_key: str


class RequestDeps(TypedDict):
    headers: dict[str, str]


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
