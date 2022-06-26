import uvicorn
import logging

from fastapi import FastAPI
from mangum import Mangum

from app.core.config import DEBUG, API_PREFIX, API_VERSION
from app.api.v1.api import router as api_router

# Start application
app = FastAPI(
    title="Price API 🚀",
    description="API for fetching electricity prices, currencies, etc.",
    debug=DEBUG
)
app.include_router(api_router, prefix=f"/{API_PREFIX}/{API_VERSION}")

@app.on_event("startup")
def configure_logger():
    # Customize logging
    logger = logging.getLogger("uvicorn.access")
    console_formatter = uvicorn.logging.AccessFormatter(
        fmt="%(levelprefix)s %(asctime)s | %(request_line)s [%(status_code)s]",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="%",
        use_colors=True
    )
    logger.handlers[0].setFormatter(console_formatter)


# Initialize Mangum adapter
handler = Mangum(app, lifespan="off")


@app.get("/")
async def fastapi_serverless():
    """
    Fastapi serverless API for various data sources. Contact owner for 🔑.
    """
    return "Contact owner for 🔑 ಠ_ಠ"
