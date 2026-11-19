from __future__ import annotations

import asyncio
import secrets
from typing import Annotated, TypedDict

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.database import open_session
from app.keitaro import (
    Campaign,
    CampaignDraft,
    Keitaro,
    StreamDraft,
    StreamFilter,
    StreamOffer,
    get_keitaro,
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
    inner_deps: CreateCampaignInnerDeps = {**deps, "form": form}

    draft = get_campaign_draft(form, inner_deps)
    campaign = await inner_deps["keitaro"].create_campaign(draft)

    try:
        await create_campaign_streams(campaign, inner_deps)
        await save_campaign(campaign, inner_deps)
    except Exception:
        await inner_deps["keitaro"].delete_campaign(campaign.id)
        raise

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


class CreateCampaignInnerDeps(TypedDict):
    keitaro: Keitaro
    database: AsyncSession
    campaign_prefix: str
    form: CampaignForm


def get_campaign_draft(form: CampaignForm, deps: GetCampaignDraftDeps) -> CampaignDraft:
    return CampaignDraft(
        alias=generate_campaign_alias(),
        name=f"{deps['campaign_prefix']}{form.name}",
        type="position",
        group_id=form.group_id,
        traffic_source_id=form.traffic_source_id,
        domain_id=form.domain_id,
    )


class GetCampaignDraftDeps(TypedDict):
    campaign_prefix: str


async def create_campaign_streams(
    campaign: Campaign,
    deps: CreateCampaignStreamsDeps,
) -> None:
    country_stream = get_country_stream_draft(campaign, deps["form"].country)
    offer_stream = get_offer_stream_draft(campaign, deps["form"].offer_id)

    await asyncio.gather(
        deps["keitaro"].create_stream(country_stream),
        deps["keitaro"].create_stream(offer_stream),
    )


class CreateCampaignStreamsDeps(TypedDict):
    keitaro: Keitaro
    form: CampaignForm


async def save_campaign(campaign: Campaign, deps: SaveCampaignDeps) -> None:
    deps["database"].add(models.Campaign(id=campaign.id))
    await deps["database"].commit()


class SaveCampaignDeps(TypedDict):
    database: AsyncSession


def generate_campaign_alias() -> str:
    return secrets.token_hex(CAMPAIGN_ALIAS_BYTES)


CAMPAIGN_ALIAS_BYTES = 4


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
        action_type="http",
        offers=[StreamOffer(offer_id=offer_id, share=100)],
    )


def get_campaigns_load_deps(
    keitaro: Annotated[Keitaro, Depends(get_keitaro)],
    database: Annotated[AsyncSession, Depends(open_session)],
) -> LoadCampaignsDeps:
    return {"keitaro": keitaro, "database": database}


async def load_campaigns(deps: LoadCampaignsDeps) -> list[Campaign]:
    campaign_ids = await load_saved_campaign_ids(deps)
    campaigns = await load_keitaro_campaigns(campaign_ids, deps)
    return campaigns


class LoadCampaignsDeps(TypedDict):
    keitaro: Keitaro
    database: AsyncSession


async def load_saved_campaign_ids(deps: LoadSavedCampaignIdsDeps) -> list[int]:
    query = select(models.Campaign.id).order_by(models.Campaign.created_at)
    result = await deps["database"].scalars(query)
    campaign_ids = list(result)
    return campaign_ids


class LoadSavedCampaignIdsDeps(TypedDict):
    database: AsyncSession


async def load_keitaro_campaigns(
    campaign_ids: list[int],
    deps: LoadKeitaroCampaignsDeps,
) -> list[Campaign]:
    campaigns = await asyncio.gather(
        *(deps["keitaro"].load_campaign(campaign_id) for campaign_id in campaign_ids),
    )

    return list(campaigns)


class LoadKeitaroCampaignsDeps(TypedDict):
    keitaro: Keitaro
