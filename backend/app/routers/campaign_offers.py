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
