"""Prueba de la interfaz del asesor con streamlit.testing (RF-06). El log va a un archivo temporal."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from simulador_credito.dominio.simulacion import aviso_simulacion

RUTA_APP = Path(__file__).resolve().parents[1] / "src" / "simulador_credito" / "app" / "interfaz_asesor.py"


def test_aviso_visible_en_interfaz(tmp_path, monkeypatch):
    """Regla: RF-06. Una simulación válida muestra en pantalla el aviso de simulación, no oferta."""
    monkeypatch.setenv("SIMULADOR_LOG_RUTA", str(tmp_path / "eventos.jsonl"))
    at = AppTest.from_file(str(RUTA_APP), default_timeout=20).run()

    at.text_input(key="monto").input("10000000")
    at.text_input(key="plazo").input("36")
    at.text_input(key="tasa").input("26")
    at.text_input(key="ingresos").input("4000000")
    at.text_input(key="otras_cuotas").input("500000")
    at.button(key="simular").click().run()

    assert not at.exception
    textos = [aviso.value for aviso in at.info]
    assert aviso_simulacion in textos


def test_interfaz_rechaza_exceso(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Regla: productos.credito_consumo.endeudamiento_maximo (RN-05). El redondeo visual no permite el exceso."""
    monkeypatch.setenv("SIMULADOR_LOG_RUTA", str(tmp_path / "eventos.jsonl"))
    at = AppTest.from_file(str(RUTA_APP), default_timeout=20).run()

    at.text_input(key="monto").input("10000000")
    at.text_input(key="plazo").input("36")
    at.text_input(key="tasa").input("26")
    at.text_input(key="ingresos").input("2219900")
    at.text_input(key="otras_cuotas").input("500000")
    at.button(key="simular").click().run()

    assert not at.exception
    assert not at.success
    assert at.error
    assert "supera el máximo permitido de 40 %" in at.error[0].value
    textos = [elemento.value for elemento in at.markdown]
    assert "**Endeudamiento:** 40 %: no le alcanza" in textos
    assert not any("Cuota mensual" in texto or "Costo total" in texto for texto in textos)
    assert aviso_simulacion in [aviso.value for aviso in at.info]
