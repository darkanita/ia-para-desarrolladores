"""Interfaz del asesor (Streamlit): captura los datos, llama a simular_credito y muestra el resultado.

Ejecutar: python -m streamlit run src/simulador_credito/app/interfaz_asesor.py
"""
import os
from decimal import Decimal
from pathlib import Path

import streamlit as st

from simulador_credito.adaptadores.parametros_desde_banco import ProveedorParametrosDesdeBanco
from simulador_credito.adaptadores.registro_eventos_json import RegistroEventosJson
from simulador_credito.casos_uso.simular_credito import simular_credito
from simulador_credito.dominio.entradas import ErrorEntrada, convertir_decimal
from simulador_credito.dominio.reglas import formatear_pesos, formatear_porcentaje
from simulador_credito.dominio.simulacion import DatosSimulacion

RAIZ = Path(__file__).resolve().parents[3]
RUTA_BANCO = RAIZ / "banco.yaml"
RUTA_LOG = Path(os.environ.get("SIMULADOR_LOG_RUTA", RAIZ / "logs" / "simulador_credito.jsonl"))

st.title("Simulador de crédito de consumo")

with st.form("simulacion"):
    monto_texto = st.text_input("Monto (COP)", key="monto")
    plazo_texto = st.text_input("Plazo (meses)", key="plazo")
    tasa_texto = st.text_input("Tasa efectiva anual (por ejemplo 26 %)", key="tasa")
    ingresos_texto = st.text_input("Ingresos mensuales (COP)", key="ingresos")
    otras_texto = st.text_input("Otras cuotas mensuales (COP)", key="otras_cuotas")
    sin_otras_cuotas = st.checkbox("El cliente no tiene otras cuotas (0 COP)", key="confirmo_otras_cero")
    enviado = st.form_submit_button("Simular", key="simular")

if enviado:
    try:
        otras = Decimal("0") if (sin_otras_cuotas and otras_texto.strip() == "") else convertir_decimal(
            otras_texto, "otras_cuotas"
        )
        datos = DatosSimulacion(
            monto=convertir_decimal(monto_texto, "monto"),
            plazo_meses=int(convertir_decimal(plazo_texto, "plazo")),
            tasa_ea=convertir_decimal(tasa_texto, "tasa"),
            ingresos=convertir_decimal(ingresos_texto, "ingresos"),
            otras_cuotas=otras,
        )
    except ErrorEntrada as error:
        st.error(error.mensaje)
    else:
        try:
            resultado = simular_credito(datos, ProveedorParametrosDesdeBanco(RUTA_BANCO), RegistroEventosJson(RUTA_LOG))
        except Exception:  # el detalle técnico no se muestra al asesor ni se registra con datos del cliente
            RegistroEventosJson(RUTA_LOG).registrar("ERROR", "error_inesperado")
            st.error("No fue posible completar la simulación. Intente de nuevo.")
        else:
            if resultado.endeudamiento is not None:
                veredicto = "le alcanza" if resultado.motivo is None else "no le alcanza"
                st.markdown(f"**Endeudamiento:** {formatear_porcentaje(resultado.endeudamiento)}: {veredicto}")
            if resultado.valido:
                st.success("Simulación válida")
                st.markdown(f"**Cuota mensual:** {formatear_pesos(resultado.cuota)} {resultado.moneda}")
                st.markdown(f"**Costo total:** {formatear_pesos(resultado.costo_total)} {resultado.moneda}")
                st.markdown(f"**Plazo:** {resultado.plazo_meses} meses")
            else:
                st.error(resultado.motivo.mensaje)
            st.info(resultado.aviso)
