import os
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, Query, Body, HTTPException, Form
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

USER = os.getenv("MSSQL_USER")
PWD = os.getenv("MSSQL_PASSWORD")
HOST = os.getenv("MSSQL_HOST", "localhost")
PORT = os.getenv("MSSQL_PORT", "1433")
DB   = os.getenv("MSSQL_DB", "DB_HSB")
DRV  = os.getenv("MSSQL_DRIVER", "ODBC Driver 18 for SQL Server")
TRUST= os.getenv("MSSQL_TRUST_CERT", "yes")  # yes|no

# Cadena de conexión (pyodbc)
odbc_raw = (
    f"Driver={{{DRV}}};"
    f"Server={HOST},{PORT};"
    f"Database={DB};"
    f"Uid={USER};Pwd={PWD};"
    "Encrypt=yes;"
    f"TrustServerCertificate={'yes' if TRUST.lower()=='yes' else 'no'};"
    "Connection Timeout=30;"
)
conn_str = "mssql+pyodbc:///?odbc_connect=" + quote_plus(odbc_raw)

engine = create_engine(conn_str, pool_pre_ping=True)

app = FastAPI(title="HSB API", version="1.0.0")


class HCItem(BaseModel):
    HCId: Optional[int] = None
    HCBarCode: Optional[str] = None
    HC_x_PersonaApellidoNombre: Optional[str] = None
    HC_x_Personanrodocumento: Optional[str] = None
    HCEstado: Optional[str] = None
    CajasHCId: Optional[int] = None
    CajasHCFechaBaja: Optional[datetime] = None
    CajasId: Optional[int] = None
    CajasBC: Optional[str] = None


@app.get("/doc", response_model=List[HCItem])
def get_hc(
    hcbarcodes: List[str] = Query(
        default=[],
        description="Lista de patrones para HCBarCode (se usa LIKE %%patrón%%). Repetir el parámetro para múltiples valores."
    ),
    documento: Optional[str] = Query(
        default=None,
        description="Filtrar por h.HC_x_Personanrodocumento (igualdad exacta)."
    ),
    incluir_bajas: bool = Query(
        default=False,
        description="Si true, incluye registros con ch.CajasHCFechaBaja no nula."
    ),
    limit: int = Query(default=200, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
):
    """
    Devuelve los registros de HC + CajasHC + Cajas con filtros opcionales.
    """
    where_clauses = []
    params = {}

    # Filtro por documento (opcional)
    if documento:
        where_clauses.append("h.HC_x_Personanrodocumento = :doc")
        params["doc"] = documento

    # Filtro por lista de barcodes (LIKE %...%)
    like_clauses = []
    for i, bc in enumerate(hcbarcodes):
        key = f"bc{i}"
        like_clauses.append(f"h.HCBarCode LIKE :{key}")
        params[key] = f"%{bc}%"
    if like_clauses:
        where_clauses.append("(" + " OR ".join(like_clauses) + ")")

    # Excluir bajas por defecto
    if not incluir_bajas:
        where_clauses.append("ch.CajasHCFechaBaja IS NULL")

    where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    # Consulta base (tu SELECT)
    base_sql = f"""
    SELECT
        h.HCId,
        h.HCBarCode,
        h.HC_x_PersonaApellidoNombre,
        h.HC_x_Personanrodocumento,
        h.HCEstado,
        ch.CajasHCId,
        ch.CajasHCFechaBaja,
        c.CajasId,
        c.CajasBC
    FROM [DB_HSB].[dbo].[HC] h
    JOIN CajasHC ch ON h.HCId = ch.HCId
    JOIN Cajas c     ON c.CajasId = ch.CajasId
    {where_sql}
    ORDER BY h.HCId DESC
    OFFSET :offset ROWS
    FETCH NEXT :limit ROWS ONLY
    """

    params["offset"] = offset
    params["limit"] = limit

    with engine.connect() as conn:
        rows = conn.execute(text(base_sql), params).mappings().all()

    return [dict(row) for row in rows]





@app.get("/barcode/{hcbarcode}", response_model=HCItem)
def get_barcode_unique(hcbarcode: str):
    sql = text(
        """
        SELECT TOP 1
            h.HCId,
            h.HCBarCode,
            h.HC_x_PersonaApellidoNombre,
            h.HC_x_Personanrodocumento,
            h.HCEstado,
            ch.CajasHCId,
            ch.CajasHCFechaBaja,
            c.CajasId,
            c.CajasBC
        FROM [DB_HSB].[dbo].[HC] h
        JOIN CajasHC ch ON h.HCId = ch.HCId
        JOIN Cajas c     ON c.CajasId = ch.CajasId
        WHERE h.HCBarCode = :bc
          AND ch.CajasHCFechaBaja IS NULL
        ORDER BY h.HCId DESC
        """
    )
    with engine.connect() as conn:
        row = conn.execute(sql, {"bc": hcbarcode}).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="No se encontró el HCBarCode indicado.")
    return dict(row)
