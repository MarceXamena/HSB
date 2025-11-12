from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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

class DocRequest(BaseModel):
    documento: str

class BajaRequest(BaseModel):
    HCBarCode: str
    CajasHCId: Optional[int] = None
    UsuarioBaja: Optional[int] = None