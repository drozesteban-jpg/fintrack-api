from fastapi import FastAPI
from app.database import engine, Base
from app.routers import router
from app.auth_router import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinTrack API",
    description="API para seguimiento de finanzas personales",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(router)
