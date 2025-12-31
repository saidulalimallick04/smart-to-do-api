from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from api.v1.api import api_router
from core.config import settings
from db.mongodb import init_db
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.openapi.docs import get_redoc_html

templates = Jinja2Templates(directory="templates")

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

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("templates/favicon.ico")


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Redoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
    )

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    context = {
        "request": request,
        "project_name": "Smart To Do API",
        "project_version": "v1.0.0",
        "project_description": "A robust, user-centric To Do API suitable for modern applications.",
        "project_keywords": "fastapi, mongodb, beanie, jwt, python, async, smart-todo",
        "project_repo_url": "https://github.com/saidulalimallick04/smart-to-do-api",
        "developers": [
            {
                "name": "Saidul Ali Mallick",
                "username": "saidulalimallick04",
                "role": "Backend Developer & AI Engineer",
                "quote": "Building impact, not just code.",
                "github_url": "https://github.com/saidulalimallick04",
                "linkedin_url": "https://linkedin.com/in/saidulalimallick04",
                "twitter_url": "https://x.com/saidulmallick04"
            }
        ],
        "hero_badge_text": "Production Ready",
        "hero_title": "Smart To Do API",
        "hero_description": "A robust, user-centric backend designed for modern applications. Powered by FastAPI, MongoDB (Beanie), and Context-Aware AI.",
        "api_total_endpoints": "9+",
        "api_get_count": 3,
        "api_post_count": 4,
        "api_put_count": 1,
        "api_delete_count": 1,
        "about_description": "Use this in your next project to have a solid, secure, and smart task management backend out of the box.",
        "tech_stack": [
            {"icon": "fab fa-python", "name": "Python"},
            {"icon": "fas fa-bolt", "name": "FastAPI"},
            {"icon": "fas fa-database", "name": "MongoDB"},
            {"icon": "fas fa-leaf", "name": "Beanie"},
            {"icon": "fas fa-key", "name": "JWT"},
        ],
        "quick_links": [
            {"icon": "fas fa-book", "name": "API Docs", "url": "/docs"},
            {"icon": "fab fa-github", "name": "Repository", "url": "https://github.com/saidulalimallick04/smart-to-do-api"},
        ],
        "server_status": "Operational",
        "server_api_status": "Healthy",
        "server_db_status": "Connected",
        "developer_name": "Saidul Ali Mallick"
    }
    return templates.TemplateResponse("index_jinja.html", context)

app.include_router(api_router, prefix="/api/v1")
