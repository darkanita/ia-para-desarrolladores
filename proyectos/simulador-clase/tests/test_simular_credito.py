"""Pruebas del caso de uso simular_credito con dobles en memoria (RF-02 moneda, RF-04, RF-05, RF-06, logs)."""
from decimal import Decimal

from simulador_credito.adaptadores.parametros_en_memoria import ProveedorParametrosEnMemoria
from simulador_credito.adaptadores.registro_eventos_en_memoria import RegistroEventosEnMemoria
from simulador_credito.casos_uso.simular_credito import simular_credito
from simulador_credito.dominio.simulacion import (
    DatosSimulacion,
    ParametrosProducto,
    aviso_simulacion,
)

PARAMETROS = ParametrosProducto(
    monto_minimo=Decimal("1000000"),
    monto_maximo=Decimal("100000000"),
    plazo_minimo=6,
    plazo_maximo=72,
    tasa_maxima_ea=Decimal("0.26"),
    endeudamiento_maximo=Decimal("0.40"),
)


def _simular(datos: DatosSimulacion, registro: RegistroEventosEnMemoria | None = None):
    """Ejecuta el caso de uso con parámetros en memoria y un registro en memoria."""
    registro = registro or RegistroEventosEnMemoria()
    resultado = simular_credito(datos, ProveedorParametrosEnMemoria(PARAMETROS), registro)
    return resultado, registro


def _datos_validos() -> DatosSimulacion:
    """Monto 10.000.000, 36 meses, 26 % E.A., ingresos 4.000.000 y otras cuotas 500.000 (sintéticos)."""
    return DatosSimulacion(
        monto=Decimal("10000000"),
        plazo_meses=36,
        tasa_ea=Decimal("0.26"),
        ingresos=Decimal("4000000"),
        otras_cuotas=Decimal("500000"),
    )


def _datos_monto_bajo() -> DatosSimulacion:
    """Monto 999.999: rechaza por RN-01."""
    return DatosSimulacion(
        monto=Decimal("999999"),
        plazo_meses=36,
        tasa_ea=Decimal("0.26"),
        ingresos=Decimal("4000000"),
        otras_cuotas=Decimal("500000"),
    )


def test_resultado_valido_muestra_aviso():
    """Regla: RF-06. Toda simulación válida muestra el aviso de simulación, no oferta."""
    resultado, _ = _simular(_datos_validos())
    assert resultado.valido is True
    assert resultado.cuota == Decimal("388846")
    assert resultado.aviso == aviso_simulacion


def test_rechazo_no_muestra_cuota_ni_costo():
    """Regla: RF-04 y RF-06. Una simulación rechazada no muestra cuota ni costo total."""
    resultado, _ = _simular(_datos_monto_bajo())
    assert resultado.valido is False
    assert resultado.cuota is None
    assert resultado.costo_total is None


def test_rechazo_muestra_motivo_y_aviso():
    """Regla: RF-06. Un rechazo muestra solo el motivo y el aviso."""
    resultado, _ = _simular(_datos_monto_bajo())
    assert resultado.motivo is not None
    assert resultado.motivo.regla == "RN-01"
    assert resultado.motivo.mensaje == "El monto mínimo es 1.000.000 COP."
    assert resultado.aviso == aviso_simulacion


def test_rechazo_registra_warning():
    """Regla: politicas.logs. Una regla rechazada se registra en WARNING con el id de la regla, sin datos restringidos."""
    _, registro = _simular(_datos_monto_bajo())
    assert len(registro.eventos) == 1
    evento = registro.eventos[0]
    assert evento["nivel"] == "WARNING"
    assert evento["regla"] == "RN-01"
    assert "4000000" not in str(evento) and "500000" not in str(evento)


def test_misma_entrada_mismo_resultado():
    """Regla: RF-05. Los mismos datos de entrada dan exactamente el mismo resultado."""
    primero, _ = _simular(_datos_validos())
    segundo, _ = _simular(_datos_validos())
    assert primero == segundo


def test_resultado_muestra_costo_en_cop():
    """Regla: RF-02. El costo total aparece junto a la cuota y al plazo, en COP."""
    resultado, _ = _simular(_datos_validos())
    assert resultado.costo_total == Decimal("13998456")
    assert resultado.moneda == "COP"
    assert resultado.plazo_meses == 36


def test_endeudamiento_excedido_muestra_indicador_sin_cuota():
    """Regla: RF-04 y D5. Endeudamiento de 52,6 % muestra el indicador y no lo presenta como válido, sin cuota ni costo."""
    datos = DatosSimulacion(
        monto=Decimal("10000000"),
        plazo_meses=36,
        tasa_ea=Decimal("0.26"),
        ingresos=Decimal("1500000"),
        otras_cuotas=Decimal("400000"),
    )
    resultado, registro = _simular(datos)
    assert resultado.valido is False
    assert resultado.motivo.regla == "RN-05"
    assert resultado.endeudamiento.quantize(Decimal("0.001")) == Decimal("0.526")
    assert resultado.cuota is None
    assert resultado.costo_total is None
    assert registro.eventos[0]["nivel"] == "WARNING"


def test_ingresos_cero_no_calcula_endeudamiento():
    """Regla: RF-03. Con ingresos en 0 no hay endeudamiento que calcular: rechaza y pide ingresos mayores que cero."""
    datos = DatosSimulacion(
        monto=Decimal("10000000"),
        plazo_meses=36,
        tasa_ea=Decimal("0.26"),
        ingresos=Decimal("0"),
        otras_cuotas=Decimal("0"),
    )
    resultado, _ = _simular(datos)
    assert resultado.valido is False
    assert resultado.endeudamiento is None
    assert resultado.motivo.mensaje == "Los ingresos deben ser mayores que cero."
