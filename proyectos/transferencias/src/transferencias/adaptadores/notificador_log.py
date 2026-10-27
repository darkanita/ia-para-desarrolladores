"""Notificador que escribe en el log. En producción enviaría un correo o una notificación push."""
from __future__ import annotations

import logging

from transferencias.dominio.modelo.transferencia import Transferencia

log = logging.getLogger("transferencias")


def _enmascarar(cuenta: str) -> str:
    return "*" * (len(cuenta) - 4) + cuenta[-4:]


class NotificadorLog:
    def transferencia_realizada(self, transferencia: Transferencia) -> None:
        log.info("Transferencia %s: %s -> %s por %s (GMF %s)", transferencia.referencia,
                 _enmascarar(transferencia.origen), _enmascarar(transferencia.destino),
                 transferencia.monto, transferencia.gmf)
