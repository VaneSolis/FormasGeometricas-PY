from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.controllers.geometry_controller import GeometryController
from app.models.schemas import (
    GeometricCalculationRequest, GeometricCalculationResponse, CalculationResult
)
from app.core.deps import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/geometry", tags=["Geometría"])

@router.post("/calculate", response_model=GeometricCalculationResponse, 
             summary="Calcular y guardar forma geométrica",
             description="Calcula el área y/o volumen de una forma geométrica y lo guarda en la base de datos")
async def calculate_and_save_geometry(
    request: GeometricCalculationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Calcular y guardar un cálculo geométrico"""
    try:
        controller = GeometryController(db)
        result = controller.calculate_and_save(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.post("/calculate-only", response_model=CalculationResult,
             summary="Calcular forma geométrica sin guardar",
             description="Calcula el área y/o volumen de una forma geométrica sin guardarlo en la base de datos")
async def calculate_only_geometry(
    request: GeometricCalculationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Calcular sin guardar en la base de datos"""
    try:
        controller = GeometryController(db)
        result = controller.calculate_only(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/calculations", response_model=List[GeometricCalculationResponse],
            summary="Obtener todos los cálculos",
            description="Obtiene todos los cálculos guardados con paginación")
async def get_all_calculations(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener todos los cálculos con paginación"""
    controller = GeometryController(db)
    return controller.get_all_calculations(skip=skip, limit=limit)

@router.get("/calculations/{calculation_id}", response_model=GeometricCalculationResponse,
            summary="Obtener cálculo por ID",
            description="Obtiene un cálculo específico por su ID")
async def get_calculation_by_id(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener un cálculo por ID"""
    controller = GeometryController(db)
    calculation = controller.get_calculation_by_id(calculation_id)
    if not calculation:
        raise HTTPException(status_code=404, detail="Cálculo no encontrado")
    return calculation

@router.get("/calculations/shape/{shape_type}", response_model=List[GeometricCalculationResponse],
            summary="Obtener cálculos por tipo de forma",
            description="Obtiene todos los cálculos de un tipo específico de forma geométrica")
async def get_calculations_by_shape_type(
    shape_type: str,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener cálculos por tipo de forma"""
    controller = GeometryController(db)
    return controller.get_calculations_by_shape_type(shape_type, skip=skip, limit=limit)

@router.delete("/calculations/{calculation_id}",
               summary="Eliminar cálculo",
               description="Elimina un cálculo específico por su ID")
async def delete_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Eliminar un cálculo por ID"""
    controller = GeometryController(db)
    success = controller.delete_calculation(calculation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cálculo no encontrado")
    return {"message": "Cálculo eliminado exitosamente"}

@router.get("/statistics",
            summary="Obtener estadísticas",
            description="Obtiene estadísticas de los cálculos guardados")
async def get_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener estadísticas de los cálculos"""
    controller = GeometryController(db)
    return controller.get_statistics()

@router.get("/shapes",
            summary="Obtener formas soportadas",
            description="Obtiene la lista de formas geométricas soportadas por la API")
async def get_supported_shapes():
    """Obtener formas geométricas soportadas"""
    return {
        "supported_shapes": [
            {
                "name": "cube",
                "description": "Cubo",
                "dimensions": ["side"],
                "calculations": ["area", "volume", "both"]
            },
            {
                "name": "sphere", 
                "description": "Esfera",
                "dimensions": ["radius"],
                "calculations": ["area", "volume", "both"]
            },
            {
                "name": "cylinder",
                "description": "Cilindro", 
                "dimensions": ["radius", "height"],
                "calculations": ["area", "volume", "both"]
            },
            {
                "name": "square",
                "description": "Cuadrado",
                "dimensions": ["side"],
                "calculations": ["area"]
            },
            {
                "name": "circle",
                "description": "Círculo",
                "dimensions": ["radius"],
                "calculations": ["area"]
            }
        ]
    } 