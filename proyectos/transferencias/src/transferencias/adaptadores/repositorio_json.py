"""Repositorios que guardan en archivos JSON. Sirven para desarrollo local; en producción irían a la base de datos."""
from __future__ import annotations

import json
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from transferencias.dominio.modelo.cuenta import Cuenta, EstadoCuenta, TipoCuenta
from transferencias.dominio.modelo.transferencia import Transferencia


class RepositorioCuentasJson:
    def __init__(self, archivo: Path) -> None:
        self._archivo = archivo
        datos = json.loads(archivo.read_text(encoding="utf-8"))
        self._cuentas = {c["numero"]: Cuenta(
            numero=c["numero"], titular_id=c["titular_id"], tipo=TipoCuenta(c["tipo"]),
            saldo=Decimal(c["saldo"]), estado=EstadoCuenta(c["estado"]), exenta_gmf=c.get("exenta_gmf", False),
        ) for c in datos}

    def obtener(self, numero: str) -> Cuenta | None:
        return self._cuentas.get(numero)

    def guardar(self, cuenta: Cuenta) -> None:
        self._cuentas[cuenta.numero] = cuenta
        self._archivo.write_text(json.dumps([{
            "numero": c.numero, "titular_id": c.titular_id, "tipo": c.tipo.value, "saldo": str(c.saldo),
            "estado": c.estado.value, "exenta_gmf": c.exenta_gmf,
        } for c in self._cuentas.values()], indent=2, ensure_ascii=False), encoding="utf-8")


class RepositorioTransferenciasJson:
    def __init__(self, archivo: Path) -> None:
        self._archivo = archivo
        self._lista: list[Transferencia] = []
        if archivo.exists():
            self._lista = [Transferencia(t["origen"], t["destino"], Decimal(t["monto"]), Decimal(t["gmf"]),
                                         datetime.fromisoformat(t["fecha"]), t["referencia"])
                           for t in json.loads(archivo.read_text(encoding="utf-8"))]

    def registrar(self, transferencia: Transferencia) -> None:
        self._lista.append(transferencia)
        self._archivo.write_text(json.dumps([{
            "origen": t.origen, "destino": t.destino, "monto": str(t.monto), "gmf": str(t.gmf),
            "fecha": t.fecha.isoformat(), "referencia": t.referencia,
        } for t in self._lista], indent=2), encoding="utf-8")

    def total_debitado_en(self, cuenta: str, dia: date) -> Decimal:
        return sum((t.monto for t in self._lista if t.origen == cuenta and t.fecha.date() == dia), Decimal("0"))

    def de_cuenta(self, cuenta: str) -> list[Transferencia]:
        return [t for t in self._lista if cuenta in (t.origen, t.destino)]
