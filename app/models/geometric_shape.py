from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.db.database import Base

class GeometricCalculation(Base):
    __tablename__ = "geometric_calculations"
    
    id = Column(Integer, primary_key=True, index=True)
    shape_type = Column(String(50), nullable=False, index=True)
    dimensions = Column(Text, nullable=False)  # JSON string con las dimensiones
    area = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    calculation_type = Column(String(20), nullable=False)  # "area", "volume", "both"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 