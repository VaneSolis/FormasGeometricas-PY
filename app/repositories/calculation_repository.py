import json
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.geometric_shape import GeometricCalculation
from app.models.schemas import GeometricCalculationResponse

class CalculationRepository:
    """Repositorio para manejar operaciones de base de datos de cálculos geométricos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_calculation(self, shape_type: str, dimensions: dict, 
                          area: Optional[float], volume: Optional[float], 
                          calculation_type: str) -> GeometricCalculation:
        """Crear un nuevo cálculo en la base de datos"""
        db_calculation = GeometricCalculation(
            shape_type=shape_type,
            dimensions=json.dumps(dimensions),
            area=area,
            volume=volume,
            calculation_type=calculation_type
        )
        self.db.add(db_calculation)
        self.db.commit()
        self.db.refresh(db_calculation)
        return db_calculation
    
    def get_calculation_by_id(self, calculation_id: int) -> Optional[GeometricCalculation]:
        """Obtener un cálculo por ID"""
        return self.db.query(GeometricCalculation).filter(
            GeometricCalculation.id == calculation_id
        ).first()
    
    def get_all_calculations(self, skip: int = 0, limit: int = 100) -> List[GeometricCalculation]:
        """Obtener todos los cálculos con paginación"""
        return self.db.query(GeometricCalculation).offset(skip).limit(limit).all()
    
    def get_calculations_by_shape_type(self, shape_type: str, 
                                     skip: int = 0, limit: int = 100) -> List[GeometricCalculation]:
        """Obtener cálculos por tipo de forma"""
        return self.db.query(GeometricCalculation).filter(
            GeometricCalculation.shape_type == shape_type
        ).offset(skip).limit(limit).all()
    
    def delete_calculation(self, calculation_id: int) -> bool:
        """Eliminar un cálculo por ID"""
        calculation = self.get_calculation_by_id(calculation_id)
        if calculation:
            self.db.delete(calculation)
            self.db.commit()
            return True
        return False
    
    def get_calculations_count(self) -> int:
        """Obtener el total de cálculos"""
        return self.db.query(GeometricCalculation).count() 