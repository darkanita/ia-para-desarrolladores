"""Pruebas del registro de eventos en JSON (política de logs). Usa un archivo temporal."""
import json
from decimal import Decimal

from simulador_credito.adaptadores.parametros_en_memoria import ProveedorParametrosEnMemoria
from simulador_credito.adaptadores.registro_eventos_json import RegistroEventosJson
from simulador_credito.casos_uso.simular_credito import simular_credito
from simulador_credito.dominio.simulacion import DatosSimulacion, ParametrosProducto

CAMPOS_ESPERADOS = {"fecha", "nivel", "servicio", "id_correlacion", "evento", "regla"}


def test_registro_json_no_incluye_ingresos_ni_otras_cuotas(tmp_path):
    """Regla: politicas.logs y datos.reglas. Un evento tiene los campos del formato y ni ingresos ni otras cuotas."""
    ruta = tmp_path / "eventos.jsonl"
    registro = RegistroEventosJson(ruta)
    parametros = ProveedorParametrosEnMemoria(
        ParametrosProducto(
            monto_minimo=Decimal("1000000"),
            monto_maximo=Decimal("100000000"),
            plazo_minimo=6,
            plazo_maximo=72,
            tasa_maxima_ea=Decimal("0.26"),
            endeudamiento_maximo=Decimal("0.40"),
        )
    )
    # Datos sintéticos: ingresos 1.500.000 y otras cuotas 400.000 (cifras que no deben aparecer en el log).
    datos = DatosSimulacion(
        monto=Decimal("10000000"),
        plazo_meses=36,
        tasa_ea=Decimal("0.26"),
        ingresos=Decimal("1500000"),
        otras_cuotas=Decimal("400000"),
    )

    simular_credito(datos, parametros, registro)

    texto = ruta.read_text(encoding="utf-8")
    lineas = [json.loads(linea) for linea in texto.splitlines()]
    assert len(lineas) == 1
    assert set(lineas[0]) == CAMPOS_ESPERADOS
    assert lineas[0]["nivel"] == "WARNING"
    assert lineas[0]["regla"] == "RN-05"
    assert lineas[0]["servicio"] == "simulador_credito"
    assert "1500000" not in texto
    assert "400000" not in texto
