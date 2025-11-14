from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import settings
from app.api.v1.hc import router as hc_router
from app.api.v1.deposito import router as deposito_router

app = FastAPI(title="HSB API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)
app.include_router(hc_router, prefix="/api/v1")
app.include_router(deposito_router, prefix="/api/v1")