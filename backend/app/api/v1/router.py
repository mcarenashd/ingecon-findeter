from fastapi import APIRouter

from app.api.v1.endpoints import auth, contratos, dashboard, fotos, informes, plan_accion, usuarios

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(dashboard.router)
api_router.include_router(contratos.router)
api_router.include_router(informes.router)
api_router.include_router(fotos.router)
api_router.include_router(plan_accion.router)
api_router.include_router(usuarios.router)
