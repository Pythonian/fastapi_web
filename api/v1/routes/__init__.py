"""Router configuration.

This module sets up the routing for the API version, including the necessary
routers for various modules. To add a new router to this configuration, follow
the example below:

Example:
    1. Import the new router:
       from api.v1.routes.new_module import new_router

    2. Include the router in the `api_version_one` router:
       api_version_one.include_router(new_router)

Usage:
    This configuration is included in the `main.py` application router to
    make the API version endpoints available.

Example:
        from fastapi import FastAPI
        from api.v1.routes import api_version_one

        app = FastAPI()
        app.include_router(api_version_one)
"""

from fastapi import APIRouter

from api.v1.routes.blog import blog

api_version_one = APIRouter(prefix="/api/v1")

api_version_one.include_router(blog)
