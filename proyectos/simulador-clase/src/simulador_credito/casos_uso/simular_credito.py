"""Caso de uso: validar las reglas del banco, calcular cuota, costo y endeudamiento, y registrar el evento."""

from simulador_credito.dominio.calculos import (
    calcular_costo_total,
    calcular_cuota_mensual,
    calcular_endeudamiento,
)
from simulador_credito.dominio.reglas import (
    MotivoRechazo,
    validar_endeudamiento,
    validar_ingresos,
    validar_monto,
    validar_plazo,
    validar_tasa,
)
from simulador_credito.dominio.simulacion import DatosSimulacion, ResultadoSimulacion
from simulador_credito.puertos.parametros_producto import ProveedorParametrosProducto
from simulador_credito.puertos.registro_eventos import RegistroEventos


def simular_credito(
    datos: DatosSimulacion,
    proveedor: ProveedorParametrosProducto,
    registro: RegistroEventos,
) -> ResultadoSimulacion:
    """Simula un crédito de consumo. Si una regla no se cumple, no muestra cuota ni costo total."""
    parametros = proveedor.obtener()
    motivo = (
        validar_monto(datos.monto, parametros.monto_minimo, parametros.monto_maximo)
        or validar_plazo(datos.plazo_meses, parametros.plazo_minimo, parametros.plazo_maximo)
        or validar_tasa(datos.tasa_ea, parametros.tasa_maxima_ea)
        or validar_ingresos(datos.ingresos)
    )
    if motivo is not None:
        return _rechazar(motivo, datos.plazo_meses, registro)

    cuota = calcular_cuota_mensual(datos.monto, datos.plazo_meses, datos.tasa_ea)
    endeudamiento = calcular_endeudamiento(cuota, datos.otras_cuotas, datos.ingresos)
    motivo = validar_endeudamiento(endeudamiento, parametros.endeudamiento_maximo)
    if motivo is not None:
        registro.registrar("WARNING", "simulacion_rechazada", motivo.regla)
        return ResultadoSimulacion(
            valido=False,
            plazo_meses=datos.plazo_meses,
            endeudamiento=endeudamiento,
            motivo=motivo,
        )

    registro.registrar("INFO", "simulacion_calculada")
    return ResultadoSimulacion(
        valido=True,
        plazo_meses=datos.plazo_meses,
        cuota=cuota,
        costo_total=calcular_costo_total(datos.monto, datos.plazo_meses, datos.tasa_ea),
        endeudamiento=endeudamiento,
    )


def _rechazar(motivo: MotivoRechazo, plazo_meses: int, registro: RegistroEventos) -> ResultadoSimulacion:
    """Arma un rechazo sin cuota ni costo y lo registra en WARNING con el id de la regla."""
    registro.registrar("WARNING", "simulacion_rechazada", motivo.regla)
    return ResultadoSimulacion(valido=False, plazo_meses=plazo_meses, motivo=motivo)
