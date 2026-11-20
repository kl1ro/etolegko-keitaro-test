from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app import campaigns
from app.keitaro import Campaign

router = APIRouter()


@router.post("/campaigns", status_code=201)
async def handle_campaign_creation(
    form: campaigns.CampaignForm,
    deps: Annotated[
        campaigns.CreateCampaignDeps,
        Depends(campaigns.get_campaign_creation_deps),
    ],
) -> Campaign:
    return await campaigns.create_campaign(form, deps)


@router.get("/campaigns")
async def handle_campaigns_load(
    deps: Annotated[
        campaigns.LoadCampaignsDeps,
        Depends(campaigns.get_campaigns_load_deps),
    ],
) -> list[Campaign]:
    return await campaigns.load_campaigns(deps)


@router.delete("/campaigns/{campaign_id}", status_code=204)
async def handle_campaign_deletion(
    campaign_id: int,
    deps: Annotated[
        campaigns.DeleteCampaignDeps,
        Depends(campaigns.get_campaign_deletion_deps),
    ],
) -> None:
    try:
        await campaigns.delete_campaign(campaign_id, deps)
    except campaigns.CampaignNotFoundError as error:
        raise HTTPException(404, "Campaign not found") from error
