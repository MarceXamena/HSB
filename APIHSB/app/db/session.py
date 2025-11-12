from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings

# Crear engine asíncrono (para SQL Server con aioodbc)
engine = create_async_engine(
    settings.DATABASE_URL_ASYNC,
    echo=False,         # podés poner True para debug
    pool_pre_ping=True, # evita conexiones muertas
    future=True
)

# Fábrica de sesiones asíncronas
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency para FastAPI
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

