# API de Cálculos Geométricos

Una API REST completa para calcular áreas y volúmenes de formas geométricas con almacenamiento en Supabase (PostgreSQL).

## 🚀 Características

- **Cálculos Precisos**: Áreas y volúmenes de formas geométricas
- **Base de Datos**: Almacenamiento en PostgreSQL (Supabase)
- **API REST**: Documentación automática con Swagger
- **Arquitectura Limpia**: Separación clara de responsabilidades
- **Validación**: Validación de datos con Pydantic
- **Autenticación JWT**: Sistema de autenticación seguro
- **CORS Configurado**: Soporte para aplicaciones frontend
- **Escalable**: Diseñado para crecer fácilmente

## 📐 Formas Soportadas

| Forma | Área | Volumen | Dimensiones |
|-------|------|---------|-------------|
| **Cubo** | ✅ | ✅ | `side` |
| **Esfera** | ✅ | ✅ | `radius` |
| **Cilindro** | ✅ | ✅ | `radius`, `height` |
| **Cuadrado** | ✅ | ❌ | `side` |
| **Círculo** | ✅ | ❌ | `radius` |

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd mi-APIpythonFastApi
```

### 2. Crear entorno virtual
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r dependencias.txt
```

### 4. Configurar variables de entorno
Copia el archivo `env.example` a `.env` y configura tus credenciales:

```bash
cp env.example .env
```

Edita el archivo `.env` con tus credenciales de Supabase:
```env
SUPABASE_URL=tu_url_de_supabase
SUPABASE_KEY=tu_clave_de_supabase
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_db
DEBUG=True

# Configuración JWT
SECRET_KEY=tu_clave_secreta_muy_segura_aqui_cambiala_en_produccion
ACCESS_TOKEN_EXPIRE_MINUTES=30

### 5. Configurar Supabase

1. Crea una cuenta en [Supabase](https://supabase.com)
2. Crea un nuevo proyecto
3. Ve a Settings > Database para obtener la URL de conexión
4. La tabla `geometric_calculations` se creará automáticamente

## 🚀 Ejecutar la aplicación

```bash
# Desarrollo
uvicorn app.main:app --reload

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

La API estará disponible en: http://localhost:8000

## 📚 Documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Endpoints Principales

### 🔐 Autenticación
```http
POST /api/v1/auth/register    # Registrar nuevo usuario
POST /api/v1/auth/login       # Iniciar sesión
GET  /api/v1/auth/me          # Obtener información del usuario actual
```

### 📐 Geometría (Requiere autenticación)
```http
POST /api/v1/geometry/calculate
POST /api/v1/geometry/calculate-only
GET  /api/v1/geometry/calculations
GET  /api/v1/geometry/calculations/{id}
GET  /api/v1/geometry/calculations/shape/{shape_type}
DELETE /api/v1/geometry/calculations/{id}
GET  /api/v1/geometry/statistics
GET  /api/v1/geometry/shapes
```

### Ejemplo de uso con autenticación:
```bash
# 1. Registrar usuario
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@ejemplo.com",
    "username": "usuario",
    "password": "contraseña123"
  }'

# 2. Iniciar sesión
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario&password=contraseña123"

# 3. Usar el token para calcular
curl -X POST "http://localhost:8000/api/v1/geometry/calculate" \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "shape_type": "cube",
    "dimensions": {"side": 5.0},
    "calculation_type": "both"
  }'
```

## 📁 Estructura del Proyecto

```
mi-APIpythonFastApi/
├── app/
│   ├── controllers/          # Lógica de negocio
│   │   └── geometry_controller.py
│   ├── core/                # Configuración
│   │   └── config.py
│   ├── db/                  # Base de datos
│   │   └── database.py
│   ├── models/              # Modelos y esquemas
│   │   ├── geometric_shape.py
│   │   └── schemas.py
│   ├── repositories/        # Acceso a datos
│   │   └── calculation_repository.py
│   ├── routers/            # Rutas de la API
│   │   └── geometry_routes.py
│   ├── services/           # Lógica de cálculo
│   │   └── geometry_service.py
│   └── main.py            # Aplicación principal
├── dependencias.txt        # Dependencias del proyecto
├── env.example            # Variables de entorno de ejemplo
└── README.md             # Este archivo
```

## 🏗️ Arquitectura

El proyecto sigue los principios de **Clean Architecture**:

- **Controllers**: Manejan las peticiones HTTP y la lógica de negocio
- **Services**: Contienen la lógica de cálculo geométrico
- **Repositories**: Manejan el acceso a la base de datos
- **Models**: Definen la estructura de datos
- **Routers**: Definen los endpoints de la API

## 🧪 Ejemplos de Uso

### Calcular área de un círculo
```bash
curl -X POST "http://localhost:8000/api/v1/geometry/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "shape_type": "circle",
    "dimensions": {"radius": 3.0},
    "calculation_type": "area"
  }'
```

### Calcular volumen de una esfera
```bash
curl -X POST "http://localhost:8000/api/v1/geometry/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "shape_type": "sphere",
    "dimensions": {"radius": 4.0},
    "calculation_type": "volume"
  }'
```

### Obtener todos los cálculos
```bash
curl "http://localhost:8000/api/v1/geometry/calculations"
```

## 🔒 Seguridad

- **Autenticación JWT**: Tokens seguros para autenticación
- **Hash de contraseñas**: Contraseñas hasheadas con bcrypt
- **Validación de datos**: Validación de entrada con Pydantic
- **CORS configurado**: Soporte seguro para aplicaciones frontend
- **Manejo de errores**: Códigos HTTP apropiados
- **Dependencias seguras**: Todas las rutas protegidas requieren autenticación

## 🚀 Despliegue

### Heroku
```bash
# Crear Procfile
echo "web: uvicorn app.main:app --host=0.0.0.0 --port=\$PORT" > Procfile

# Desplegar
heroku create tu-app-geometria
heroku config:set DATABASE_URL=tu_url_de_supabase
git push heroku main
```

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r dependencias.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Si tienes alguna pregunta o problema, por favor abre un issue en el repositorio.
