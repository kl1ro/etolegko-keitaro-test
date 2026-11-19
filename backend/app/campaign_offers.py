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


def get_campaign_offer_addition_deps(
    keitaro: Annotated[Keitaro, Depends(get_keitaro)],
) -> AddCampaignOfferDeps:
    return {"keitaro": keitaro}


async def add_campaign_offer(
    campaign_id: int,
    offer_id: int,
    deps: AddCampaignOfferDeps,
) -> list[StreamOffer]:
    offer_stream = await load_offer_stream(campaign_id, deps)
    offers = get_offers_with_added_offer(offer_stream.offers, offer_id)
    updated_stream = await deps["keitaro"].update_stream_offers(offer_stream.id, offers)
    return updated_stream.offers


class AddCampaignOfferDeps(TypedDict):
    keitaro: Keitaro


def get_offers_with_added_offer(
    offers: list[StreamOffer],
    offer_id: int,
) -> list[StreamOffer]:
    ensure_offer_not_in_stream(offer_id, offers)
    added = [*offers, StreamOffer(offer_id=offer_id, share=0)]
    shared = get_offers_with_even_shares(added)
    return shared


def ensure_offer_not_in_stream(offer_id: int, offers: list[StreamOffer]) -> None:
    if has_offer(offers, offer_id):
        raise OfferAlreadyInStreamError(offer_id)


class OfferAlreadyInStreamError(Exception):
    def __init__(self, offer_id: int) -> None:
        super().__init__(f"Offer {offer_id} is already in the stream")
        self.offer_id = offer_id


def get_offers_with_even_shares(offers: list[StreamOffer]) -> list[StreamOffer]:
    shares = get_even_shares(len(offers))

    shared = [
        offer.model_copy(update={"share": share})
        for offer, share in zip(offers, shares, strict=True)
    ]

    return shared


def has_offer(offers: list[StreamOffer], offer_id: int) -> bool:
    return any(is_offer(offer, offer_id) for offer in offers)


def get_even_shares(count: int) -> list[int]:
    share, leftover = divmod(TOTAL_SHARE, count)
    shares = [share] * (count - leftover) + [share + 1] * leftover
    return shares


TOTAL_SHARE = 100


def is_offer(offer: StreamOffer, offer_id: int) -> bool:
    return offer.offer_id == offer_id


def get_campaign_offer_removal_deps(
    keitaro: Annotated[Keitaro, Depends(get_keitaro)],
) -> RemoveCampaignOfferDeps:
    return {"keitaro": keitaro}


async def remove_campaign_offer(
    campaign_id: int,
    offer_id: int,
    deps: RemoveCampaignOfferDeps,
) -> list[StreamOffer]:
    offer_stream = await load_offer_stream(campaign_id, deps)
    offers = get_offers_with_removed_offer(offer_stream.offers, offer_id)
    updated_stream = await deps["keitaro"].update_stream_offers(offer_stream.id, offers)
    return updated_stream.offers


class RemoveCampaignOfferDeps(TypedDict):
    keitaro: Keitaro


def get_offers_with_removed_offer(
    offers: list[StreamOffer],
    offer_id: int,
) -> list[StreamOffer]:
    ensure_offer_in_stream(offer_id, offers)
    ensure_several_offers(offers)
    remaining = [offer for offer in offers if not is_offer(offer, offer_id)]
    shared = get_offers_with_even_shares(remaining)
    return shared


def ensure_offer_in_stream(offer_id: int, offers: list[StreamOffer]) -> None:
    if not has_offer(offers, offer_id):
        raise OfferNotInStreamError(offer_id)


class OfferNotInStreamError(Exception):
    def __init__(self, offer_id: int) -> None:
        super().__init__(f"Offer {offer_id} is not in the stream")
        self.offer_id = offer_id


def ensure_several_offers(offers: list[StreamOffer]) -> None:
    if len(offers) < 2:
        raise LastOfferRemovalError()


class LastOfferRemovalError(Exception):
    def __init__(self) -> None:
        super().__init__("The last offer of a stream can't be removed")
