# Sesión 6 · Trabajo autónomo (antes de la clase)

La sesión 6 se mueve un día. Usen ese tiempo para llegar a clase con el mismo caso de la docente y con el trabajo de "ojo humano" ya hecho. En clase lo repetimos con el agente **Verificador** y comparamos: ¿encontró lo mismo que ustedes?, ¿más?, ¿menos?

**Tiempo:** 65 a 80 minutos. **Individual.** **No** abran todavía el agente Verificador ni corran `/pruebas`: eso lo hacemos juntos.

Todo en **Git Bash**, desde la carpeta del curso y con el entorno activo (`source .venv/Scripts/activate`).

---

## 1. Material y herramientas · 5 min

1. Traiga el material nuevo: descargue el `.zip` nuevo y descomprímalo **sobre** la carpeta del curso (o `git pull`).
2. Instale la cobertura:

   ```bash
   pip install -U "pytest-cov>=5" "coverage>=7.5"
   ```

   Si después `pytest` falla con `KeyError: 'BREAK_LOOP'` o menciona `cov_core`, quedó una versión vieja: `pip uninstall -y cov-core pytest-cov coverage` y vuelva a correr el comando de arriba.

## 2. El mismo caso de la docente · 10 min

El script crea una carpeta nueva, `demo-clase`, al lado de `mi-reto`, con el simulador de la docente ya listo (con `git` y su historia). Su `mi-reto` no se toca. Desde aquí trabajamos con **dos repositorios**: `demo-clase` para seguir a la docente en clase y `mi-reto` para repetirlo con su reto.

```bash
python proyectos/nivelar_clase.py ../demo-clase --sesion 6
cd ../demo-clase
python -m pytest -q                       # 47 passed
python herramientas/verificar_capas.py    # Regla de capas: OK
git log --oneline -4
```

En `git log` deben ver cuatro commits. El último es **"Pantalla del asesor con lo que pidieron las oficinas"**, de un *Compañero del equipo*. Todas las pruebas pasan. La pregunta de la sesión es: **¿lo que pide la especificación sigue probado?**

> Si `nivelar_clase.py` dice que `../demo-clase` ya existe, bórrelo (`rm -rf ../demo-clase`) y vuelva a correrlo.

### Súbalo a GitHub · 5 min

1. En GitHub: **New repository**, nombre `demo-clase`, **Private**, y **sin** README, `.gitignore` ni licencia (debe quedar vacío).
2. En la terminal, dentro de `demo-clase` (cambie `<su-usuario>`):

   ```bash
   git remote add origin https://github.com/<su-usuario>/demo-clase.git
   git push -u origin main
   ```

3. Recargue la página del repositorio: deben verse los cuatro commits y la carpeta `src/`.

## 3. Leer la especificación · 15 min

Abra `docs/sdlc/simulador-credito-consumo/spec.md` en VS Code y lea:

- **Sección 4:** RF-01 a RF-06, cada uno con sus criterios *Dado… cuando… entonces…*
- **Sección 5:** las reglas RN-01 a RN-07.
- **Sección 9:** los casos borde.

Fíjese en qué criterios hablan de **lo que ve el asesor** en la pantalla (*"cuando el asesor ve el resultado…"*) y cuáles hablan solo del cálculo.

## 4. La matriz a mano · 20 min

Cree el archivo `docs/sdlc/simulador-credito-consumo/matriz-a-mano.md` y llene una fila por criterio:

```markdown
| Criterio de la spec | Prueba que lo verifica (archivo::función) | Estado |
|---|---|---|
| RF-01 · cuota de 10.000.000 a 36 meses = 388.846 COP | tests/test_calculos.py::... | cubierto |
| RF-02 · ... | | |
```

Use tres estados:

- **cubierto:** hay una prueba que verifica exactamente eso;
- **parcial:** se prueba en el cálculo (`tests/test_simular_credito.py`), pero el criterio habla de la pantalla y la pantalla no se prueba;
- **sin prueba:** no hay ninguna.

Para encontrar las pruebas rápido, cada una dice qué regla verifica en su docstring:

```bash
grep -rn "Regla:" tests
```

## 5. Cobertura · 5 min

```bash
python -m pytest -q --cov=src/simulador_credito/dominio --cov-report=term-missing
```

Anote el porcentaje del dominio. Pregunta para traer a clase: **con 47 pruebas en verde y esa cobertura, ¿está probado lo que ve el asesor?**

## 6. Usar la pantalla como el asesor · 15 min

```bash
python -m streamlit run src/simulador_credito/app/interfaz_asesor.py
```

Se abre en el navegador. Simule estos tres casos, que salen de la spec, y compare lo que **ve** con lo que la spec dice que debería ver:

| Caso | Monto | Plazo | Tasa | Ingresos | Otras cuotas | Qué dice la spec |
|---|---|---|---|---|---|---|
| A · válida | 10000000 | 36 | 26 | 4000000 | 500000 | RF-01 y RF-02 |
| B · rechazada | 10000000 | 36 | 26 | 1500000 | 400000 | RF-03, RF-04 y RF-06 |
| C · otras cuotas vacías | 10000000 | 36 | 26 | 4000000 | *(vacío)* | Sección 9 |

En el caso C, mire también la casilla "El cliente no tiene otras cuotas". Cierre con `Ctrl + C` en la terminal.

Agregue al final de `matriz-a-mano.md` una sección **"Lo que la pantalla hace distinto de la spec"**, con una línea por diferencia y el criterio que incumple.

> **No corrija nada en `src/`.** Si encuentra una diferencia, es un *posible defecto*: se reporta, no se arregla. En clase vemos cómo lo deja escrito el Verificador.

## 7. Guardar · 2 min

```bash
git switch -c pruebas/simulador-credito-consumo-verificacion
git add docs
git commit -m "Matriz a mano de la especificación del simulador (sesión 6)"
git push -u origin pruebas/simulador-credito-consumo-verificacion
```

No abra todavía el pull request: en clase le agregamos las pruebas del Verificador y lo abrimos juntos.

---

## Para traer a la sesión

- [ ] `demo-clase` con 47 pruebas en verde y subido a GitHub (`main` y la rama `pruebas/...`).
- [ ] `matriz-a-mano.md` con la matriz y las diferencias que encontró en la pantalla.
- [ ] El porcentaje de cobertura del dominio.
- [ ] Su pull request de la sesión 5 en `mi-reto`, fusionado o con los hallazgos que le quedaron.

**Si algo no le funciona**, escriba en el grupo con el comando y el mensaje de error completo (copiado, no foto).
