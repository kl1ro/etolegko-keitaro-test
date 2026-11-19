from __future__ import annotations

from typing import Annotated, Any, Literal, TypedDict

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer

from app import http


async def create_campaign(draft: CampaignDraft, deps: CreateCampaignDeps) -> Campaign:
    request: http.HttpRequest = {
        "method": "POST",
        "url": get_keitaro_url("/campaigns", deps),
        "headers": create_keitaro_headers(deps),
        "body": convert_model_to_json(draft),
    }

    created = await http.send_request(request)
    return convert_json_to_model(created, Campaign)


class CreateCampaignDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_campaign(campaign_id: int, deps: LoadCampaignDeps) -> Campaign:
    request: http.HttpRequest = {
        "method": "GET",
        "url": get_keitaro_url(f"/campaigns/{campaign_id}", deps),
        "headers": create_keitaro_headers(deps),
        "body": None,
    }

    loaded = await http.send_request(request)
    return convert_json_to_model(loaded, Campaign)


class LoadCampaignDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_campaign_streams(
    campaign_id: int,
    deps: LoadCampaignStreamsDeps,
) -> list[Stream]:
    request: http.HttpRequest = {
        "method": "GET",
        "url": get_keitaro_url(f"/campaigns/{campaign_id}/streams", deps),
        "headers": create_keitaro_headers(deps),
        "body": None,
    }

    loaded = await http.send_request(request)
    return convert_json_to_models(loaded, Stream)


class LoadCampaignStreamsDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def create_stream(draft: StreamDraft, deps: CreateStreamDeps) -> Stream:
    request: http.HttpRequest = {
        "method": "POST",
        "url": get_keitaro_url("/streams", deps),
        "headers": create_keitaro_headers(deps),
        "body": convert_model_to_json(draft),
    }

    created = await http.send_request(request)
    return convert_json_to_model(created, Stream)


class CreateStreamDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def update_stream_offers(
    stream_id: int,
    offers: list[StreamOffer],
    deps: UpdateStreamOffersDeps,
) -> Stream:
    update = StreamOffersUpdate(offers=offers)

    request: http.HttpRequest = {
        "method": "PUT",
        "url": get_keitaro_url(f"/streams/{stream_id}", deps),
        "headers": create_keitaro_headers(deps),
        "body": convert_model_to_json(update),
    }

    updated = await http.send_request(request)
    return convert_json_to_model(updated, Stream)


class UpdateStreamOffersDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


class StreamOffersUpdate(BaseModel):
    offers: list[StreamOffer]


async def load_offers(deps: LoadOffersDeps) -> list[Offer]:
    request: http.HttpRequest = {
        "method": "GET",
        "url": get_keitaro_url("/offers", deps),
        "headers": create_keitaro_headers(deps),
        "body": None,
    }

    loaded = await http.send_request(request)
    return convert_json_to_models(loaded, Offer)


class LoadOffersDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_domains(deps: LoadDomainsDeps) -> list[Domain]:
    request: http.HttpRequest = {
        "method": "GET",
        "url": get_keitaro_url("/domains", deps),
        "headers": create_keitaro_headers(deps),
        "body": None,
    }

    loaded = await http.send_request(request)
    return convert_json_to_models(loaded, Domain)


class LoadDomainsDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_campaign_groups(deps: LoadCampaignGroupsDeps) -> list[CampaignGroup]:
    request: http.HttpRequest = {
        "method": "GET",
        "url": get_keitaro_url("/groups?type=campaigns", deps),
        "headers": create_keitaro_headers(deps),
        "body": None,
    }

    loaded = await http.send_request(request)
    return convert_json_to_models(loaded, CampaignGroup)


class LoadCampaignGroupsDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_traffic_sources(deps: LoadTrafficSourcesDeps) -> list[TrafficSource]:
    request: http.HttpRequest = {
        "method": "GET",
        "url": get_keitaro_url("/traffic_sources", deps),
        "headers": create_keitaro_headers(deps),
        "body": None,
    }

    loaded = await http.send_request(request)
    return convert_json_to_models(loaded, TrafficSource)


class LoadTrafficSourcesDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


def get_keitaro_url(path: str, deps: GetKeitaroUrlDeps) -> str:
    return f"{deps['keitaro_url']}{path}"


class GetKeitaroUrlDeps(TypedDict):
    keitaro_url: str


def create_keitaro_headers(deps: CreateKeitaroHeadersDeps) -> dict[str, str]:
    return {"Api-Key": deps["keitaro_api_key"]}


class CreateKeitaroHeadersDeps(TypedDict):
    keitaro_api_key: str


def convert_model_to_json(model: BaseModel) -> Any:
    return model.model_dump(by_alias=True)


def convert_json_to_model[Model: BaseModel](
    json: Any,
    model_type: type[Model],
) -> Model:
    return model_type.model_validate(json)


def convert_json_to_models[Model: BaseModel](
    json: Any,
    model_type: type[Model],
) -> list[Model]:
    models = [convert_json_to_model(item, model_type) for item in json]
    return models


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
