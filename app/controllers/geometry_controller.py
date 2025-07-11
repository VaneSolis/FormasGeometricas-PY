from sqlalchemy.orm import Session
from typing import List, Optional
from app.services.geometry_service import GeometryService
from app.repositories.calculation_repository import CalculationRepository
from app.models.schemas import (
    GeometricCalculationRequest, GeometricCalculationResponse, CalculationResult
)
from app.models.geometric_shape import GeometricCalculation

class GeometryController:
    """Controlador para manejar la lógica de negocio de cálculos geométricos"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = CalculationRepository(db)
        self.service = GeometryService()
    
    def calculate_and_save(self, request: GeometricCalculationRequest) -> GeometricCalculationResponse:
        """Calcular y guardar un nuevo cálculo geométrico"""
        
        # Extraer dimensiones del request
        dimensions_dict = request.dimensions.dict()
        
        # Realizar el cálculo
        result = self.service.calculate_shape(
            shape_type=request.shape_type,
            dimensions=dimensions_dict,
            calculation_type=request.calculation_type
        )
        
        # Guardar en la base de datos
        db_calculation = self.repository.create_calculation(
            shape_type=result.shape_type,
            dimensions=result.dimensions,
            area=result.area,
            volume=result.volume,
            calculation_type=result.calculation_type
        )
        
        return GeometricCalculationResponse.from_orm(db_calculation)
    
    def calculate_only(self, request: GeometricCalculationRequest) -> CalculationResult:
        """Calcular sin guardar en la base de datos"""
        dimensions_dict = request.dimensions.dict()
        
        return self.service.calculate_shape(
            shape_type=request.shape_type,
            dimensions=dimensions_dict,
            calculation_type=request.calculation_type
        )
    
    def get_calculation_by_id(self, calculation_id: int) -> Optional[GeometricCalculationResponse]:
        """Obtener un cálculo por ID"""
        calculation = self.repository.get_calculation_by_id(calculation_id)
        if calculation:
            return GeometricCalculationResponse.from_orm(calculation)
        return None
    
    def get_all_calculations(self, skip: int = 0, limit: int = 100) -> List[GeometricCalculationResponse]:
        """Obtener todos los cálculos"""
        calculations = self.repository.get_all_calculations(skip=skip, limit=limit)
        return [GeometricCalculationResponse.from_orm(calc) for calc in calculations]
    
    def get_calculations_by_shape_type(self, shape_type: str, 
                                     skip: int = 0, limit: int = 100) -> List[GeometricCalculationResponse]:
        """Obtener cálculos por tipo de forma"""
        calculations = self.repository.get_calculations_by_shape_type(
            shape_type=shape_type, skip=skip, limit=limit
        )
        return [GeometricCalculationResponse.from_orm(calc) for calc in calculations]
    
    def delete_calculation(self, calculation_id: int) -> bool:
        """Eliminar un cálculo"""
        return self.repository.delete_calculation(calculation_id)
    
    def get_statistics(self) -> dict:
        """Obtener estadísticas de los cálculos"""
        total_calculations = self.repository.get_calculations_count()
        
        # Contar por tipo de forma
        shape_counts = {}
        for shape_type in ["cube", "sphere", "cylinder", "square", "circle"]:
            calculations = self.repository.get_calculations_by_shape_type(shape_type)
            shape_counts[shape_type] = len(calculations)
        
        return {
            "total_calculations": total_calculations,
            "calculations_by_shape": shape_counts
        } 