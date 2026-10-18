# TickerLab Services

`tickerlab-services` es el orquestador y capa de API para el ecosistema TickerLab. Actúa como el puente entre la interfaz de usuario (`tickerlab-ui`) y el motor de análisis cuantitativo (`tickerlab-core`), exponiendo las capacidades de análisis a través de una interfaz REST.

## 🚀 Características

- **API REST**: Construida con FastAPI para un alto rendimiento y documentación automática.
- **Orquestación E2E**: Ejecuta el pipeline completo de análisis cuantitativo (ingesta, features, etiquetas y validación) para cualquier activo financiero.
- **Integración con Core**: Envuelve las funciones del núcleo de TickerLab en servicios asíncronos y endpoints accesibles.
- **CORS Enabled**: Configurado para permitir la conexión fluida con la aplicación de frontend.

## 🛠️ Arquitectura

El proyecto sigue una estructura modular basada en servicios:

- `app/main.py`: Punto de entrada de la aplicación y configuración de FastAPI.
- `app/api/`: Definición de los endpoints y esquemas de solicitud/respuesta (Pydantic).
- `app/services/`: Capa de lógica de negocio que interactúa con el núcleo de análisis.
- `app/core/`: Configuraciones globales y utilidades internas.

## 📦 Instalación

### Requisitos previos
- Python $\ge$ 3.11
- `tickerlab-core` instalado en el entorno.

### Instalación local
```bash
# Clonar el repositorio (si no está en el monorepo)
git clone <repository-url>
cd tickerlab-services

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate    # Windows

# Instalar dependencias
pip install -e .
pip install -e ".[dev]"
```

## 🏃 Ejecución

Para iniciar el servidor de desarrollo con recarga automática:

```bash
# Desde la raíz del proyecto tickerlab-services
python app/main.py
```
O usando uvicorn directamente:
```bash
uvicorn app.main:app --reload --port 8000
```

El servidor estará disponible en: `http://localhost:8000`
La documentación interactiva (Swagger) en: `http://localhost:8000/docs`

## 🔌 API Endpoints

### Análisis Cuantitativo

`POST /analysis/analyze`

Ejecuta el pipeline de análisis E2E para un activo.

**Cuerpo de la solicitud:**
```json
{
  "symbol": "AAPL",
  "timeframe": "1d",
  "period": "max",
  "source": "yahoo"
}
```

**Respuestas:**
- `200 OK`: Retorna el resultado completo del análisis cuantitativo.
- `400 Bad Request`: Error en los parámetros de entrada o error inesperado.
- `500 Internal Server Error`: Error en la ejecución del núcleo de análisis.

### Salud del Sistema

`GET /health`

Verifica el estado del servicio.

## 🧪 Pruebas

El proyecto incluye pruebas unitarias e integrales para asegurar la estabilidad de la API.

```bash
pytest tests/
```
