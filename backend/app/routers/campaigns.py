from typing import Annotated, TypedDict

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import campaigns
from app.database import open_session
from app.dependencies import get_keitaro
from app.keitaro import Campaign, Keitaro
from app.settings import get_settings

router = APIRouter()


@router.post("/campaigns", status_code=201)
async def handle_campaign_creation(
    form: campaigns.CampaignForm,
    keitaro: Annotated[Keitaro, Depends(get_keitaro)],
    database: Annotated[AsyncSession, Depends(open_session)],
) -> Campaign:
    deps: CampaignCreationDeps = {
        "keitaro": keitaro,
        "database": database,
        "campaign_prefix": get_settings().campaign_prefix,
    }

    campaign = await campaigns.create_campaign(form, deps)
    await campaigns.save_campaign(campaign, deps)
    return campaign


class CampaignCreationDeps(TypedDict):
    keitaro: Keitaro
    database: AsyncSession
    campaign_prefix: str
