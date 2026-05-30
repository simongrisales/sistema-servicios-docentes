from unittest.mock import patch

from rest_framework import status

import core.sanitizers as sanitizers
from core.exceptions import (
    AulaConflictoError,
    CapacidadInsuficienteError,
    CredencialesInvalidasError,
    PermisoInsuficienteError,
    ReservaConflictoError,
    SistemaBaseError,
    SystemException,
)
from core.sanitizers import BleachSanitizerMixin, sanitize_text


class PayloadSanitizer(BleachSanitizerMixin):
    text_fields = ("nombre", "descripcion")


def test_sanitize_text_remueve_tags_peligrosos():
    assert "<script>" not in sanitize_text("<script>alert(1)</script><b>Aula</b>")


def test_bleach_sanitizer_mixin_solo_limpia_campos_de_texto():
    payload = {
        "nombre": "<b>Aula</b>",
        "descripcion": "<script>alert(1)</script>",
        "capacidad": 40,
    }

    sanitized = PayloadSanitizer().sanitize_payload(payload)

    assert sanitized["capacidad"] == 40
    assert "<script>" not in sanitized["descripcion"]
    assert payload["descripcion"] != sanitized["descripcion"]


def test_sanitize_text_usa_fallback_sin_bleach():
    original_bleach = sanitizers.bleach
    with patch.object(sanitizers, "bleach", None):
        output = sanitizers.sanitize_text("<b>Aula</b><script>alert(1)</script>")

    assert "script" not in output.lower()
    assert "Aula" in output
    assert sanitizers.bleach is original_bleach


def test_bleach_sanitizer_mixin_no_modifica_campos_no_texto():
    class EmptySanitizer(BleachSanitizerMixin):
        text_fields = ()

    payload = {"valor": 10, "descripcion": "<b>ok</b>"}

    sanitized = EmptySanitizer().sanitize_payload(payload)

    assert sanitized == payload


def test_excepciones_core_exponen_status_code_http():
    assert SystemException is SistemaBaseError
    assert SistemaBaseError("x").status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert (
        SistemaBaseError("x", status.HTTP_418_IM_A_TEAPOT).status_code
        == status.HTTP_418_IM_A_TEAPOT
    )
    assert CredencialesInvalidasError().status_code == status.HTTP_401_UNAUTHORIZED
    assert PermisoInsuficienteError().status_code == status.HTTP_403_FORBIDDEN
    assert AulaConflictoError().status_code == status.HTTP_409_CONFLICT
    assert CapacidadInsuficienteError().status_code == status.HTTP_400_BAD_REQUEST
    assert ReservaConflictoError().status_code == status.HTTP_409_CONFLICT
