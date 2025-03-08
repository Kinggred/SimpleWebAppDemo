from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from SWADemo.api.endpoints.authorization import router as auth_router
from SWADemo.api.endpoints.files import router as files_router
from SWADemo.config import settings
from SWADemo.database import create_db_and_tables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter()
api_router.include_router(files_router, prefix="/files", tags=["files"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

app.include_router(api_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
