from fastapi import FastAPI
from .database import init_db
from .api.routes.logs import router as logs_router
from .api.routes.analytics import router as analytics_router
from .api.routes.alerts import router as alerts_router
from .config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    @app.on_event("startup")
    def _startup():
        init_db()

    @app.get("/health")
    def health():
        return {"status": "ok"}

    app.include_router(logs_router)
    app.include_router(analytics_router)
    app.include_router(alerts_router)

    return app


app = create_app()

