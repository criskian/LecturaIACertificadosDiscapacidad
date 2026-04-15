# Backend de análisis de certificados de discapacidad

API en FastAPI para cargar certificados de discapacidad de Colombia en imagen o PDF, extraer información relevante, analizar el perfil funcional/laboral con OpenAI y exponer un resultado estructurado listo para un dashboard o infografía web.

## Características

- Validación de archivos PDF e imágenes.
- Extracción de texto desde PDF y fallback visual para imágenes o PDFs escaneados.
- Análisis con OpenAI usando un prompt de negocio encapsulado en `app/prompts/certificate_analysis.py`.
- Respuesta estructurada en JSON con datos personales, dominios funcionales, códigos CIF y recomendaciones laborales.
- Persistencia simple en memoria para consultar resultados por ID.
- Exportación opcional del análisis como HTML.
- Pruebas básicas con `pytest`.

## Estructura

```text
app/
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
MAX_FILE_SIZE_MB=10
ALLOW_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173
REQUEST_TIMEOUT_SECONDS=90
MAX_PDF_PAGES_FOR_VISION=5
MAX_IMAGE_DIMENSION=1600
LOG_LEVEL=INFO
```

## Ejecución

```bash
uvicorn app.main:app --reload
```

Swagger quedará disponible en:

- `http://127.0.0.1:8000/docs`

## Endpoints principales

- `GET /health`
- `POST /api/v1/analyses/upload`
- `POST /api/v1/analyses`
- `GET /api/v1/analyses/{analysis_id}`
- `POST /api/v1/analyses/{analysis_id}/regenerate`
- `GET /api/v1/analyses/{analysis_id}/html`

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

## Pruebas

```bash
pytest
```

## Notas técnicas

- La persistencia actual es en memoria. Si reinicias el proceso, los resultados se pierden.
- El endpoint `/upload` valida el archivo pero no lo almacena definitivamente.
- El servicio OpenAI está implementado con `httpx` contra `POST /v1/chat/completions`.
- El HTML exportado está pensado como respaldo o vista rápida; el frontend puede renderizar el JSON principal.
