from fastapi import APIRouter

from app.routers.v1 import cliente_routes, test_routes


api_router_v1 = APIRouter()

api_router_v1.include_router(test_routes.router)
api_router_v1.include_router(cliente_routes.router)