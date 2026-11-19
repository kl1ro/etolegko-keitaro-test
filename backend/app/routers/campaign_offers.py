from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app import campaign_offers
from app.keitaro import StreamOffer

router = APIRouter()


@router.get("/campaigns/{campaign_id}/offers")
async def handle_campaign_offers_load(
    campaign_id: int,
    deps: Annotated[
        campaign_offers.LoadCampaignOffersDeps,
        Depends(campaign_offers.get_campaign_offers_load_deps),
    ],
) -> list[StreamOffer]:
    try:
        return await campaign_offers.load_campaign_offers(campaign_id, deps)
    except campaign_offers.OfferStreamNotFoundError as error:
        raise HTTPException(404, "Campaign has no offer stream") from error


@router.post("/campaigns/{campaign_id}/offers/{offer_id}")
async def handle_campaign_offer_addition(
    campaign_id: int,
    offer_id: int,
    deps: Annotated[
        campaign_offers.AddCampaignOfferDeps,
        Depends(campaign_offers.get_campaign_offer_addition_deps),
    ],
) -> list[StreamOffer]:
    try:
        return await campaign_offers.add_campaign_offer(campaign_id, offer_id, deps)
    except campaign_offers.OfferStreamNotFoundError as error:
        raise HTTPException(404, "Campaign has no offer stream") from error
    except campaign_offers.OfferAlreadyInStreamError as error:
        raise HTTPException(409, "Offer is already in the campaign") from error


@router.delete("/campaigns/{campaign_id}/offers/{offer_id}")
async def handle_campaign_offer_removal(
    campaign_id: int,
    offer_id: int,
    deps: Annotated[
        campaign_offers.RemoveCampaignOfferDeps,
        Depends(campaign_offers.get_campaign_offer_removal_deps),
    ],
) -> list[StreamOffer]:
    try:
        return await campaign_offers.remove_campaign_offer(campaign_id, offer_id, deps)
    except campaign_offers.OfferStreamNotFoundError as error:
        raise HTTPException(404, "Campaign has no offer stream") from error
    except campaign_offers.OfferNotInStreamError as error:
        raise HTTPException(404, "Offer is not in the campaign") from error
    except campaign_offers.LastOfferRemovalError as error:
        raise HTTPException(409, "The last offer can't be removed") from error
