import math
import json
from typing import Dict, Any, Optional
from app.models.schemas import (
    CubeDimensions, SphereDimensions, CylinderDimensions, 
    SquareDimensions, CircleDimensions, CalculationResult
)

class GeometryService:
    """Servicio para cálculos geométricos"""
    
    @staticmethod
    def calculate_cube(dimensions: CubeDimensions, calculation_type: str) -> CalculationResult:
        """Calcular área y/o volumen de un cubo"""
        side = dimensions.side
        area = None
        volume = None
        
        if calculation_type in ["area", "both"]:
            area = 6 * (side ** 2)  # 6 caras del cubo
            
        if calculation_type in ["volume", "both"]:
            volume = side ** 3
            
        return CalculationResult(
            shape_type="cube",
            dimensions={"side": side},
            area=area,
            volume=volume,
            calculation_type=calculation_type
        )
    
    @staticmethod
    def calculate_sphere(dimensions: SphereDimensions, calculation_type: str) -> CalculationResult:
        """Calcular área y/o volumen de una esfera"""
        radius = dimensions.radius
        area = None
        volume = None
        
        if calculation_type in ["area", "both"]:
            area = 4 * math.pi * (radius ** 2)
            
        if calculation_type in ["volume", "both"]:
            volume = (4/3) * math.pi * (radius ** 3)
            
        return CalculationResult(
            shape_type="sphere",
            dimensions={"radius": radius},
            area=area,
            volume=volume,
            calculation_type=calculation_type
        )
    
    @staticmethod
    def calculate_cylinder(dimensions: CylinderDimensions, calculation_type: str) -> CalculationResult:
        """Calcular área y/o volumen de un cilindro"""
        radius = dimensions.radius
        height = dimensions.height
        area = None
        volume = None
        
        if calculation_type in ["area", "both"]:
            # Área lateral + 2 bases circulares
            lateral_area = 2 * math.pi * radius * height
            base_area = 2 * math.pi * (radius ** 2)
            area = lateral_area + base_area
            
        if calculation_type in ["volume", "both"]:
            volume = math.pi * (radius ** 2) * height
            
        return CalculationResult(
            shape_type="cylinder",
            dimensions={"radius": radius, "height": height},
            area=area,
            volume=volume,
            calculation_type=calculation_type
        )
    
    @staticmethod
    def calculate_square(dimensions: SquareDimensions, calculation_type: str) -> CalculationResult:
        """Calcular área de un cuadrado"""
        side = dimensions.side
        area = None
        
        if calculation_type in ["area", "both"]:
            area = side ** 2
            
        return CalculationResult(
            shape_type="square",
            dimensions={"side": side},
            area=area,
            volume=None,  # Los cuadrados no tienen volumen
            calculation_type=calculation_type
        )
    
    @staticmethod
    def calculate_circle(dimensions: CircleDimensions, calculation_type: str) -> CalculationResult:
        """Calcular área de un círculo"""
        radius = dimensions.radius
        area = None
        
        if calculation_type in ["area", "both"]:
            area = math.pi * (radius ** 2)
            
        return CalculationResult(
            shape_type="circle",
            dimensions={"radius": radius},
            area=area,
            volume=None,  # Los círculos no tienen volumen
            calculation_type=calculation_type
        )
    
    @staticmethod
    def calculate_shape(shape_type: str, dimensions: Dict[str, Any], calculation_type: str) -> CalculationResult:
        """Método principal para calcular cualquier forma geométrica"""
        
        if shape_type == "cube":
            cube_dims = CubeDimensions(**dimensions)
            return GeometryService.calculate_cube(cube_dims, calculation_type)
            
        elif shape_type == "sphere":
            sphere_dims = SphereDimensions(**dimensions)
            return GeometryService.calculate_sphere(sphere_dims, calculation_type)
            
        elif shape_type == "cylinder":
            cylinder_dims = CylinderDimensions(**dimensions)
            return GeometryService.calculate_cylinder(cylinder_dims, calculation_type)
            
        elif shape_type == "square":
            square_dims = SquareDimensions(**dimensions)
            return GeometryService.calculate_square(square_dims, calculation_type)
            
        elif shape_type == "circle":
            circle_dims = CircleDimensions(**dimensions)
            return GeometryService.calculate_circle(circle_dims, calculation_type)
            
        else:
            raise ValueError(f"Tipo de forma no soportado: {shape_type}") 