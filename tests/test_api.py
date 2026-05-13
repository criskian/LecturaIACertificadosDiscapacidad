from __future__ import annotations

from io import BytesIO

from PIL import Image

from app.utils.analysis_guardrails import normalize_analysis_for_certificate


def _build_test_png_bytes() -> bytes:
    image = Image.new("RGB", (10, 10), color="white")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def test_health_check(client):  # noqa: ANN001
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"]


def test_upload_accepts_valid_image(client):  # noqa: ANN001
    response = client.post(
        "/api/v1/analyses/upload",
        files={"file": ("certificado.png", _build_test_png_bytes(), "image/png")},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["accepted"] is True
    assert body["filename"] == "certificado.png"


def test_upload_rejects_invalid_extension(client):  # noqa: ANN001
    response = client.post(
        "/api/v1/analyses/upload",
        files={"file": ("certificado.txt", b"hola", "text/plain")},
    )
    assert response.status_code == 400
    assert "Formato de archivo no soportado" in response.json()["detail"]


def test_analyze_and_fetch_result(client):  # noqa: ANN001
    analyze_response = client.post(
        "/api/v1/analyses",
        files={"file": ("certificado.png", _build_test_png_bytes(), "image/png")},
    )
    assert analyze_response.status_code == 201
    body = analyze_response.json()
    analysis_id = body["id"]
    assert body["analysis"]["persona"]["nombre_completo"] == "Ana Perez"

    get_response = client.get(f"/api/v1/analyses/{analysis_id}")
    assert get_response.status_code == 200
    fetched = get_response.json()
    assert fetched["id"] == analysis_id
    assert fetched["analysis"]["metadata"]["estado"] == "success"


def test_analyze_accepts_optional_form_and_observations(client):  # noqa: ANN001
    response = client.post(
        "/api/v1/analyses",
        files={
            "file": ("certificado.png", _build_test_png_bytes(), "image/png"),
            "form_file": ("entrevista.png", _build_test_png_bytes(), "image/png"),
        },
        data={"observations": "Persona oralizada. Usa audifonos."},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["analysis"]["persona"]["nombre_completo"] == "Ana Perez"


def test_html_export_returns_markup(client):  # noqa: ANN001
    analyze_response = client.post(
        "/api/v1/analyses",
        files={"file": ("certificado.png", _build_test_png_bytes(), "image/png")},
    )
    analysis_id = analyze_response.json()["id"]
    html_response = client.get(f"/api/v1/analyses/{analysis_id}/html")
    assert html_response.status_code == 200
    assert "<html" in html_response.text.lower()


def test_pdf_export_returns_pdf_attachment(client):  # noqa: ANN001
    analyze_response = client.post(
        "/api/v1/analyses",
        files={"file": ("certificado.png", _build_test_png_bytes(), "image/png")},
    )
    analysis_id = analyze_response.json()["id"]
    pdf_response = client.get(f"/api/v1/analyses/{analysis_id}/pdf")
    assert pdf_response.status_code == 200
    assert pdf_response.headers["content-type"] == "application/pdf"
    assert (
        pdf_response.headers["content-disposition"]
        == 'attachment; filename="informe_laboral_inclusivo.pdf"'
    )
    assert pdf_response.content.startswith(b"%PDF")


def test_pdf_export_returns_404_for_unknown_analysis(client):  # noqa: ANN001
    pdf_response = client.get("/api/v1/analyses/no-existe/pdf")
    assert pdf_response.status_code == 404


def test_auditiva_only_guardrails_remove_unsustained_physical_restrictions() -> None:
    payload = {
        "discapacidades_raw": [
            {"nombre": "FÃ­sica", "marcado": "NO"},
            {"nombre": "Visual", "marcado": "NO"},
            {"nombre": "Auditiva", "marcado": "SI"},
            {"nombre": "Intelectual", "marcado": "NO"},
            {"nombre": "Psicosocial", "marcado": "NO"},
            {"nombre": "Sordoceguera", "marcado": "NO"},
            {"nombre": "MÃºltiple", "marcado": "NO"},
        ],
        "discapacidades_activas": ["Auditiva"],
        "dominios": {
            "cognicion": 10,
            "movilidad": 0,
            "cuidado_personal": 0,
            "relaciones": 15,
            "vida_diaria": 5,
            "participacion": 34.38,
        },
        "analisis": {
            "tareas_recomendadas": {
                "administrativo_oficina": ["Gestion documental por canales escritos."],
                "operativo_manual_liviano": ["Evitar esfuerzo fisico y movilidad intensa."],
                "relacional_apoyo": ["Atencion telefonica directa al cliente."],
            },
            "ajustes_razonables": [
                {
                    "titulo": "Ergonomia por discapacidad fisica",
                    "descripcion": "Reducir esfuerzo corporal y cargue de peso.",
                    "fundamento": "Discapacidad fisica y auditiva.",
                }
            ],
            "tareas_no_recomendadas": [
                "Manipulacion de cargas y cargue de peso repetitivo.",
                "Atencion telefonica exclusiva sin apoyo escrito.",
            ],
            "perfil_funcionamiento": "Presenta discapacidad fisica/auditiva con limitaciones de movilidad y esfuerzo corporal.",
            "recomendaciones_rrhh_sst": [
                "Evitar desplazamientos prolongados por la discapacidad fisica.",
                "Confirmar instrucciones por escrito.",
            ],
        },
    }

    normalized = normalize_analysis_for_certificate(
        payload,
        used_vision=False,
        observations="Usa audifono. Puede comunicarse oralmente.",
    )
    serialized = str(normalized).lower()

    assert payload["discapacidades_activas"] == ["Auditiva"]
    assert "discapacidad fisica" not in serialized
    assert "cargue de peso" not in serialized
    assert "manipulacion de cargas" not in serialized
    assert "movilidad intensa" not in serialized
    assert "esfuerzo corporal" not in serialized
    assert "participacion presenta dificultad moderada" in serialized
    assert "incorporacion gradual" in serialized or "participacion gradual" in serialized
    assert "audifono" in serialized
    assert "no depender exclusivamente de llamadas" in serialized
    assert "instrucciones escritas" in serialized or "por escrito" in serialized
