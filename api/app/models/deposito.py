import sqlalchemy as sa
from app.db.base import Base

class Deposito(Base):
    __tablename__ = 'deposito'

    ArticulosId = sa.Column(sa.Integer, primary_key=True)
    ArticulosNombre = sa.Column(sa.String(255))
    SubRubrosId = sa.Column(sa.Integer)
    ArticulosRubroId_n = sa.Column(sa.Integer)
    DepositoArticuloID = sa.Column(sa.Integer)
    DepositosName = sa.Column(sa.String(255))
    DespositoStockId  = sa.Column(sa.Integer)
    DepositoStockStockActual = sa.Column(sa.Numeric(8, 2))
    DepositoStockLote = sa.Column(sa.String(255))
    DepositoStockVto = sa.Column(sa.Date)