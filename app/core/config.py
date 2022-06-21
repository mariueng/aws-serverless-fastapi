from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings
import os

load_dotenv()

ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))
ENTSOE_API_KEY = os.getenv("ENTSOE_API_KEY")
API_KEYS = CommaSeparatedStrings(os.getenv("API_KEYS", ""))
API_V1_STR = "/api/v1"
PROJECT_NAME = "FastAPI-AWS-Lambda-Example-API"