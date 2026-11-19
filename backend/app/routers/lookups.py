from typing import Annotated

from fastapi import APIRouter, Depends

from app.keitaro import (
    CampaignGroup,
    Domain,
    Keitaro,
    Offer,
    TrafficSource,
    get_keitaro,
)

router = APIRouter()
KeitaroDependency = Annotated[Keitaro, Depends(get_keitaro)]


@router.get("/offers")
async def handle_offers_load(
    keitaro: KeitaroDependency,
) -> list[Offer]:
    return await keitaro.load_offers()


@router.get("/domains")
async def handle_domains_load(
    keitaro: KeitaroDependency,
) -> list[Domain]:
    return await keitaro.load_domains()


@router.get("/campaign-groups")
async def handle_campaign_groups_load(
    keitaro: KeitaroDependency,
) -> list[CampaignGroup]:
    return await keitaro.load_campaign_groups()


@router.get("/traffic-sources")
async def handle_traffic_sources_load(
    keitaro: KeitaroDependency,
) -> list[TrafficSource]:
    return await keitaro.load_traffic_sources()
