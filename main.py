from fastapi import FastAPI
from app.database import engine, Base
from app.routers import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinTrack API",
    description="API para seguimiento de finanzas personales",
    version="1.0.0"
)

app.include_router(router)