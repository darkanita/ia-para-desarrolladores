"""Adaptador real: escribe cada evento como una línea JSON. Nunca recibe datos restringidos, solo el id de la regla."""
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path


class RegistroEventosJson:
    """Implementa RegistroEventos escribiendo en un archivo JSON Lines."""

    def __init__(self, ruta: Path, servicio: str = "simulador_credito") -> None:
        self._ruta = ruta
        self._servicio = servicio

    def registrar(self, nivel: str, evento: str, regla: str | None = None) -> None:
        """Agrega una línea con fecha, nivel, servicio, id de correlación, evento y regla."""
        registro = {
            "fecha": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "nivel": nivel,
            "servicio": self._servicio,
            "id_correlacion": uuid.uuid4().hex,
            "evento": evento,
            "regla": regla,
        }
        self._ruta.parent.mkdir(parents=True, exist_ok=True)
        with self._ruta.open("a", encoding="utf-8") as archivo:
            archivo.write(json.dumps(registro, ensure_ascii=False) + "\n")
