from fastapi import FastAPI

from app.routers import campaign_offers, campaigns, lookups

app = FastAPI(title="Keitaro campaign manager")
app.include_router(campaigns.router)
app.include_router(lookups.router)
app.include_router(campaign_offers.router)
