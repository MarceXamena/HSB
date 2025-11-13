from app.schemas import BajaRequest
from sqlalchemy import text
from app.db import engine
from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import Query
from typing import List
router = APIRouter()
@router.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}

@router.get("/hc/{documento}", tags=["hc"])
def get_hc_por_documento(documento: str):
    sql = text("""
      SELECT 
        h.HCId, h.HCBarCode, h.HC_x_PersonaApellidoNombre,
        h.HC_x_Personanrodocumento, h.HCEstado,
        ch.CajasHCId, ch.CajasHCFechaBaja,
        c.CajasId, c.CajasBC
      FROM HC h
      JOIN CajasHC ch ON h.HCId = ch.HCId
      JOIN Cajas c    ON c.CajasId = ch.CajasId
      WHERE h.HC_x_Personanrodocumento = :doc
        
      ORDER BY h.HCId DESC
    """)
    with engine.connect() as conn:
        row = conn.execute(sql, {"doc": documento}).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="No se encontró el documento.")
    return dict(row)
#async def get_hc_por_documento(documento: str):
#    return {"status": "ok"}

@router.get("/hc", tags=["hc"])
def get_lista_hc_por_documento(hcbarcodes: List[str] = Query(default=[]),
           documento: str | None = None,
           incluir_bajas: bool = False,
           limit: int = Query(100, ge=1, le=1000),
           offset: int = Query(0, ge=0)):
    where, params = [], {"limit": limit, "offset": offset}
    if documento:
        where.append("h.HC_x_Personanrodocumento = :doc")
        params["doc"] = documento
    likes=[]
    for i, bc in enumerate(hcbarcodes):
        likes.append(f"h.HCBarCode LIKE :bc{i}")
        params[f"bc{i}"] = f"%{bc}%"
    if likes: where.append("(" + " OR ".join(likes) + ")")
    if not incluir_bajas: where.append("ch.CajasHCFechaBaja IS NULL")
    where_sql = " WHERE " + " AND ".join(where) if where else ""
    sql = text(f"""
      SELECT h.HCId, h.HCBarCode, h.HC_x_PersonaApellidoNombre,
             h.HC_x_Personanrodocumento, h.HCEstado,
             ch.CajasHCId, ch.CajasHCFechaBaja,
             c.CajasId, c.CajasBC
      FROM HC h
      JOIN CajasHC ch ON h.HCId = ch.HCId
      JOIN Cajas c    ON c.CajasId = ch.CajasId
      {where_sql}
      ORDER BY h.HCId DESC
      OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY
    """)
    with engine.connect() as conn:
        rows = conn.execute(sql, params).mappings().all()
    return [dict(r) for r in rows]

@router.put("/hc/baja", tags=["hc"])
def marcar_baja(data: BajaRequest):
    """
    Marca la HC como 'C' (Cargado) y actualiza CajasHC con fecha y usuario de baja.
    """
    sql = text("""
    BEGIN TRANSACTION;

    UPDATE dbo.HC
    SET HCEstado = 'C'
    WHERE HCId = (
        SELECT TOP 1 HCId FROM dbo.HC WHERE HCBarCode = :barcode
    );

    UPDATE dbo.CajasHC
    SET
        CajasHCFechaBaja = GETDATE(),
        CajasHCUsuarioBaja = :usuario
    WHERE CajasHCId = (
      SELECT ch.CajasHCId 
		  FROM HC h
		  JOIN CajasHC ch ON h.HCId = ch.HCId 
		  JOIN Cajas c ON c.CajasId = ch.CajasId 
		  WHERE
		    h.HCBarCode = :barcode
            AND ch.CajasHCFechaBaja IS NULL
    );

    COMMIT TRANSACTION;
    """)

    try:
        with engine.begin() as conn:
            conn.execute(sql, {
                "barcode": data.HCBarCode,
                "usuario": data.UsuarioBaja,
            })
        return {"success": True, "message": "HC cargada y CajasHC actualizada correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/hc/barcode/{hcbarcode}", tags=["hc"])
async def get_hc_por_barcode(hcbarcode: str):
    sql = text("""
      SELECT TOP 1
        h.HCId, h.HCBarCode, h.HC_x_PersonaApellidoNombre,
        h.HC_x_Personanrodocumento, h.HCEstado,
        ch.CajasHCId, ch.CajasHCFechaBaja,
        c.CajasId, c.CajasBC
      FROM HC h
      JOIN CajasHC ch ON h.HCId = ch.HCId
      JOIN Cajas c    ON c.CajasId = ch.CajasId
      WHERE h.HCBarCode LIKE :pattern
      ORDER BY h.HCId DESC
    """)
    pattern = f"%{hcbarcode.strip()}%"
    with engine.connect() as conn:
        row = conn.execute(sql, {"pattern": pattern}).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="No se encontró el HCBarCode solicitado.")
    return dict(row)