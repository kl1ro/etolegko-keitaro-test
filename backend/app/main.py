from fastapi import FastAPI

from app.routers import campaigns, lookups

app = FastAPI(title="Keitaro campaign manager")
app.include_router(campaigns.router)
app.include_router(lookups.router)
