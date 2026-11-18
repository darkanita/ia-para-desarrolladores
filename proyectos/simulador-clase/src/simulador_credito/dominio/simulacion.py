"""Modelos de la simulación: parámetros del producto, datos del asesor y resultado. Sin frameworks."""
from dataclasses import dataclass
from decimal import Decimal

from simulador_credito.dominio.reglas import MotivoRechazo

# Texto pendiente de la pregunta 8 de la especificación (lo define el área legal o de producto).
aviso_simulacion = "Esta es una simulación. No es una oferta de crédito."


@dataclass(frozen=True)
class ParametrosProducto:
    """Límites del crédito de consumo, leídos de banco.yaml (productos.credito_consumo)."""

    monto_minimo: Decimal
    monto_maximo: Decimal
    plazo_minimo: int
    plazo_maximo: int
    tasa_maxima_ea: Decimal
    endeudamiento_maximo: Decimal


@dataclass(frozen=True)
class DatosSimulacion:
    """Datos digitados por el asesor ya convertidos a Decimal y validados en el borde."""

    monto: Decimal
    plazo_meses: int
    tasa_ea: Decimal
    ingresos: Decimal
    otras_cuotas: Decimal


@dataclass(frozen=True)
class ResultadoSimulacion:
    """Resultado de la simulación. Si no es válido, cuota y costo total quedan vacíos."""

    valido: bool
    plazo_meses: int
    moneda: str = "COP"
    cuota: Decimal | None = None
    costo_total: Decimal | None = None
    endeudamiento: Decimal | None = None
    motivo: MotivoRechazo | None = None
    aviso: str = aviso_simulacion
