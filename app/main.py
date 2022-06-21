from fastapi import FastAPI

from app.api.v1.api import router as api_router
from mangum import Mangum

app = FastAPI(title="Price API 🚀", description="API for fetching electricity prices, currencies, etc.")


@app.get("/")
async def fastapi_serverless():
    """
    Fastapi serverless API for various data sources. Contact owner for 🔑.
    """
    return "Contact owner for 🔑 ಠ_ಠ"


app.include_router(api_router, prefix="/api/v1")  # Need this
handler = Mangum(app, lifespan="off")
