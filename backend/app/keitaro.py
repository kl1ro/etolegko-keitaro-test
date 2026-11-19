from __future__ import annotations

from typing import Annotated, Any, Literal, TypedDict

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer

from app import http


async def create_campaign(draft: CampaignDraft, deps: CreateCampaignDeps) -> Campaign:
    created = await post_to_keitaro("/campaigns", draft, deps)
    return convert_json_to_model(created, Campaign)


class CreateCampaignDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_campaign(campaign_id: int, deps: LoadCampaignDeps) -> Campaign:
    loaded = await get_from_keitaro(f"/campaigns/{campaign_id}", deps)
    return convert_json_to_model(loaded, Campaign)


class LoadCampaignDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_campaign_streams(
    campaign_id: int,
    deps: LoadCampaignStreamsDeps,
) -> list[Stream]:
    loaded = await get_from_keitaro(f"/campaigns/{campaign_id}/streams", deps)
    return convert_json_to_models(loaded, Stream)


class LoadCampaignStreamsDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def create_stream(draft: StreamDraft, deps: CreateStreamDeps) -> Stream:
    created = await post_to_keitaro("/streams", draft, deps)
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
    updated = await put_to_keitaro(f"/streams/{stream_id}", update, deps)
    return convert_json_to_model(updated, Stream)


class UpdateStreamOffersDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


class StreamOffersUpdate(BaseModel):
    offers: list[StreamOffer]


async def load_offers(deps: LoadOffersDeps) -> list[Offer]:
    loaded = await get_from_keitaro("/offers", deps)
    return convert_json_to_models(loaded, Offer)


class LoadOffersDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_domains(deps: LoadDomainsDeps) -> list[Domain]:
    loaded = await get_from_keitaro("/domains", deps)
    return convert_json_to_models(loaded, Domain)


class LoadDomainsDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_campaign_groups(deps: LoadCampaignGroupsDeps) -> list[CampaignGroup]:
    loaded = await get_from_keitaro("/groups?type=campaigns", deps)
    return convert_json_to_models(loaded, CampaignGroup)


class LoadCampaignGroupsDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def load_traffic_sources(deps: LoadTrafficSourcesDeps) -> list[TrafficSource]:
    loaded = await get_from_keitaro("/traffic_sources", deps)
    return convert_json_to_models(loaded, TrafficSource)


class LoadTrafficSourcesDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


async def post_to_keitaro(path: str, body: BaseModel, deps: PostToKeitaroDeps) -> Any:
    url = get_keitaro_url(path, deps)
    json = convert_model_to_json(body)
    headers = create_keitaro_headers(deps)
    return await http.post(url, json, headers)


class PostToKeitaroDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


def convert_json_to_model[Model: BaseModel](
    json: Any,
    model_type: type[Model],
) -> Model:
    return model_type.model_validate(json)


async def get_from_keitaro(path: str, deps: GetFromKeitaroDeps) -> Any:
    url = get_keitaro_url(path, deps)
    headers = create_keitaro_headers(deps)
    return await http.get(url, headers)


class GetFromKeitaroDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


def convert_json_to_models[Model: BaseModel](
    json: Any,
    model_type: type[Model],
) -> list[Model]:
    models = [convert_json_to_model(item, model_type) for item in json]
    return models


async def put_to_keitaro(path: str, body: BaseModel, deps: PutToKeitaroDeps) -> Any:
    url = get_keitaro_url(path, deps)
    json = convert_model_to_json(body)
    headers = create_keitaro_headers(deps)
    return await http.put(url, json, headers)


class PutToKeitaroDeps(TypedDict):
    keitaro_url: str
    keitaro_api_key: str


def get_keitaro_url(path: str, deps: GetKeitaroUrlDeps) -> str:
    return f"{deps['keitaro_url']}{path}"


class GetKeitaroUrlDeps(TypedDict):
    keitaro_url: str


def convert_model_to_json(model: BaseModel) -> Any:
    return model.model_dump(by_alias=True)


def create_keitaro_headers(deps: CreateKeitaroHeadersDeps) -> dict[str, str]:
    return {"Api-Key": deps["keitaro_api_key"]}


class CreateKeitaroHeadersDeps(TypedDict):
    keitaro_api_key: str


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
