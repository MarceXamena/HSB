import sqlalchemy as sa
from app.db.base import Base

class HC(Base):
    __tablename__ = "HC"
    HCId = sa.Column(sa.Integer, primary_key=True)
    HCBarCode = sa.Column(sa.String(255))
    HC_x_PersonaApellidoNombre = sa.Column(sa.String(255))
    HC_x_Personanrodocumento = sa.Column(sa.String(255))
    HCEstado = sa.Column(sa.String(255))
    CajasHCId = sa.Column(sa.Integer)
    CajasHCFechaBaja = sa.Column(sa.DateTime)
    CajasId = sa.Column(sa.Integer)
    CajasBC = sa.Column(sa.String(255))