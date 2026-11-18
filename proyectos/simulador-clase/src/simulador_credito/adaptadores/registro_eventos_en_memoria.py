"""Adaptador para pruebas: guarda los eventos en una lista para verificarlos."""


class RegistroEventosEnMemoria:
    """Doble del puerto RegistroEventos. Cada evento queda como dict con nivel, evento y regla."""

    def __init__(self) -> None:
        self.eventos: list[dict[str, str | None]] = []

    def registrar(self, nivel: str, evento: str, regla: str | None = None) -> None:
        """Guarda el evento en memoria."""
        self.eventos.append({"nivel": nivel, "evento": evento, "regla": regla})
