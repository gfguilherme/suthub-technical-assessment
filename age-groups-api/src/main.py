import logging

from fastapi import FastAPI
from mangum import Mangum

from src.api.main import api_router

logger = logging.getLogger(__name__)

app = FastAPI(root_path="/Prod/")
lambda_handler = Mangum(app)


@app.get("/")
def read_root():
    return {"description": "Age Groups API"}


app.include_router(api_router, prefix="/api/v1")
