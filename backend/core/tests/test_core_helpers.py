from rest_framework import status

from core.exceptions import (
    AulaConflictoError,
    CapacidadInsuficienteError,
    CredencialesInvalidasError,
    PermisoInsuficienteError,
    ReservaConflictoError,
    SistemaBaseError,
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


def test_excepciones_core_exponen_status_code_http():
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
