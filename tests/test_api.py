from __future__ import annotations

from io import BytesIO

from PIL import Image


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
    assert "attachment;" in pdf_response.headers["content-disposition"].lower()
    assert pdf_response.content.startswith(b"%PDF")
