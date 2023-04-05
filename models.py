from sqlalchemy import Column, ForeignKey, String, Float, Table, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

materials = Table(
    "materials",
    Base.metadata,
    Column("material_id", Integer, ForeignKey("material.material_id")),
    Column("material_name", String, ForeignKey("material.material_name")),
    Column("adm_stress", Float, ForeignKey("material.adm_stress")),
    Column("mat_den", Float, ForeignKey("material.mat_den"))
)

class Material(Base):
    __tablename__ = "material"
    material_id = Column(Integer, primary_key=True)
    material_name = Column(String)
    adm_stress = Column(Float)
    mat_den = Column(Float)
