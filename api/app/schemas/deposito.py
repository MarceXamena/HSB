from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ArticuloItem(BaseModel):
    ArticulosId: Optional[int] = None
    SubRubrosId: Optional[int] = None
    ArticulosRubroId_n: Optional[int] = None
    ArticulosNombre: Optional[str] = None
    DepositoArticuloID: Optional[int] = None
    DepositosName: Optional[str] = None
    DespositoStockId: Optional[int] = None
    DepositoStockStockActual: Optional[int] = None
    DepositoStockLote: Optional[str] = None
    DepositoStockVto: Optional[datetime] = None

class ArticulosRequest(BaseModel):
    ArticulosNombre: str

#class BajaRequest(BaseModel):
#    HCBarCode: str
#    CajasHCId: Optional[int] = None
#    UsuarioBaja: Optional[int] = None