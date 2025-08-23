from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.db.database import Base, engine
from api.utils.logging_config import setup_logging
from api.v1.routes import api_version_one

# Create all database tables
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup tasks before starting the application
    # e.g., connecting to databases, initializing resources
    yield
    # Cleanup tasks before shutting down the application
    # e.g., closing database connections, releasing resources


# Setup logging configuration
setup_logging()

app = FastAPI(
    title="FastAPI Web",
    description="This is the API documentation for the FastAPI Web Project.",
    version="0.1.0",
    lifespan=lifespan,
    contact={
        "name": "Seyi Pythonian",
        "url": "https://www.github.com/Pythonian/fastapi_web",
        "email": "seyipythonian@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS settings
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API version 1 router
app.include_router(api_version_one)


# Root endpoint
@app.get("/", tags=["Home"], response_class=JSONResponse)
async def get_root(request: Request) -> JSONResponse:
    return JSONResponse(
        {
            "message": "Welcome to My API",
            "URL": request.url._url,
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
