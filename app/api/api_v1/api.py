from fastapi import APIRouter, Depends
from app.api.api_v1.endpoints import crypto_xr, currency_xr
from app.core.security import api_key_auth

from .endpoints import elprice

_prefix = "/prices"

router = APIRouter()
router.include_router(elprice.router, prefix=_prefix, tags=["Electricit prices ⚡️"], dependencies=[Depends(api_key_auth)])
router.include_router(currency_xr.router, prefix=_prefix, tags=["Currency XR 💰"])
router.include_router(crypto_xr.router, prefix=_prefix, tags=["Currency XR 💰"])
