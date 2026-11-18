"""Puerto: a dónde van los eventos de negocio y los rechazos. Solo el contrato."""
from typing import Protocol


class RegistroEventos(Protocol):
    """Registra un evento con su nivel. Nunca recibe datos restringidos, solo el id de la regla."""

    def registrar(self, nivel: str, evento: str, regla: str | None = None) -> None:
        """Registra el evento; regla es el id de la regla incumplida (por ejemplo RN-01), si aplica."""
        ...
