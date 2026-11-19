from __future__ import annotations

from typing import Annotated, TypedDict

from fastapi import Depends

from app.keitaro import Keitaro, Stream, StreamOffer, get_keitaro


def get_campaign_offers_load_deps(
    keitaro: Annotated[Keitaro, Depends(get_keitaro)],
) -> LoadCampaignOffersDeps:
    return {"keitaro": keitaro}


async def load_campaign_offers(
    campaign_id: int,
    deps: LoadCampaignOffersDeps,
) -> list[StreamOffer]:
    offer_stream = await load_offer_stream(campaign_id, deps)
    return offer_stream.offers


class LoadCampaignOffersDeps(TypedDict):
    keitaro: Keitaro


async def load_offer_stream(campaign_id: int, deps: LoadOfferStreamDeps) -> Stream:
    streams = await deps["keitaro"].load_campaign_streams(campaign_id)
    offer_stream = find_offer_stream(streams)

    if not offer_stream:
        raise OfferStreamNotFoundError(campaign_id)

    return offer_stream


class LoadOfferStreamDeps(TypedDict):
    keitaro: Keitaro


class OfferStreamNotFoundError(Exception):
    def __init__(self, campaign_id: int) -> None:
        super().__init__(f"Campaign {campaign_id} has no offer stream")
        self.campaign_id = campaign_id


def find_offer_stream(streams: list[Stream]) -> Stream | None:
    offer_stream = next((stream for stream in streams if is_offer_stream(stream)), None)
    return offer_stream


def is_offer_stream(stream: Stream) -> bool:
    return stream.type == "default"
