from fastapi import APIRouter
from .endpoints import employers

api_router = APIRouter()
api_router.include_router(employers.router, prefix="/employers", tags=["employers"])
