from fastapi import APIRouter

from src.api.routes import age_groups

api_router = APIRouter()
api_router.include_router(age_groups.router, prefix="/age_groups", tags=["Age groups"])
