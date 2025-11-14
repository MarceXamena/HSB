from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Re-exportar desde los módulos del paquete
from .hc import HCItem, DocRequest, BajaRequest
from .deposito import ArticuloItem, ArticulosRequest

__all__ = [
    "HCItem",
    "DocRequest", 
    "BajaRequest",
    "ArticuloItem",
    "ArticulosRequest",
]