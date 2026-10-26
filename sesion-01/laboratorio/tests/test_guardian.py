"""Pruebas del laboratorio S1. No las modifiques: tu código debe hacerlas pasar."""
import math

import pytest

import guardian_prompt as g


# ---------------------------------------------------------------- Parte 1
class TestTokensYCosto:
    def test_texto_vacio_es_cero(self):
        assert g.contar_tokens("") == 0

    def test_texto_no_vacio_tiene_tokens(self):
        assert g.contar_tokens("def f(x): return x") > 0

    def test_mas_texto_mas_tokens(self):
        corto = "saldo = cuenta.saldo"
        assert g.contar_tokens(corto * 10) > g.contar_tokens(corto)

    def test_aproximacion_sin_tokenizador(self, monkeypatch):
        monkeypatch.setattr(g, "_ENC", None)
        assert g.contar_tokens("abcdefghi") == math.ceil(9 / 4)

    def test_costo_basico(self):
        # 1M de entrada a 2.5 + 500k de salida a 10 = 2.5 + 5 = 7.5
        assert g.estimar_costo_usd(1_000_000, 500_000, 2.5, 10.0) == pytest.approx(7.5)

    def test_costo_redondeado_a_6_decimales(self):
        # 1234 * 0.15 / 1M = 0.0001851 → 0.000185
        assert g.estimar_costo_usd(1234, 0, 0.15, 0) == 0.000185

    def test_costo_negativo_falla(self):
        with pytest.raises(ValueError):
            g.estimar_costo_usd(-1, 0, 2.5, 10)


# ---------------------------------------------------------------- Parte 2
class TestLuhn:
    @pytest.mark.parametrize("numero", ["4111111111111111", "4111 1111 1111 1111", "5500-0000-0000-0004"])
    def test_validos(self, numero):
        assert g.es_luhn_valido(numero)

    @pytest.mark.parametrize("numero", ["4111111111111112", "1234567890123456", ""])
    def test_invalidos(self, numero):
        assert not g.es_luhn_valido(numero)


class TestRedaccion:
    def test_email(self):
        texto, c = g.redactar_datos_sensibles("notificar a ana.perez@banco.com.co hoy")
        assert texto == "notificar a [EMAIL] hoy"
        assert c["EMAIL"] == 1

    def test_tarjeta_valida_se_redacta(self):
        texto, c = g.redactar_datos_sensibles("tarjeta = '4111 1111 1111 1111'")
        assert "[TARJETA]" in texto and "4111" not in texto
        assert c["TARJETA"] == 1

    def test_numero_largo_no_luhn_se_conserva(self):
        texto, c = g.redactar_datos_sensibles("id_transaccion = 1234567890123456")
        assert "1234567890123456" in texto
        assert c["TARJETA"] == 0

    @pytest.mark.parametrize(
        "entrada, esperado",
        [
            ("cedula: 1036123456", "cedula: [CEDULA]"),
            ("CC 43123456", "CC [CEDULA]"),
            ("c.c.=71234567", "c.c.=[CEDULA]"),
            ("Cédula #98765432", "Cédula #[CEDULA]"),
        ],
    )
    def test_cedula_con_palabra_clave(self, entrada, esperado):
        texto, c = g.redactar_datos_sensibles(entrada)
        assert texto == esperado
        assert c["CEDULA"] == 1

    def test_numero_sin_palabra_clave_no_es_cedula(self):
        texto, c = g.redactar_datos_sensibles("timeout = 30000000")
        assert texto == "timeout = 30000000"
        assert c["CEDULA"] == 0

    @pytest.mark.parametrize(
        "secreto",
        [
            "sk-proj-AbCdEfGhIjKlMnOpQrStUvWx",
            "AKIAABCDEFGHIJKLMNOP",
            "ghp_" + "a1B2" * 9,
        ],
    )
    def test_llaves_conocidas(self, secreto):
        texto, c = g.redactar_datos_sensibles(f"cliente = Cliente(llave='{secreto}')")
        assert secreto not in texto and "[SECRETO]" in texto
        assert c["SECRETO"] == 1

    @pytest.mark.parametrize(
        "entrada, esperado",
        [
            ('password = "Banco2026*"', 'password = "[SECRETO]"'),
            ("API_KEY: 'xyz-123'", "API_KEY: '[SECRETO]'"),
            ('clave="abc"', 'clave="[SECRETO]"'),
        ],
    )
    def test_asignacion_de_secretos(self, entrada, esperado):
        texto, c = g.redactar_datos_sensibles(entrada)
        assert texto == esperado
        assert c["SECRETO"] == 1

    def test_conteo_tiene_todas_las_llaves(self):
        _, c = g.redactar_datos_sensibles("sin nada sensible")
        assert c == {"EMAIL": 0, "TARJETA": 0, "CEDULA": 0, "SECRETO": 0}

    def test_texto_mixto(self):
        codigo = (
            "def notificar():\n"
            "    destino = 'soporte@empresa.co'\n"
            "    token = 'tok-9988'\n"
            "    # cliente con cedula 1036123456 y tarjeta 5500 0000 0000 0004\n"
        )
        texto, c = g.redactar_datos_sensibles(codigo)
        assert c == {"EMAIL": 1, "TARJETA": 1, "CEDULA": 1, "SECRETO": 1}
        for dato in ["soporte@empresa.co", "tok-9988", "1036123456", "5500 0000 0000 0004"]:
            assert dato not in texto
        assert texto.startswith("def notificar():\n")


# ---------------------------------------------------------------- Parte 3
class TestPrepararContexto:
    def test_estructura_de_respuesta(self):
        r = g.preparar_contexto("x = 1\n", max_tokens=100)
        assert set(r) == {"texto", "tokens", "costo_usd", "hallazgos", "recortado"}
        assert r["recortado"] is False
        assert r["tokens"] == g.contar_tokens(r["texto"])

    def test_redacta_antes_de_contar(self):
        r = g.preparar_contexto("correo = 'a@b.co'\n", max_tokens=100)
        assert "[EMAIL]" in r["texto"]
        assert r["hallazgos"]["EMAIL"] == 1

    def test_costo_usa_precio_de_entrada(self):
        r = g.preparar_contexto("x = 1\n" * 5, max_tokens=1000, precio_entrada_1m=1_000_000)
        assert r["costo_usd"] == pytest.approx(r["tokens"])

    def test_excede_sin_recortar_lanza_error(self):
        with pytest.raises(g.ContextoExcedidoError):
            g.preparar_contexto("linea de codigo\n" * 200, max_tokens=20)

    def test_excede_con_recorte_quita_lineas_del_final(self):
        codigo = "".join(f"paso_{i} = {i}\n" for i in range(200))
        r = g.preparar_contexto(codigo, max_tokens=30, recortar=True)
        assert r["recortado"] is True
        assert r["tokens"] <= 30
        assert r["texto"].startswith("paso_0 = 0\n")
        assert r["texto"].endswith("\n")  # se recortan líneas completas
