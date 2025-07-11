from pydantic import BaseModel, Field
from typing import Optional, Union, Dict, Any
from datetime import datetime

# Esquemas base para dimensiones
class CubeDimensions(BaseModel):
    side: float = Field(..., gt=0, description="Longitud del lado del cubo")

class SphereDimensions(BaseModel):
    radius: float = Field(..., gt=0, description="Radio de la esfera")

class CylinderDimensions(BaseModel):
    radius: float = Field(..., gt=0, description="Radio del cilindro")
    height: float = Field(..., gt=0, description="Altura del cilindro")

class SquareDimensions(BaseModel):
    side: float = Field(..., gt=0, description="Longitud del lado del cuadrado")

class CircleDimensions(BaseModel):
    radius: float = Field(..., gt=0, description="Radio del círculo")

# Esquemas para cálculos
class GeometricCalculationRequest(BaseModel):
    shape_type: str = Field(..., description="Tipo de forma: cube, sphere, cylinder, square, circle")
    dimensions: Union[CubeDimensions, SphereDimensions, CylinderDimensions, SquareDimensions, CircleDimensions]
    calculation_type: str = Field(..., description="Tipo de cálculo: area, volume, both")

class GeometricCalculationResponse(BaseModel):
    id: int
    shape_type: str
    dimensions: str
    area: Optional[float] = None
    volume: Optional[float] = None
    calculation_type: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CalculationResult(BaseModel):
    shape_type: str
    dimensions: Dict[str, Any]
    area: Optional[float] = None
    volume: Optional[float] = None
    calculation_type: str 