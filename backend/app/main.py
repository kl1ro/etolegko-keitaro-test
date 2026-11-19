from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.http import RequestRejectedError
from app.routers import campaign_offers, campaigns, lookups

app = FastAPI(title="Keitaro campaign manager")
app.include_router(campaigns.router)
app.include_router(lookups.router)
app.include_router(campaign_offers.router)


@app.exception_handler(RequestRejectedError)
async def handle_request_rejection(
    request: Request,
    error: RequestRejectedError,
) -> JSONResponse:
    return JSONResponse(status_code=error.status_code, content={"detail": error.body})
