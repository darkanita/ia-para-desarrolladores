"""Crea el repositorio de la clase: el mismo caso de la docente, para seguirla paso a paso.

Todos quedan con el mismo código, la misma historia de git y el mismo punto de partida de la demo:
el simulador de crédito de consumo de la docente (caso `simulador-credito-consumo`), con el agente del
equipo en la versión del curso, y lo que deja "un compañero" antes de la demo de la sesión.

Uso (desde la carpeta del curso, con el entorno activo):
    python proyectos/nivelar_clase.py ../demo-clase --sesion 6

Después:
    cd ../demo-clase
    python -m pytest -q
    claude
Su reto (mi-reto) no se toca: en clase trabaja aquí, siguiendo a la docente; en casa repite en su reto.
"""
from __future__ import annotations

import argparse
import shutil
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


def git(repo: Path, *args: str, quien: list[str] | None = None) -> str:
    r = subprocess.run(["git", *(quien or []), *args], cwd=repo, capture_output=True, text=True, encoding="utf-8")
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


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("destino", type=Path)
    p.add_argument("--sesion", type=int, default=6, choices=[6])
    a = p.parse_args()
    destino = a.destino.expanduser().resolve()
    if destino.exists() and any(destino.iterdir()):
        print(f"{destino} ya existe y no está vacío. Bórrelo o elija otra carpeta (por ejemplo ../demo-clase-2).")
        return 2

    # 1. El agente del equipo, en la versión del curso (con su historia de versiones)
    r = subprocess.run([sys.executable, str(AQUI / "crear_repositorio.py"), str(destino), "--proyecto", "plantilla-equipo"],
                       capture_output=True, text=True, encoding="utf-8")
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

    print(f"Repositorio de la clase listo en {destino} (sesión {a.sesion}).")
    print(git(destino, "log", "--oneline", "-4"))
    print("\nSiguiente paso:")
    print(f'  cd "{destino}"')
    print("  python -m pytest -q")
    print("  claude")
    return 0


if __name__ == "__main__":
    sys.exit(main())
