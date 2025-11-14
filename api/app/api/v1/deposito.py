from app.schemas import ArticuloItem
from sqlalchemy import text
from app.db import engine
from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import Query
from typing import List
router = APIRouter()

@router.get("/deposito/{articulo}", response_model=List[ArticuloItem], tags=["deposito"])
def get_articulos_por_deposito(articulo: str):
    sql = text("""
      SELECT 
        a.ArticulosId 
        , a.ArticulosNombre
        , da.DepositoArticuloID 
        , d.DepositosName
        , ds.DespositoStockId 
        , ds.DepositoStockStockActual 
        , ds.DepositoStockLote 
        , ds.DepositoStockVto 
        FROM [DB_HSB].[dbo].[Articulos] a
        JOIN DepositoArticulo da ON a.ArticulosId = da.DepositoArticuloArticuloId_n 
        JOIN Depositos d ON da.DepositosId = d.DepositosId
        JOIN DepositoStock ds ON ds.DepositoArticuloID =da.DepositoArticuloID 
        JOIN ArticuloSubRubros asr ON asr.ArticulosId = a.ArticulosId
        JOIN ArticulosRubro ar ON ar.ArticulosId = a.ArticulosId 
        WHERE LOWER(a.ArticulosNombre) LIKE LOWER(:pattern)
        
      ORDER BY a.ArticulosId DESC
    """)
    pattern = f"%{articulo.strip()}%"
    with engine.connect() as conn:
        rows = conn.execute(sql, {"pattern": pattern}).mappings().all()
    if not rows:
        raise HTTPException(status_code=404, detail="No se encontraron artículos.")
    return [dict(r) for r in rows]
