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
    description="A robust, user-centric To Do API.",
    version="1.0.0",
    lifespan=lifespan
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"message": "Oops! We couldn't find what you were looking for. Please check ID and try again."}
        )
    if exc.status_code == 401:
        # If the error has a specific message (like from login), use it.
        # Otherwise, use the friendly default for missing auth.
        message = exc.detail
        if message in ["Not authenticated", "Unauthorized", None]:
             message = "Hold up! You need to be logged in to do that."
             
        return JSONResponse(
            status_code=401,
            content={"message": message}
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # Get the first error message to keep it clean and human-friendly
    error = exc.errors()[0]
    field = error.get('loc', ['unknown'])[-1]
    msg = error.get('msg', 'Invalid input')
    
    return JSONResponse(
        status_code=422,
        content={"message": f"Whoops! There's an issue with the '{field}': {msg}."}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    # Log the error here in a real app
    print(f"INTERNAL ERROR: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Oh no! Something went wrong on our end. Please try again later."}
    )

@app.get("/")
async def root():
    return {"message": "Welcome to Smart To Do API"}

app.include_router(api_router, prefix="/api/v1")
