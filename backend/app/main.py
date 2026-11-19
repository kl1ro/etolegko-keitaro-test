from fastapi import FastAPI

from app.routers import campaigns

app = FastAPI(title="Keitaro campaign manager")
app.include_router(campaigns.router)
