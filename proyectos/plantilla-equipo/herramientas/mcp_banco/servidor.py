"""Servidor MCP del Banco Orquídea (ficticio): las herramientas del banco para el agente.

Expone herramientas que leen banco.yaml (no salen a internet ni tocan datos reales):
  - glosario            términos de negocio (GMF, tasa E.A., usura, capacidad de pago...)    · sesión 3
  - consultar_politica  la política del banco sobre un tema (datos, seguridad, nombres, logs...) · sesión 3
  - catalogo_servicios  las APIs internas ficticias que ya existen y su contrato             · sesión 3
  - validar_nombre      revisa que un nombre cumpla las convenciones del banco               · sesión 4

Claude Code lo arranca desde .mcp.json y Copilot desde .vscode/mcp.json. Habla MCP por
entrada y salida estándar (JSON-RPC 2.0, un mensaje por línea). Solo necesita PyYAML: el
protocolo está implementado aquí mismo para que funcione igual en cualquier máquina del curso.
En un proyecto real se usaría el SDK oficial de MCP para Python.

Uso:
    python herramientas/mcp_banco/servidor.py            # lo usan las herramientas, no usted
    python herramientas/mcp_banco/servidor.py --probar   # prueba rápida en la terminal
"""
from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path
from typing import Any, Callable

RAIZ = Path(__file__).resolve().parents[2]
BANCO = RAIZ / "banco.yaml"
NOMBRE, VERSION = "banco-orquidea", "1.1.0"
PROTOCOLOS = ["2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"]


# --------------------------------------------------------------------------- datos

def cargar_banco() -> dict[str, Any]:
    """Lee banco.yaml en cada llamada, para que un cambio se vea sin reiniciar."""
    import yaml  # PyYAML: pip install pyyaml

    with BANCO.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def normalizar(texto: str) -> str:
    """Minúsculas, sin tildes y con guion bajo: 'Tasa E.A.' -> 'tasa_e_a'."""
    sin_tildes = "".join(c for c in unicodedata.normalize("NFD", texto.lower()) if unicodedata.category(c) != "Mn")
    return "_".join("".join(c if c.isalnum() else " " for c in sin_tildes).split())


# --------------------------------------------------------------------------- herramientas

def glosario(termino: str = "") -> str:
    """Define un término de negocio del banco. Sin término, lista los disponibles."""
    terminos: dict[str, str] = cargar_banco().get("glosario", {})
    if not termino.strip():
        return "Términos del glosario: " + ", ".join(sorted(terminos))
    buscado = normalizar(termino)
    for clave, definicion in terminos.items():
        if buscado == clave or buscado.replace("_", "") == clave.replace("_", ""):
            return f"{clave}: {definicion}"
    parecidos = [c for c in terminos if buscado in c or c in buscado or buscado.split("_")[0] in c]
    if parecidos:
        return "\n".join(f"{c}: {terminos[c]}" for c in parecidos)
    return (f"'{termino}' no está en el glosario del banco. Términos disponibles: {', '.join(sorted(terminos))}. "
            "No invente una definición: anótelo como pregunta abierta.")


def consultar_politica(tema: str = "") -> str:
    """Devuelve la política del banco sobre un tema. Sin tema, lista los temas."""
    politicas: dict[str, dict[str, Any]] = cargar_banco().get("politicas", {})
    if not tema.strip():
        return "Temas con política: " + ", ".join(sorted(politicas))
    buscado = normalizar(tema)
    clave = next((c for c in politicas if c == buscado or c.rstrip("s") == buscado.rstrip("s")), None)
    if clave is None:
        clave = next((c for c in politicas if c in buscado or buscado in c), None)
    if clave is None:
        return (f"No hay una política sobre '{tema}'. Temas disponibles: {', '.join(sorted(politicas))}. "
                "Si el caso lo necesita, anótelo como pregunta abierta.")
    p = politicas[clave]
    reglas = "\n".join(f"  {i}. {r}" for i, r in enumerate(p.get("reglas", []), 1))
    return f"Política de {clave} (cite como politicas.{clave}):\n{p.get('resumen', '')}\n{reglas}"


def catalogo_servicios(busqueda: str = "") -> str:
    """Busca APIs internas del banco por nombre, descripción o campo. Sin búsqueda, las lista todas."""
    servicios: list[dict[str, Any]] = cargar_banco().get("catalogo_servicios", [])
    buscado = normalizar(busqueda)

    def coincide(s: dict[str, Any]) -> bool:
        if not buscado:
            return True
        texto = normalizar(json.dumps(s, ensure_ascii=False))
        return all(p in texto for p in buscado.split("_") if len(p) > 2) or buscado in texto

    encontrados = [s for s in servicios if coincide(s)]
    if not encontrados:
        nombres = ", ".join(s["nombre"] for s in servicios)
        return f"Ningún servicio coincide con '{busqueda}'. Servicios del catálogo: {nombres}."
    bloques = []
    for s in encontrados:
        lineas = [f"{s['nombre']} · {s.get('descripcion', '')} (dueño: {s.get('dueno', '?')})"]
        for op in s.get("operaciones", []):
            lineas.append(f"  {op['ruta']}")
            for etiqueta in ("recibe", "devuelve"):
                if op.get(etiqueta):
                    campos = ", ".join(f"{c} [{clas}]" for c, clas in op[etiqueta].items())
                    lineas.append(f"    {etiqueta}: {campos}")
        bloques.append("\n".join(lineas))
    return ("Servicios del catálogo (entre corchetes, la clasificación de cada campo según datos.clasificacion):\n\n"
            + "\n\n".join(bloques))


TIPOS_NOMBRE = ("modulo", "funcion", "variable", "clase", "caso_uso", "servicio", "ruta", "prueba", "paquete")


def _palabras(nombre: str) -> list[str]:
    """Separa snake_case, kebab-case, rutas y PascalCase en palabras en minúscula."""
    texto = "".join(f" {c}" if c.isupper() else c for c in nombre)
    return [p for p in normalizar(texto).split("_") if p]


def validar_nombre(tipo: str = "", nombre: str = "") -> str:
    """Revisa un nombre contra las convenciones del banco (convenciones y politicas.nombres)."""
    import re

    tipo = normalizar(tipo)
    if tipo not in TIPOS_NOMBRE or not nombre.strip():
        return f"Indique tipo ({', '.join(TIPOS_NOMBRE)}) y nombre. Ejemplo: validar_nombre('caso_uso', 'simular_credito')."
    nombre = nombre.strip()
    convenciones = cargar_banco().get("convenciones", {})
    ingles = set(convenciones.get("palabras_en_ingles", []))
    problemas: list[str] = []
    snake = re.fullmatch(r"[a-z][a-z0-9]*(_[a-z0-9]+)*", nombre)

    if tipo in ("modulo", "funcion", "variable", "paquete", "caso_uso"):
        if not snake:
            problemas.append("debe ir en snake_case: minúsculas y guion bajo (simular_credito)")
    if tipo == "paquete" and "_" in nombre and len(nombre) > 20:
        problemas.append("un paquete debe tener un nombre corto")
    if tipo == "caso_uso" and snake and not re.search(r"(ar|er|ir)$", nombre.split("_")[0]):
        problemas.append("un caso de uso empieza con un verbo en infinitivo (realizar_transferencia, simular_credito)")
    if tipo == "clase" and not re.fullmatch(r"[A-Z][a-z0-9]+([A-Z][a-z0-9]+)*", nombre):
        problemas.append("una clase va en PascalCase (SimulacionCredito)")
    if tipo == "servicio" and not re.fullmatch(r"svc-[a-z]+(-[a-z]+)*", nombre):
        problemas.append("un servicio se llama svc-<dominio> en minúsculas con guiones (svc-creditos)")
    if tipo == "prueba" and not re.fullmatch(r"test_[a-z0-9]+(_[a-z0-9]+)*", nombre):
        problemas.append("una prueba se llama test_<regla>_<caso> en snake_case")
    if tipo == "ruta":
        partes = [p for p in nombre.split("/") if p]
        if not partes or not re.fullmatch(r"v\d+", partes[0]):
            problemas.append("la ruta empieza con la versión: /v1/...")
        recursos = [p for p in partes[1:] if not p.startswith("{")]
        if recursos and not recursos[0].endswith("s"):
            problemas.append("el primer recurso va en plural (/v1/creditos)")
        if any(not re.fullmatch(r"[a-z]+(-[a-z]+)*|\{[a-z_]+\}", p) for p in partes[1:]):
            problemas.append("los segmentos van en minúsculas; los parámetros como {id_cliente}")
    en_ingles = sorted({p for p in _palabras(nombre) if p in ingles})
    if en_ingles:
        problemas.append(f"usa palabras en inglés ({', '.join(en_ingles)}): los nombres van en español")

    if not problemas:
        return f"OK: '{nombre}' cumple las convenciones para {tipo} (politicas.nombres)."
    return f"No cumple: '{nombre}' ({tipo}).\n" + "\n".join(f"  - {p}" for p in problemas) + "\nCorríjalo antes de usarlo."


HERRAMIENTAS: dict[str, tuple[Callable[..., str], str, dict[str, Any]]] = {
    "glosario": (glosario,
                 "Define un término de negocio del Banco Orquídea (por ejemplo GMF, tasa E.A., usura, capacidad de pago). "
                 "Úsela antes de explicar o asumir el significado de un término. Sin término, lista los disponibles.",
                 {"termino": {"type": "string", "description": "Término a definir, por ejemplo 'usura'"}}),
    "consultar_politica": (consultar_politica,
                           "Devuelve la política del banco sobre un tema: datos, seguridad, nombres, logs, apis o pruebas. "
                           "Úsela al especificar o revisar, y cite la política con su clave. Sin tema, lista los temas.",
                           {"tema": {"type": "string", "description": "Tema de la política, por ejemplo 'datos'"}}),
    "catalogo_servicios": (catalogo_servicios,
                           "Busca las APIs internas que el banco ya tiene (clientes, cuentas, créditos, tasas, pagos, "
                           "notificaciones), con sus rutas y la clasificación de cada campo. Úsela antes de proponer un "
                           "servicio nuevo o un origen de datos.",
                           {"busqueda": {"type": "string", "description": "Palabra a buscar, por ejemplo 'tasas' o 'ingresos'"}}),
    "validar_nombre": (validar_nombre,
                       "Revisa que un nombre cumpla las convenciones del banco: español, snake_case, clases en PascalCase, "
                       "casos de uso con verbo en infinitivo, servicios svc-<dominio>, rutas /v1/<plural>. Úsela antes de "
                       "crear un módulo, función, clase, caso de uso, servicio, ruta o prueba.",
                       {"tipo": {"type": "string", "enum": list(TIPOS_NOMBRE), "description": "Qué se está nombrando"},
                        "nombre": {"type": "string", "description": "El nombre propuesto, por ejemplo 'simular_credito'"}}),
}


# --------------------------------------------------------------------------- protocolo MCP (JSON-RPC por stdio)

def describir_herramientas() -> list[dict[str, Any]]:
    return [{"name": nombre, "description": desc,
             "inputSchema": {"type": "object", "properties": props, "additionalProperties": False}}
            for nombre, (_, desc, props) in HERRAMIENTAS.items()]


def atender(mensaje: dict[str, Any]) -> dict[str, Any] | None:
    """Responde un mensaje JSON-RPC. Las notificaciones (sin id) no llevan respuesta."""
    metodo, ident, params = mensaje.get("method"), mensaje.get("id"), mensaje.get("params") or {}
    if ident is None:
        return None

    def ok(resultado: dict[str, Any]) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": ident, "result": resultado}

    if metodo == "initialize":
        pedido = params.get("protocolVersion")
        return ok({"protocolVersion": pedido if pedido in PROTOCOLOS else PROTOCOLOS[0],
                   "capabilities": {"tools": {"listChanged": False}},
                   "serverInfo": {"name": NOMBRE, "version": VERSION},
                   "instructions": "Herramientas del Banco Orquídea (ficticio). Consulte el glosario, las políticas y "
                                   "el catálogo antes de inventar términos, reglas o servicios."})
    if metodo == "ping":
        return ok({})
    if metodo == "tools/list":
        return ok({"tools": describir_herramientas()})
    if metodo == "tools/call":
        nombre, argumentos = params.get("name"), params.get("arguments") or {}
        if nombre not in HERRAMIENTAS:
            return {"jsonrpc": "2.0", "id": ident, "error": {"code": -32602, "message": f"Herramienta desconocida: {nombre}"}}
        funcion = HERRAMIENTAS[nombre][0]
        try:
            texto, error = funcion(**{k: str(v) for k, v in argumentos.items()}), False
        except Exception as exc:  # el agente debe ver el error, no el servidor caerse
            texto, error = f"Error en {nombre}: {exc}", True
        return ok({"content": [{"type": "text", "text": texto}], "isError": error})
    return {"jsonrpc": "2.0", "id": ident, "error": {"code": -32601, "message": f"Método no soportado: {metodo}"}}


def servir() -> None:
    entrada = (linea.decode("utf-8", errors="replace") for linea in sys.stdin.buffer)
    for linea in entrada:
        if not linea.strip():
            continue
        try:
            mensaje = json.loads(linea)
        except json.JSONDecodeError:
            respuesta: dict[str, Any] | None = {"jsonrpc": "2.0", "id": None,
                                                "error": {"code": -32700, "message": "JSON inválido"}}
        else:
            lote = mensaje if isinstance(mensaje, list) else [mensaje]
            respuestas = [r for r in (atender(m) for m in lote) if r is not None]
            respuesta = (respuestas if isinstance(mensaje, list) else respuestas[0]) if respuestas else None
        if respuesta is not None:
            sys.stdout.buffer.write((json.dumps(respuesta, ensure_ascii=False) + "\n").encode("utf-8"))
            sys.stdout.buffer.flush()


def probar() -> int:
    """Llama a cada herramienta como lo haría el agente y muestra el resultado."""
    try:
        cargar_banco()
    except ImportError:
        print("Falta PyYAML. Con el entorno del curso activo: pip install pyyaml")
        return 1
    print(f"Servidor {NOMBRE} {VERSION} · herramientas: {', '.join(HERRAMIENTAS)}\n")
    for nombre, args in [("glosario", {"termino": "usura"}), ("consultar_politica", {"tema": "logs"}),
                         ("catalogo_servicios", {"busqueda": "tasas"}),
                         ("validar_nombre", {"tipo": "caso_uso", "nombre": "calculate_loan"})]:
        respuesta = atender({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": nombre, "arguments": args}})
        print(f"> {nombre}({args})\n{respuesta['result']['content'][0]['text']}\n")
    print("El servidor responde. Si su asistente no lo ve, ejecute: python herramientas/configurar_mcp.py")
    return 0


if __name__ == "__main__":
    sys.exit(probar() if "--probar" in sys.argv else (servir() or 0))
