from fastapi import FastAPI, Response
from dotenv import load_dotenv

from app.api.api_v1.api import router as api_router
from mangum import Mangum


load_dotenv()

app = FastAPI(title="Price API 🚀", description="API for fetching electricity prices, currencies, etc.")


@app.get("/")
async def fastapi_serverless():
    """
    Fastapi serverless API for various data sources. Contact owner for 🔑.
    """
    return Response(content="Contact owner for 🔑 ಠ_ಠ", status_code=200)


app.include_router(api_router, prefix="/api/v1")  # Need this
handler = Mangum(app)
