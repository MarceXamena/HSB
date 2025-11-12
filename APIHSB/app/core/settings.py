from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus

class Settings(BaseSettings):
    # Ambiente
    ENV: str = "dev"

    # Configuración SQL Server
    MSSQL_USER: str
    MSSQL_PASSWORD: str
    MSSQL_HOST: str
    MSSQL_PORT: int = 1433
    MSSQL_DB: str
    MSSQL_DRIVER: str = "ODBC Driver 18 for SQL Server"
    MSSQL_TRUST_CERT: str = "yes"

    # === URL de conexión asíncrona (para FastAPI / SQLAlchemy async) ===
    @property
    def DATABASE_URL_ASYNC(self) -> str:
        """
        Retorna la cadena de conexión async (usada por create_async_engine)
        Ejemplo:
        mssql+aioodbc:///?odbc_connect=DRIVER%3DODBC%20Driver%2018%20for%20SQL%20Server%3B...
        """
        conn_str = (
            f"Driver={self.MSSQL_DRIVER};"
            f"Server={self.MSSQL_HOST},{self.MSSQL_PORT};"
            f"Database={self.MSSQL_DB};"
            f"UID={self.MSSQL_USER};"
            f"PWD={self.MSSQL_PASSWORD};"
            f"TrustServerCertificate={self.MSSQL_TRUST_CERT};"
        )
        return f"mssql+aioodbc:///?odbc_connect={quote_plus(conn_str)}"

    # === URL de conexión síncrona (para Alembic) ===
    @property
    def DATABASE_URL_SYNC(self) -> str:
        """
        Retorna la cadena de conexión sync (usada por Alembic)
        """
        conn_str = (
            f"Driver={self.MSSQL_DRIVER};"
            f"Server={self.MSSQL_HOST},{self.MSSQL_PORT};"
            f"Database={self.MSSQL_DB};"
            f"UID={self.MSSQL_USER};"
            f"PWD={self.MSSQL_PASSWORD};"
            f"TrustServerCertificate={self.MSSQL_TRUST_CERT};"
        )
        return f"mssql+pyodbc:///?odbc_connect={quote_plus(conn_str)}"

    # Configuración de archivo .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


# Instancia global (importar desde otros módulos)
settings = Settings()
