import re
from collections.abc import Mapping
from html import escape
from typing import Any

try:
    import bleach
except ImportError:  # pragma: no cover - fallback when dependency is absent locally
    bleach = None


def sanitize_text(value: str) -> str:
    if bleach is not None:
        return bleach.clean(value, strip=True)

    stripped = re.sub(r"<[^>]*>", "", value)
    return escape(stripped)


class BleachSanitizerMixin:
    """Mixin reutilizable para sanitizar campos de texto antes de persistir."""

    text_fields: tuple[str, ...] = ()

    def sanitize_payload(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        sanitized = dict(payload)
        for field in self.text_fields:
            value = sanitized.get(field)
            if isinstance(value, str):
                sanitized[field] = sanitize_text(value)
        return sanitized
