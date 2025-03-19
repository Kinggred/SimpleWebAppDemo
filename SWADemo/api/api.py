import logging

from fastapi import APIRouter, FastAPI, Request, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from SWADemo.api.endpoints.authorization import router as auth_router
from SWADemo.api.endpoints.files import router as files_router
from SWADemo.config import settings

logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
app = FastAPI(
    debug=True,
    docs_url="/docs",
    openapi_url="/openapi.json",
    servers=[{"url": settings.LAMBDA_PATH, "description": "AWS Lambda"}],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter()
api_router.include_router(files_router, prefix="/files", tags=["files"])
api_router.include_router(auth_router, tags=["auth"])

app.include_router(api_router)
