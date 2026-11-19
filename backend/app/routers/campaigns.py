from typing import Annotated

from fastapi import APIRouter, Depends

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
