from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.v1.api import api_router
from core.config import settings
from db.mongodb import init_db
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A robust, human-centric To Do API.",
    version="1.0.0",
    lifespan=lifespan
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"message": "Oops! We couldn't find what you were looking for. Please check the URL or ID and try again."}
        )
    if exc.status_code == 401:
        return JSONResponse(
            status_code=401,
            content={"message": "Hold up! You need to be logged in to do that."}
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)}
    )

@app.get("/")
async def root():
    return {"message": "Welcome to Smart To Do API"}

app.include_router(api_router, prefix="/api/v1")
