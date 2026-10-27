"""Punto de entrada por línea de comandos: arma las dependencias y llama a los casos de uso."""
from __future__ import annotations

import argparse
import logging
import sys
from decimal import Decimal, InvalidOperation

from transferencias.adaptadores.notificador_log import NotificadorLog
from transferencias.adaptadores.repositorio_json import RepositorioCuentasJson, RepositorioTransferenciasJson
from transferencias.app import config
from transferencias.dominio.casos_uso.consultar_movimientos import ConsultarMovimientos
from transferencias.dominio.casos_uso.realizar_transferencia import RealizarTransferencia
from transferencias.dominio.modelo.errores import ErrorTransferencia


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    p = argparse.ArgumentParser(prog="transferencias", description="Transferencias entre cuentas")
    sub = p.add_subparsers(dest="comando", required=True)
    t = sub.add_parser("transferir", help="Transfiere entre dos cuentas")
    t.add_argument("origen")
    t.add_argument("destino")
    t.add_argument("monto")
    m = sub.add_parser("movimientos", help="Últimas transferencias de una cuenta")
    m.add_argument("cuenta")
    m.add_argument("--ultimos", type=int, default=10)
    args = p.parse_args(argv)

    cfg = config.cargar()
    cuentas = RepositorioCuentasJson(cfg.archivo_cuentas)
    historial = RepositorioTransferenciasJson(cfg.archivo_transferencias)
    try:
        if args.comando == "transferir":
            try:
                monto = Decimal(args.monto)
            except InvalidOperation:
                print(f"Monto inválido: {args.monto}", file=sys.stderr)
                return 2
            caso = RealizarTransferencia(cuentas, historial, NotificadorLog(), cfg.limite_diario)
            tr = caso.ejecutar(args.origen, args.destino, monto)
            print(f"OK {tr.referencia}: debitado {tr.total_debitado} (GMF {tr.gmf})")
        else:
            for tr in ConsultarMovimientos(cuentas, historial).ejecutar(args.cuenta, args.ultimos):
                signo = "-" if tr.origen == args.cuenta else "+"
                print(f"{tr.fecha:%Y-%m-%d %H:%M} {tr.referencia} {signo}{tr.monto}")
    except ErrorTransferencia as e:
        print(f"Rechazada ({type(e).__name__}): {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
