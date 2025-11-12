from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus

class Settings(BaseSettings):
    ENV: str = "dev"
    MSSQL_USER: str
    MSSQL_PASSWORD: str
    MSSQL_HOST: str
    MSSQL_PORT: int = 1433
    MSSQL_DB: str
    MSSQL_DRIVER: str = "ODBC Driver 18 for SQL Server"
    MSSQL_TRUST_CERT: str = "yes"

    @property
    def DATABASE_URL_ASYNC(self) -> str:
        conn = (f"Driver={self.MSSQL_DRIVER};"
                f"Server={self.MSSQL_HOST},{self.MSSQL_PORT};"
                f"Database={self.MSSQL_DB};"
                f"UID={self.MSSQL_USER};PWD={self.MSSQL_PASSWORD};"
                f"TrustServerCertificate={self.MSSQL_TRUST_CERT};")
        return f"mssql+aioodbc:///?odbc_connect={quote_plus(conn)}"

    @property
    def DATABASE_URL_SYNC(self) -> str:
        conn = (f"Driver={self.MSSQL_DRIVER};"
                f"Server={self.MSSQL_HOST},{self.MSSQL_PORT};"
                f"Database={self.MSSQL_DB};"
                f"UID={self.MSSQL_USER};PWD={self.MSSQL_PASSWORD};"
                f"TrustServerCertificate={self.MSSQL_TRUST_CERT};")
        return f"mssql+pyodbc:///?odbc_connect={quote_plus(conn)}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
