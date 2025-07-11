#!/usr/bin/env python3
"""
Script de prueba para verificar que la API de geometría funciona correctamente.
Ejecutar después de iniciar el servidor con: uvicorn app.main:app --reload
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_health_check():
    """Probar el endpoint de salud"""
    print("🔍 Probando health check...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health check exitoso")
            return True
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. Asegúrate de que esté ejecutándose.")
        return False

def test_supported_shapes():
    """Probar el endpoint de formas soportadas"""
    print("\n🔍 Probando endpoint de formas soportadas...")
    try:
        response = requests.get(f"{BASE_URL}/geometry/shapes")
        if response.status_code == 200:
            data = response.json()
            print("✅ Formas soportadas obtenidas:")
            for shape in data["supported_shapes"]:
                print(f"   - {shape['name']}: {shape['description']}")
            return True
        else:
            print(f"❌ Error obteniendo formas: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_calculations():
    """Probar diferentes cálculos geométricos"""
    print("\n🧮 Probando cálculos geométricos...")
    
    test_cases = [
        {
            "name": "Cubo - área y volumen",
            "data": {
                "shape_type": "cube",
                "dimensions": {"side": 5.0},
                "calculation_type": "both"
            }
        },
        {
            "name": "Esfera - volumen",
            "data": {
                "shape_type": "sphere", 
                "dimensions": {"radius": 3.0},
                "calculation_type": "volume"
            }
        },
        {
            "name": "Círculo - área",
            "data": {
                "shape_type": "circle",
                "dimensions": {"radius": 4.0},
                "calculation_type": "area"
            }
        },
        {
            "name": "Cilindro - área y volumen",
            "data": {
                "shape_type": "cylinder",
                "dimensions": {"radius": 2.0, "height": 6.0},
                "calculation_type": "both"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n   Probando: {test_case['name']}")
        try:
            response = requests.post(
                f"{BASE_URL}/geometry/calculate-only",
                json=test_case["data"],
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ {test_case['name']} - Exitoso")
                if result.get("area"):
                    print(f"      Área: {result['area']:.2f}")
                if result.get("volume"):
                    print(f"      Volumen: {result['volume']:.2f}")
            else:
                print(f"   ❌ {test_case['name']} - Error: {response.status_code}")
                print(f"      Respuesta: {response.text}")
                
        except Exception as e:
            print(f"   ❌ {test_case['name']} - Error: {e}")

def test_database_operations():
    """Probar operaciones con base de datos"""
    print("\n💾 Probando operaciones de base de datos...")
    
    # Crear un cálculo y guardarlo
    test_data = {
        "shape_type": "square",
        "dimensions": {"side": 7.0},
        "calculation_type": "area"
    }
    
    try:
        # Guardar cálculo
        response = requests.post(
            f"{BASE_URL}/geometry/calculate",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            saved_calc = response.json()
            calc_id = saved_calc["id"]
            print(f"   ✅ Cálculo guardado con ID: {calc_id}")
            
            # Obtener el cálculo por ID
            response = requests.get(f"{BASE_URL}/geometry/calculations/{calc_id}")
            if response.status_code == 200:
                print("   ✅ Cálculo recuperado exitosamente")
            else:
                print(f"   ❌ Error recuperando cálculo: {response.status_code}")
            
            # Obtener todos los cálculos
            response = requests.get(f"{BASE_URL}/geometry/calculations")
            if response.status_code == 200:
                calculations = response.json()
                print(f"   ✅ Total de cálculos en BD: {len(calculations)}")
            else:
                print(f"   ❌ Error obteniendo cálculos: {response.status_code}")
                
        else:
            print(f"   ❌ Error guardando cálculo: {response.status_code}")
            print(f"      Respuesta: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error en operaciones de BD: {e}")

def test_statistics():
    """Probar endpoint de estadísticas"""
    print("\n📊 Probando estadísticas...")
    try:
        response = requests.get(f"{BASE_URL}/geometry/statistics")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Estadísticas obtenidas:")
            print(f"   Total de cálculos: {stats['total_calculations']}")
            print("   Cálculos por forma:")
            for shape, count in stats['calculations_by_shape'].items():
                print(f"     - {shape}: {count}")
        else:
            print(f"❌ Error obteniendo estadísticas: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas de la API de Geometría")
    print("=" * 50)
    
    # Verificar que el servidor esté ejecutándose
    if not test_health_check():
        print("\n❌ El servidor no está ejecutándose. Ejecuta:")
        print("   uvicorn app.main:app --reload")
        return
    
    # Ejecutar todas las pruebas
    test_supported_shapes()
    test_calculations()
    test_database_operations()
    test_statistics()
    
    print("\n" + "=" * 50)
    print("✅ Todas las pruebas completadas")
    print("\n📚 Documentación disponible en:")
    print("   - Swagger UI: http://localhost:8000/docs")
    print("   - ReDoc: http://localhost:8000/redoc")

if __name__ == "__main__":
    main() 