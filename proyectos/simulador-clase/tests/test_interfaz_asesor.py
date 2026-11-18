"""Prueba de la interfaz del asesor con streamlit.testing (RF-06). El log va a un archivo temporal."""
from pathlib import Path

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
