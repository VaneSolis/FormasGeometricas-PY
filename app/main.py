from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import geometry_routes
from app.db.database import engine
from app.models import geometric_shape

# Crear las tablas en la base de datos
geometric_shape.Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    ## API de Cálculos Geométricos
    
    Esta API permite calcular áreas y volúmenes de diferentes formas geométricas:
    
    ### Formas Soportadas:
    - **Cubo**: Volumen y área superficial
    - **Esfera**: Volumen y área superficial  
    - **Cilindro**: Volumen y área superficial
    - **Cuadrado**: Área
    - **Círculo**: Área
    
    ### Características:
    - ✅ Cálculos precisos de áreas y volúmenes
    - ✅ Almacenamiento en base de datos PostgreSQL (Supabase)
    - ✅ API REST con documentación Swagger
    - ✅ Arquitectura limpia (Clean Architecture)
    - ✅ Validación de datos con Pydantic
    
    ### Endpoints Principales:
    - `POST /api/v1/geometry/calculate` - Calcular y guardar
    - `POST /api/v1/geometry/calculate-only` - Calcular sin guardar
    - `GET /api/v1/geometry/calculations` - Obtener todos los cálculos
    - `GET /api/v1/geometry/shapes` - Formas soportadas
    """,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(geometry_routes.router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Información"])
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "¡Bienvenido a la API de Cálculos Geométricos!",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "api_prefix": settings.API_V1_STR
    }

@app.get("/health", tags=["Salud"])
async def health_check():
    """Verificar el estado de salud de la API"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "database": "connected"  # En una implementación real, verificar conexión a BD
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
