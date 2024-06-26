from fastapi import APIRouter

from src.api.routes import enrollment

api_router = APIRouter()
api_router.include_router(enrollment.router, prefix="/enrollments", tags=["Enrollment"])
