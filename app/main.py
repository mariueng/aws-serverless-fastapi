from fastapi import Depends, FastAPI
from dotenv import load_dotenv

from app.api.api_v1.api import router as api_router
from mangum import Mangum


load_dotenv()

app = FastAPI()


@app.get("/")
async def fastapi_serverless():
    """
    Fastapi serverless API for various data sources.
    """
    return "Contact owner for 🔑"


app.include_router(api_router, prefix="/api/v1")
handler = Mangum(app)
