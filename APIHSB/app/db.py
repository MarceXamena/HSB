# app/db.py
import os, urllib.parse
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("MSSQL_USER")
PWD  = os.getenv("MSSQL_PASSWORD")
HOST = os.getenv("MSSQL_HOST", "localhost")
PORT = os.getenv("MSSQL_PORT", "1433")
DB   = os.getenv("MSSQL_DB", "DB_HSB")
DRV  = os.getenv("MSSQL_DRIVER", "ODBC Driver 18 for SQL Server")  # Debe coincidir con `odbcinst -q -d`
TRUST= os.getenv("MSSQL_TRUST_CERT", "yes")

odbc_str = (
    f"Driver={{{DRV}}};"
    f"Server={HOST},{PORT};"
    f"Database={DB};"
    f"Uid={USER};Pwd={PWD};"
    "Encrypt=yes;"
    f"TrustServerCertificate={'yes' if TRUST.lower()=='yes' else 'no'};"
    "Connection Timeout=30;"
)

conn_str = "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(odbc_str)
engine = create_engine(conn_str, pool_pre_ping=True, future=True)

def ping():
    with engine.connect() as c:
        c.execute(text("SELECT 1"))
