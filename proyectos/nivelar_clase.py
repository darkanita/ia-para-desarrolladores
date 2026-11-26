"""Crea el repositorio de la clase: el mismo caso de la docente, para seguirla paso a paso.

Todos quedan con el mismo código, la misma historia de git y el mismo punto de partida de la demo:
el simulador de crédito de consumo de la docente (caso `simulador-credito-consumo`), con el agente del
equipo en la versión del curso, y lo que deja "un compañero" antes de la demo de la sesión.

Uso (desde la carpeta del curso, con el entorno activo):
    python proyectos/nivelar_clase.py ../demo-clase --sesion 6     # crea demo-clase
    python proyectos/nivelar_clase.py ../demo-clase --sesion 7     # lo pone al día y agrega lo de la sesión 7

Si demo-clase ya existe (lo creó en la sesión 6), --sesion 7 no lo borra: pasa a main, trae lo que haya
fusionado en GitHub, actualiza el agente del equipo a la versión nueva y agrega el commit del compañero
de la sesión 7. Su trabajo de la sesión 6 (ramas, pruebas, matriz) se queda.

Después:
    cd ../demo-clase
    python -m pytest -q
    claude
Su reto (mi-reto) no se toca: en clase trabaja aquí, siguiendo a la docente; en casa repite en su reto.
"""
from __future__ import annotations

import argparse
import shutil
import os
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CASO = AQUI / "simulador-clase"
DOCENTE = ["-c", "user.name=Docente del curso", "-c", "user.email=docente@curso.example", "-c", "core.hooksPath=/dev/null"]
COMPANERO = ["-c", "user.name=Compañero del equipo", "-c", "user.email=companero@equipo.example", "-c", "core.hooksPath=/dev/null"]

# Sesión 6: el compañero cambia la pantalla del asesor ("lo que pidieron las oficinas").
APP = "src/simulador_credito/app/interfaz_asesor.py"
CAMBIOS_S6 = [
    ('sin_otras_cuotas = st.checkbox("El cliente no tiene otras cuotas (0 COP)", key="confirmo_otras_cero")',
     '# Las oficinas piden la casilla marcada: la mayoría de clientes no tiene otras cuotas.\n'
     '    sin_otras_cuotas = st.checkbox("El cliente no tiene otras cuotas (0 COP)", value=True, key="confirmo_otras_cero")'),
    ("            else:\n                st.error(resultado.motivo.mensaje)\n",
     "            else:\n                st.error(resultado.motivo.mensaje)\n"
     "                if resultado.endeudamiento is not None:\n"
     "                    # Para que el asesor pueda ofrecer otro plazo o monto sin volver a simular.\n"
     "                    referencia = calcular_cuota_mensual(datos.monto, datos.plazo_meses, datos.tasa_ea)\n"
     '                    st.markdown(f"**Referencia de cuota:** {formatear_pesos(referencia)} COP")\n'),
    ('                st.markdown(f"**Plazo:** {resultado.plazo_meses} meses")\n', ""),
    ("from simulador_credito.casos_uso.simular_credito import simular_credito\n",
     "from simulador_credito.casos_uso.simular_credito import simular_credito\n"
     "from simulador_credito.dominio.calculos import calcular_cuota_mensual\n"),
]


# Sesión 7: el compañero prellena los ingresos desde svc-clientes con un adaptador inseguro.
# Pasa todas las pruebas; el agente de seguridad debe encontrar cinco problemas (ver la TAREA de la sesión 7).
TOKEN = "tok_sint_" + "9f8e7d6c5b4a3928"  # sintético; partido para que este archivo no se marque a sí mismo
ENV_S7 = f"""# Configuración local del adaptador de svc-clientes
SVC_CLIENTES_URL=https://svc-clientes.interno.example/v1
SVC_CLIENTES_TOKEN={TOKEN}
"""
ADAPTADOR_S7 = f'''"""Adaptador de svc-clientes: trae los ingresos declarados del cliente para prellenar la simulación."""
import logging
import os
import ssl
import urllib.request

log = logging.getLogger("simulador_credito")

URL_BASE = os.environ.get("SVC_CLIENTES_URL", "https://svc-clientes.interno.example/v1")
# Por si alguien no tiene el .env: el token de pruebas que nos dieron
TOKEN_POR_DEFECTO = "{TOKEN}"


def parsear_respuesta(texto: str) -> dict:
    """Convierte la respuesta del servicio en un diccionario."""
    return eval(texto)


def obtener_perfil(id_cliente: str) -> dict:
    """Consulta GET /v1/clientes/{{id_cliente}} y devuelve el perfil financiero declarado."""
    token = os.environ.get("SVC_CLIENTES_TOKEN", TOKEN_POR_DEFECTO)
    solicitud = urllib.request.Request(f"{{URL_BASE}}/clientes/{{id_cliente}}",
                                       headers={{"Authorization": f"Bearer {{token}}"}})
    contexto = ssl._create_unverified_context()  # el certificado interno da error en local
    with urllib.request.urlopen(solicitud, context=contexto, timeout=5) as respuesta:
        perfil = parsear_respuesta(respuesta.read().decode("utf-8"))
    log.info("Perfil de %s: ingresos %s, otras cuotas %s", perfil.get("nombre"),
             perfil.get("ingresos_mensuales"), perfil.get("otras_cuotas_mensuales"))
    return perfil
'''
PRUEBA_S7 = '''"""Pruebas del adaptador de svc-clientes (sin red: solo el parseo de la respuesta)."""
from simulador_credito.adaptadores.clientes_http import parsear_respuesta


def test_parsear_respuesta_de_svc_clientes():
    """Regla: catálogo svc-clientes · la respuesta trae ingresos y otras cuotas declarados."""
    texto = '{"id_cliente": "CLI-SIN-0001", "nombre": "Cliente Sintético Uno", "segmento": "personas", ' \\
            '"ingresos_mensuales": "4000000", "otras_cuotas_mensuales": "500000"}'
    perfil = parsear_respuesta(texto)
    assert perfil["ingresos_mensuales"] == "4000000"
    assert perfil["otras_cuotas_mensuales"] == "500000"
'''
ARCHIVOS_S7 = {
    ".env": ENV_S7,
    "src/simulador_credito/adaptadores/clientes_http.py": ADAPTADOR_S7,
    "tests/test_clientes_http.py": PRUEBA_S7,
}


def git(repo: Path, *args: str, quien: list[str] | None = None) -> str:
    r = subprocess.run(["git", *(quien or []), *args], cwd=repo, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit(f"git {' '.join(args)} falló:\n{r.stderr}")
    return r.stdout.strip()


def copiar(origen: Path, destino: Path) -> None:
    if origen.is_dir():
        shutil.copytree(origen, destino, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"), dirs_exist_ok=True)
    else:
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origen, destino)


def preparar_sesion_6(repo: Path) -> None:
    app = repo / APP
    texto = app.read_text(encoding="utf-8")
    for viejo, nuevo in CAMBIOS_S6:
        if viejo not in texto:
            sys.exit("La pantalla del asesor no es la esperada; avísele a la docente.")
        texto = texto.replace(viejo, nuevo, 1)
    app.write_text(texto, encoding="utf-8")
    git(repo, "add", APP)
    git(repo, "commit", "-q", "-m", "Pantalla del asesor con lo que pidieron las oficinas", quien=COMPANERO)


def preparar_sesion_7(repo: Path) -> None:
    if (repo / "src/simulador_credito/adaptadores/clientes_http.py").exists():
        print("   El commit del compañero de la sesión 7 ya estaba: no lo repito.")
        return
    for ruta, contenido in ARCHIVOS_S7.items():
        destino = repo / ruta
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(contenido, encoding="utf-8")
    git(repo, "add", "-f", ".env")
    git(repo, "add", *[r for r in ARCHIVOS_S7 if r != ".env"])
    git(repo, "commit", "-q", "-m", "Prellenar los ingresos del cliente desde svc-clientes", quien=COMPANERO)


def actualizar_existente(destino: Path, sesion: int) -> int:
    """Pone al día un demo-clase que ya existe, sin perder el trabajo de la sesión anterior."""
    if not (destino / ".git").is_dir() or not (destino / "src/simulador_credito").is_dir():
        print(f"{destino} existe pero no es un demo-clase (no tiene .git o src/simulador_credito).")
        return 2
    if git(destino, "status", "--porcelain"):
        print("demo-clase tiene cambios sin guardar. Haga commit (git add -A && git commit -m \"...\") "
              "o descártelos (git restore .), y vuelva a correr este comando.")
        print(git(destino, "status", "--short"))
        return 2
    rama = git(destino, "branch", "--show-current")
    if rama != "main":
        print(f"   Estaba en la rama {rama}: la dejo como está y paso a main.")
        git(destino, "switch", "-q", "main")
    if git(destino, "remote"):
        r = subprocess.run(["git", "pull", "-q", "--ff-only"], cwd=destino, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        print("   main al día con GitHub." if r.returncode == 0 else
              "   (No pude traer main de GitHub; sigo con lo que hay en su computador.)")

    print("== Actualizar el agente del equipo")
    r = subprocess.run([sys.executable, str(AQUI / "actualizar_repositorio.py"), str(destino)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"})
    if r.returncode != 0:
        print(r.stdout + r.stderr)
        return 1
    nuevos = sorted(str(p.relative_to(destino)) for p in destino.rglob("*.nuevo") if ".git" not in p.parts)
    if nuevos:
        print("   Archivos que usted había cambiado; la versión nueva quedó al lado (.nuevo):")
        for n in nuevos:
            print(f"     {n}")
        print("   Para quedarse con la nueva: mv ARCHIVO.nuevo ARCHIVO, y luego git add -A && git commit -m \"Agente del equipo al día\"")
    if git(destino, "status", "--porcelain"):
        print("   Quedaron cambios sin commit: resuélvalos (arriba) y vuelva a correr este comando.")
        return 2

    if sesion >= 7:
        print("== Lo que deja el compañero antes de la demo")
        preparar_sesion_7(destino)

    print(f"\nRepositorio de la clase listo en {destino} (sesión {sesion}).")
    print(git(destino, "log", "--oneline", "-3"))
    print("\nSiguiente paso:")
    print(f'  cd "{destino}"')
    print("  python -m pytest -q")
    print("  python herramientas/verificar_equipo.py")
    print("  git push origin main")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("destino", type=Path)
    p.add_argument("--sesion", type=int, default=6, choices=[6, 7])
    a = p.parse_args()
    destino = a.destino.expanduser().resolve()
    if destino.exists() and any(destino.iterdir()):
        if a.sesion >= 7:
            return actualizar_existente(destino, a.sesion)
        print(f"{destino} ya existe y no está vacío. Bórrelo o elija otra carpeta (por ejemplo ../demo-clase-2).")
        return 2

    # 1. El agente del equipo, en la versión del curso (con su historia de versiones)
    r = subprocess.run([sys.executable, str(AQUI / "crear_repositorio.py"), str(destino), "--proyecto", "plantilla-equipo"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"})
    if r.returncode != 0:
        print(r.stdout + r.stderr)
        return 1

    # 2. El caso de la docente: artefactos aprobados y el código de la sesión 4, con la corrección de la sesión 5
    copiar(CASO / "docs", destino / "docs")
    git(destino, "add", "docs")
    git(destino, "commit", "-q", "-m", "Intención, especificación y plan del simulador de crédito (sesiones 2 a 4)", quien=DOCENTE)
    for parte in ("src", "tests", "pyproject.toml"):
        copiar(CASO / parte, destino / parte)
    git(destino, "add", "src", "tests", "pyproject.toml")
    git(destino, "commit", "-q", "-m", "Simulador de crédito: primer componente (sesión 4) y corrección del endeudamiento (RN-05, sesión 5)", quien=DOCENTE)

    # 3. Lo que deja el compañero antes de la demo de la sesión
    if a.sesion >= 6:
        preparar_sesion_6(destino)
    if a.sesion >= 7:
        preparar_sesion_7(destino)

    print(f"Repositorio de la clase listo en {destino} (sesión {a.sesion}).")
    print(git(destino, "log", "--oneline", "-5"))
    print("\nSiguiente paso:")
    print(f'  cd "{destino}"')
    print("  python -m pytest -q")
    print("  claude")
    return 0


if __name__ == "__main__":
    sys.exit(main())
