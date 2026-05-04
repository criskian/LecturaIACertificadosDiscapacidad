# Backend de análisis de certificados de discapacidad

API en FastAPI para cargar certificados de discapacidad de Colombia en imagen o PDF, extraer información relevante, analizar el perfil funcional/laboral con OpenAI y exponer un resultado estructurado listo para un dashboard o infografía web.

## Monorepo listo para Vercel

Este repositorio queda preparado para desplegar dos proyectos independientes en Vercel usando el mismo GitHub repo:

- Backend FastAPI con `Root Directory = app`
- Frontend React + Vite con `Root Directory = frontend`

La configuración sigue la recomendación actual de Vercel para monorepos: un proyecto por directorio, cada uno con su propia configuración y variables de entorno.

## Características

- Validación de archivos PDF e imágenes.
- Extracción de texto desde PDF y fallback visual para imágenes o PDFs escaneados.
- Análisis con OpenAI usando un prompt de negocio encapsulado en `app/prompts/certificate_analysis.py`.
- Respuesta estructurada en JSON con datos personales, dominios funcionales, códigos CIF y recomendaciones laborales.
- Persistencia simple en memoria para consultar resultados por ID.
- Exportación opcional del análisis como HTML.
- Descarga de PDF del análisis generado.
- Pruebas básicas con `pytest`.

## Estructura

```text
app/
  index.py
  api/
    dependencies.py
    routes/
      analyses.py
      health.py
  core/
    config.py
    logging.py
  models/
    analysis_record.py
  prompts/
    certificate_analysis.py
  schemas/
    analysis.py
    document.py
  services/
    analysis_pipeline.py
    file_service.py
    html_exporter.py
    openai_service.py
    storage.py
  utils/
    json_utils.py
  main.py
tests/
  conftest.py
  test_api.py
frontend/
  .env.example
  src/
```

## Requisitos

- Python 3.11 o superior
- Variable `OPENAI_API_KEY`

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

## Variables de entorno

```env
OPENAI_API_KEY=sk-your-openai-key
OPENAI_MODEL=gpt-4.1-mini
FRONTEND_URL=https://tu-frontend.vercel.app
MAX_FILE_SIZE_MB=10
ALLOW_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173
ALLOW_ORIGIN_REGEX=^https://[a-zA-Z0-9-]+\.vercel\.app$
REQUEST_TIMEOUT_SECONDS=90
MAX_PDF_PAGES_FOR_VISION=5
MAX_IMAGE_DIMENSION=1600
LOG_LEVEL=INFO
```

## Frontend

El frontend vive en `frontend/` y consume el backend mediante `VITE_API_BASE_URL`.

Variables de entorno del frontend:

```env
VITE_API_BASE_URL=https://tu-backend.vercel.app
```

Para desarrollo local puedes copiar:

```bash
copy frontend\.env.example frontend\.env
```

## Ejecución local

Backend:

```bash
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Swagger del backend quedará disponible en:

- `http://127.0.0.1:8000/docs`

## Endpoints principales

- `GET /health`
- `POST /api/v1/analyses/upload`
- `POST /api/v1/analyses`
- `GET /api/v1/analyses/{analysis_id}`
- `POST /api/v1/analyses/{analysis_id}/regenerate`
- `GET /api/v1/analyses/{analysis_id}/html`
- `GET /api/v1/analyses/{analysis_id}/pdf`

## Flujo de análisis

1. El backend valida tamaño, extensión y tipo MIME del archivo.
2. Si es PDF, extrae texto con PyMuPDF.
3. Si el texto es insuficiente o el archivo es imagen, genera imágenes del documento para análisis visual.
4. Envía prompt + texto + imágenes a OpenAI pidiendo JSON estricto.
5. Limpia cualquier salida extra y valida la respuesta con Pydantic.
6. Guarda el análisis en memoria para consulta posterior.

## Ejemplo de uso

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/analyses" ^
  -H "accept: application/json" ^
  -H "Content-Type: multipart/form-data" ^
  -F "file=@certificado.pdf"
```

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/analyses/{analysis_id}/pdf" ^
  -H "accept: application/pdf" ^
  --output informe_laboral_inclusivo.pdf
```

## Pruebas

```bash
pytest
```

## Despliegue en Vercel

### Proyecto 1: backend

Configura un proyecto nuevo en Vercel con:

- Repository: este mismo repositorio
- Root Directory: `app`
- Framework Preset: `Other`

No se necesita `vercel.json` para este backend. Se usa detección automática de Python/FastAPI y un entrypoint compatible en `app/index.py`, que expone una instancia global `app = FastAPI()` a través de `app.main`.

Archivos importantes para el deploy del backend:

- `app/index.py`: entrypoint compatible con Vercel
- `app/main.py`: crea y expone la aplicación FastAPI
- `app/requirements.txt`: dependencias para el proyecto cuyo root es `app`

Variables de entorno recomendadas para el proyecto backend en Vercel:

- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `FRONTEND_URL`
- `ALLOW_ORIGINS`
- `ALLOW_ORIGIN_REGEX`
- `REQUEST_TIMEOUT_SECONDS`
- `MAX_PDF_PAGES_FOR_VISION`
- `MAX_IMAGE_DIMENSION`
- `LOG_LEVEL`

Rutas esperadas del backend desplegado:

- `GET /health`
- `POST /api/v1/analyses/upload`
- `POST /api/v1/analyses`

### Proyecto 2: frontend

Configura otro proyecto nuevo en Vercel con:

- Repository: este mismo repositorio
- Root Directory: `frontend`
- Framework Preset: `Vite`

Variable de entorno obligatoria del frontend:

- `VITE_API_BASE_URL=https://tu-backend.vercel.app`

### Orden recomendado de despliegue

1. Despliega primero el backend.
2. Copia la URL productiva del backend.
3. Configura `VITE_API_BASE_URL` en el proyecto frontend.
4. Configura `FRONTEND_URL` en el proyecto backend con la URL productiva del frontend.
5. Si quieres permitir previews del frontend en Vercel, deja `ALLOW_ORIGIN_REGEX=^https://[a-zA-Z0-9-]+\.vercel\.app$`.

## Notas de Vercel

- El backend no debe usar la raíz del repositorio como Root Directory si quieres separarlo claramente del frontend.
- `app/requirements.txt` existe para que Vercel instale dependencias correctamente cuando el Root Directory del proyecto backend es `app`.
- El frontend no hardcodea `localhost`; usa `VITE_API_BASE_URL`.
- Si el backend devuelve 404 en Vercel, revisa primero que el proyecto backend tenga `Root Directory = app` y que el despliegue esté usando `app/index.py`.

## Notas técnicas

- La persistencia actual es en memoria. Si reinicias el proceso, los resultados se pierden.
- El endpoint `/upload` valida el archivo pero no lo almacena definitivamente.
- El servicio OpenAI está implementado con `httpx` contra `POST /v1/chat/completions`.
- El HTML exportado está pensado como respaldo o vista rápida; el frontend puede renderizar el JSON principal.
- El PDF usa HTML de impresión con fondo blanco y prioriza `weasyprint`, con `pdfkit` como alternativa.
