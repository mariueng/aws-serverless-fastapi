from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings
import os

load_dotenv()

ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))
PORT = int(os.getenv("PORT", 8000))
ENTSOE_API_KEY = os.getenv("ENTSOE_API_KEY")
API_KEYS = CommaSeparatedStrings(os.getenv("API_KEYS", ""))
API_PREFIX = "api"
API_VERSION = "v1"
PROJECT_NAME = "AWS Serverless FastAPI"
DEBUG = os.getenv("DEBUG", "False")