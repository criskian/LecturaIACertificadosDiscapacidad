from __future__ import annotations

from app.prompts.certificate_analysis_prompt import build_user_prompt


def _build(**overrides) -> str:
    params = {
        "extracted_text": "CERTIFICADO DE DISCAPACIDAD",
        "filename": "certificado.pdf",
        "used_vision": False,
    }
    params.update(overrides)
    return build_user_prompt(**params)


def test_resume_text_reaches_the_prompt() -> None:
    prompt = _build(resume_text="Auxiliar de control de calidad. Empaque y etiquetado.")

    assert "Hoja de vida de la persona" in prompt
    assert "Auxiliar de control de calidad" in prompt


def test_resume_section_states_its_absence_when_missing() -> None:
    prompt = _build()

    assert "[NO SE ADJUNTO HOJA DE VIDA O NO FUE POSIBLE EXTRAER TEXTO LEGIBLE]" in prompt


def test_resume_and_form_are_separate_sections() -> None:
    prompt = _build(
        form_text="Requiere confirmacion escrita de instrucciones.",
        resume_text="Analista de gestion documental con SGDEA.",
    )

    assert "Texto complementario de hoja de vida / formulario" in prompt
    assert "Hoja de vida de la persona" in prompt
    assert "Requiere confirmacion escrita" in prompt
    assert "SGDEA" in prompt
    # La hoja de vida se ubica despues del formulario y antes de la entrevista.
    assert prompt.index("Texto complementario de hoja de vida / formulario") < prompt.index("SGDEA")
    assert prompt.index("SGDEA") < prompt.index("Notas de entrevista de valoración")


def test_clinical_text_reaches_the_prompt() -> None:
    prompt = _build(clinical_text="Hipoacusia bilateral. Usa audifonos desde 2019.")

    assert "Historia clínica complementaria" in prompt
    assert "Hipoacusia bilateral" in prompt
