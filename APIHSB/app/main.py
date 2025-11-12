# app/main.py
'''from fastapi import FastAPI
from app.db import ping
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="HSB API", version="1.0.0")

@app.on_event("startup")
def _startup(): ping()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # agrega tu frontend/dom
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.get("/health")
def health(): return {"ok": True}

app.include_router(router)

'''
from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
