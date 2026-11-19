from __future__ import annotations

from typing import Annotated, Any, Literal, TypedDict

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer

from app import http


async def create_campaign(draft: CampaignDraft, deps: CreateCampaignDeps) -> Campaign:
    request = create_campaign_creation_request(draft, deps)
    created = await http.send_request(request)
    return convert_json_to_model(created, Campaign)


class CreateCampaignDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_campaign(campaign_id: int, deps: LoadCampaignDeps) -> Campaign:
    request = create_campaign_load_request(campaign_id, deps)
    loaded = await http.send_request(request)
    return convert_json_to_model(loaded, Campaign)


class LoadCampaignDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_campaign_streams(
    campaign_id: int,
    deps: LoadCampaignStreamsDeps,
) -> list[Stream]:
    request = create_campaign_streams_load_request(campaign_id, deps)
    loaded = await http.send_request(request)
    return convert_json_to_models(loaded, Stream)


class LoadCampaignStreamsDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def create_stream(draft: StreamDraft, deps: CreateStreamDeps) -> Stream:
    request = create_stream_creation_request(draft, deps)
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
    request = create_stream_offers_update_request(stream_id, offers, deps)
    updated = await http.send_request(request)
    return convert_json_to_model(updated, Stream)


class UpdateStreamOffersDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_offers(deps: LoadOffersDeps) -> list[Offer]:
    request = create_offers_load_request(deps)
    loaded = await http.send_request(request)
    return convert_json_to_models(loaded, Offer)


class LoadOffersDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_domains(deps: LoadDomainsDeps) -> list[Domain]:
    request = create_domains_load_request(deps)
    loaded = await http.send_request(request)
    return convert_json_to_models(loaded, Domain)


class LoadDomainsDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_campaign_groups(deps: LoadCampaignGroupsDeps) -> list[CampaignGroup]:
    request = create_campaign_groups_load_request(deps)
    loaded = await http.send_request(request)
    return convert_json_to_models(loaded, CampaignGroup)


class LoadCampaignGroupsDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_traffic_sources(deps: LoadTrafficSourcesDeps) -> list[TrafficSource]:
    request = create_traffic_sources_load_request(deps)
    loaded = await http.send_request(request)
    return convert_json_to_models(loaded, TrafficSource)


class LoadTrafficSourcesDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


def create_campaign_creation_request(
    draft: CampaignDraft,
    deps: CreateCampaignCreationRequestDeps,
) -> http.HttpRequest:
    return {
        "method": "POST",
        "url": get_keitaro_url("/campaigns", deps),
        "headers": create_keitaro_headers(deps),
        "body": convert_model_to_json(draft),
    }


class CreateCampaignCreationRequestDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


def convert_json_to_model[Model: BaseModel](
    json: Any,
    model_type: type[Model],
) -> Model:
    return model_type.model_validate(json)


def create_campaign_load_request(
    campaign_id: int,
    deps: CreateCampaignLoadRequestDeps,
) -> http.HttpRequest:
    return {
        "method": "GET",
        "url": get_keitaro_url(f"/campaigns/{campaign_id}", deps),
        "headers": create_keitaro_headers(deps),
        "body": None,
    }


class CreateCampaignLoadRequestDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


def create_campaign_streams_load_request(
    campaign_id: int,
    deps: CreateCampaignStreamsLoadRequestDeps,
) -> http.HttpRequest:
    return {
        "method": "GET",
        "url": get_keitaro_url(f"/campaigns/{campaign_id}/streams", deps),
        "headers": create_keitaro_headers(deps),
        "body": None,
    }


class CreateCampaignStreamsLoadRequestDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


def convert_json_to_models[Model: BaseModel](
    json: Any,
    model_type: type[Model],
) -> list[Model]:
    models = [convert_json_to_model(item, model_type) for item in json]
    return models


def create_stream_creation_request(
    draft: StreamDraft,
    deps: CreateStreamCreationRequestDeps,
) -> http.HttpRequest:
    return {
        "method": "POST",
        "url": get_keitaro_url("/streams", deps),
        "headers": create_keitaro_headers(deps),
        "body": convert_model_to_json(draft),
    }


class CreateStreamCreationRequestDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


def create_stream_offers_update_request(
    stream_id: int,
    offers: list[StreamOffer],
    deps: CreateStreamOffersUpdateRequestDeps,
) -> http.HttpRequest:
    update = StreamOffersUpdate(offers=offers)

    return {
        "method": "PUT",
        "url": get_keitaro_url(f"/streams/{stream_id}", deps),
        "headers": create_keitaro_headers(deps),
        "body": convert_model_to_json(update),
    }


class CreateStreamOffersUpdateRequestDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


class StreamOffersUpdate(BaseModel):
    offers: list[StreamOffer]


def create_offers_load_request(deps: CreateOffersLoadRequestDeps) -> http.HttpRequest:
    return {
        "method": "GET",
        "url": get_keitaro_url("/offers", deps),
        "headers": create_keitaro_headers(deps),
        "body": None,
    }


class CreateOffersLoadRequestDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


def create_domains_load_request(deps: CreateDomainsLoadRequestDeps) -> http.HttpRequest:
    return {
        "method": "GET",
        "url": get_keitaro_url("/domains", deps),
        "headers": create_keitaro_headers(deps),
        "body": None,
    }


class CreateDomainsLoadRequestDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


def create_campaign_groups_load_request(
    deps: CreateCampaignGroupsLoadRequestDeps,
) -> http.HttpRequest:
    return {
        "method": "GET",
        "url": get_keitaro_url("/groups?type=campaigns", deps),
        "headers": create_keitaro_headers(deps),
        "body": None,
    }


class CreateCampaignGroupsLoadRequestDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


def create_traffic_sources_load_request(
    deps: CreateTrafficSourcesLoadRequestDeps,
) -> http.HttpRequest:
    return {
        "method": "GET",
        "url": get_keitaro_url("/traffic_sources", deps),
        "headers": create_keitaro_headers(deps),
        "body": None,
    }


class CreateTrafficSourcesLoadRequestDeps(TypedDict):
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
