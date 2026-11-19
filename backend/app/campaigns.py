from __future__ import annotations

import asyncio
from typing import Annotated, TypedDict

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.database import open_session
from app.dependencies import get_keitaro
from app.keitaro import (
    Campaign,
    CampaignDraft,
    Keitaro,
    StreamDraft,
    StreamFilter,
    StreamOffer,
)
from app.settings import get_settings


def get_campaign_creation_deps(
    keitaro: Annotated[Keitaro, Depends(get_keitaro)],
    database: Annotated[AsyncSession, Depends(open_session)],
) -> CreateCampaignDeps:
    return {
        "keitaro": keitaro,
        "database": database,
        "campaign_prefix": get_settings().campaign_prefix,
    }


async def create_campaign(form: CampaignForm, deps: CreateCampaignDeps) -> Campaign:
    draft = get_campaign_draft(form, deps)
    campaign = await deps["keitaro"].create_campaign(draft)
    await complete_campaign_or_delete(campaign, form, deps)
    return campaign


class CampaignForm(BaseModel):
    name: str
    country: str
    offer_id: int
    domain_id: int
    group_id: int
    traffic_source_id: int


class CreateCampaignDeps(TypedDict):
    keitaro: Keitaro
    database: AsyncSession
    campaign_prefix: str


def get_campaign_draft(form: CampaignForm, deps: GetCampaignDraftDeps) -> CampaignDraft:
    return CampaignDraft(
        name=f"{deps['campaign_prefix']}{form.name}",
        type="position",
        group_id=form.group_id,
        traffic_source_id=form.traffic_source_id,
        domain_id=form.domain_id,
    )


class GetCampaignDraftDeps(TypedDict):
    campaign_prefix: str


async def complete_campaign_or_delete(
    campaign: Campaign,
    form: CampaignForm,
    deps: CompleteCampaignOrDeleteDeps,
) -> None:
    try:
        await create_campaign_streams(campaign, form, deps)
        await save_campaign(campaign, deps)
    except Exception:
        await deps["keitaro"].delete_campaign(campaign.id)
        raise


class CompleteCampaignOrDeleteDeps(TypedDict):
    keitaro: Keitaro
    database: AsyncSession


async def create_campaign_streams(
    campaign: Campaign,
    form: CampaignForm,
    deps: CreateCampaignStreamsDeps,
) -> None:
    country_stream = get_country_stream_draft(campaign, form.country)
    offer_stream = get_offer_stream_draft(campaign, form.offer_id)

    await asyncio.gather(
        deps["keitaro"].create_stream(country_stream),
        deps["keitaro"].create_stream(offer_stream),
    )


class CreateCampaignStreamsDeps(TypedDict):
    keitaro: Keitaro


async def save_campaign(campaign: Campaign, deps: SaveCampaignDeps) -> None:
    deps["database"].add(models.Campaign(id=campaign.id))
    await deps["database"].commit()


class SaveCampaignDeps(TypedDict):
    database: AsyncSession


def get_country_stream_draft(campaign: Campaign, country: str) -> StreamDraft:
    return StreamDraft(
        campaign_id=campaign.id,
        type="regular",
        name=f"{country} to Google",
        position=1,
        action_schema="redirect",
        action_type="http",
        action_payload=GOOGLE_URL,
        filters=[StreamFilter(name="country", mode="accept", payload=[country])],
    )


GOOGLE_URL = "https://www.google.com"


def get_offer_stream_draft(campaign: Campaign, offer_id: int) -> StreamDraft:
    return StreamDraft(
        campaign_id=campaign.id,
        type="default",
        name="Offer",
        position=2,
        action_schema="landings",
        action_type="",
        offers=[StreamOffer(offer_id=offer_id, share=100)],
    )
