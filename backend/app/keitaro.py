from __future__ import annotations

from typing import Annotated, Any, Literal, TypedDict

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer

from app import http
from app.settings import get_settings


def get_keitaro() -> Keitaro:
    settings = get_settings()
    return Keitaro({"url": settings.keitaro_url, "api_key": settings.keitaro_api_key})


class Keitaro:
    def __init__(self, options: KeitaroOptions) -> None:
        self.options = options

    async def create_campaign(self, draft: CampaignDraft) -> Campaign:
        request = self.get_campaign_creation_request(draft)
        created = await http.send_request(request)
        return convert_json_to_model(created, Campaign)

    async def delete_campaign(self, campaign_id: int) -> None:
        request = self.get_campaign_deletion_request(campaign_id)
        await http.send_request(request)

    async def load_campaign(self, campaign_id: int) -> Campaign:
        request = self.get_campaign_load_request(campaign_id)
        loaded = await http.send_request(request)
        return convert_json_to_model(loaded, Campaign)

    async def load_campaign_streams(self, campaign_id: int) -> list[Stream]:
        request = self.get_campaign_streams_load_request(campaign_id)
        loaded = await http.send_request(request)
        return convert_json_to_models(loaded, Stream)

    async def create_stream(self, draft: StreamDraft) -> Stream:
        request = self.get_stream_creation_request(draft)
        created = await http.send_request(request)
        return convert_json_to_model(created, Stream)

    async def update_stream_offers(
        self,
        stream_id: int,
        offers: list[StreamOffer],
    ) -> Stream:
        request = self.get_stream_offers_update_request(stream_id, offers)
        updated = await http.send_request(request)
        return convert_json_to_model(updated, Stream)

    async def load_offers(self) -> list[Offer]:
        request = self.get_offers_load_request()
        loaded = await http.send_request(request)
        return convert_json_to_models(loaded, Offer)

    async def load_domains(self) -> list[Domain]:
        request = self.get_domains_load_request()
        loaded = await http.send_request(request)
        return convert_json_to_models(loaded, Domain)

    async def load_campaign_groups(self) -> list[CampaignGroup]:
        request = self.get_campaign_groups_load_request()
        loaded = await http.send_request(request)
        return convert_json_to_models(loaded, CampaignGroup)

    async def load_traffic_sources(self) -> list[TrafficSource]:
        request = self.get_traffic_sources_load_request()
        loaded = await http.send_request(request)
        return convert_json_to_models(loaded, TrafficSource)

    def get_campaign_creation_request(self, draft: CampaignDraft) -> http.HttpRequest:
        return {
            "method": "POST",
            "url": self.get_url("/campaigns"),
            "headers": self.create_headers(),
            "body": convert_model_to_json(draft),
        }

    def get_campaign_deletion_request(self, campaign_id: int) -> http.HttpRequest:
        return {
            "method": "DELETE",
            "url": self.get_url(f"/campaigns/{campaign_id}"),
            "headers": self.create_headers(),
            "body": None,
        }

    def get_campaign_load_request(self, campaign_id: int) -> http.HttpRequest:
        return {
            "method": "GET",
            "url": self.get_url(f"/campaigns/{campaign_id}"),
            "headers": self.create_headers(),
            "body": None,
        }

    def get_campaign_streams_load_request(self, campaign_id: int) -> http.HttpRequest:
        return {
            "method": "GET",
            "url": self.get_url(f"/campaigns/{campaign_id}/streams"),
            "headers": self.create_headers(),
            "body": None,
        }

    def get_stream_creation_request(self, draft: StreamDraft) -> http.HttpRequest:
        return {
            "method": "POST",
            "url": self.get_url("/streams"),
            "headers": self.create_headers(),
            "body": convert_model_to_json(draft),
        }

    def get_stream_offers_update_request(
        self,
        stream_id: int,
        offers: list[StreamOffer],
    ) -> http.HttpRequest:
        update = StreamOffersUpdate(offers=offers)

        return {
            "method": "PUT",
            "url": self.get_url(f"/streams/{stream_id}"),
            "headers": self.create_headers(),
            "body": convert_model_to_json(update),
        }

    def get_offers_load_request(self) -> http.HttpRequest:
        return {
            "method": "GET",
            "url": self.get_url("/offers"),
            "headers": self.create_headers(),
            "body": None,
        }

    def get_domains_load_request(self) -> http.HttpRequest:
        return {
            "method": "GET",
            "url": self.get_url("/domains"),
            "headers": self.create_headers(),
            "body": None,
        }

    def get_campaign_groups_load_request(self) -> http.HttpRequest:
        return {
            "method": "GET",
            "url": self.get_url("/groups?type=campaigns"),
            "headers": self.create_headers(),
            "body": None,
        }

    def get_traffic_sources_load_request(self) -> http.HttpRequest:
        return {
            "method": "GET",
            "url": self.get_url("/traffic_sources"),
            "headers": self.create_headers(),
            "body": None,
        }

    def get_url(self, path: str) -> str:
        return f"{self.options['url']}{path}"

    def create_headers(self) -> dict[str, str]:
        return {"Api-Key": self.options["api_key"]}


class KeitaroOptions(TypedDict):
    url: str
    api_key: str


class StreamOffersUpdate(BaseModel):
    offers: list[StreamOffer]


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
