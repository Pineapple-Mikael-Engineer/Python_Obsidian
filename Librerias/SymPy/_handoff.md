---
title: _handoff — continuar la documentacion de SymPy
draft: true
tags:
  - sympy
  - meta
---

# Continuar documentacion de la libreria SymPy (vault Obsidian)

Eres un asistente que continua un proyecto de documentacion de la libreria **SymPy** en un
vault de Obsidian. Trabaja en español. IMPORTANTE: lee primero los archivos que se indican
antes de escribir nada.

## Contexto y repo

- Repo: `/home/mikael/Documentos/Proyectos_Personales/Obdisian_General/Python_Obsidian`
- Rama de trabajo: `feat/Librerias/SymPy` (ya existe; haz `git checkout feat/Librerias/SymPy`).
- branch-guard: antes de cualquier `git commit`, asegura el marcador:
  `printf 'feat/Librerias/SymPy' > .claude/expected-branch` (es gitignored).
- NO commitees nunca `Python Basicos.md`, `Python POO.md` ni `.smart-env/` (untracked a proposito).
- El arbol/plan de notas vive en `Librerias/SymPy/Tree SymPy.md` (FUENTE DE VERDAD del roadmap).
- Las convenciones especificas estan en `Librerias/SymPy/Reglas.md` — LEELO COMPLETO.

## Objetivo

Rellenar las notas pendientes del `Tree SymPy.md`, **un directorio (submodulo) a la vez**,
siguiendo el orden de prioridad de la tabla "Estado actual" del Tree. Estado al iniciar:
**53 / ~99 notas**. Completos: conceptos_transversales, sympy.core, sympy.calculus,
sympy.solvers, sympy.polys, sympy.simplify.
**Siguiente directorio: `sympy.matrices/`** (11 notas). Luego: sympy.functions, sympy.sets,
sympy.assumptions, sympy.printing, sympy.logic, sympy.ntheory, y opcionales
(geometry, stats, physics.units), mas `introduccion.md` (raiz).

## Convenciones OBLIGATORIAS (lee Reglas.md; esto es el resumen)

1. **SIN TILDES** en TODO el texto (titulos y cuerpo de toda nota e index); solo se conserva la
   ñ. NUNCA uses á/é/í/ó/ú. Es la convencion de las librerias (SciPy/NumPy/Matplotlib).
2. **Naming de archivo** API-style, sin tildes/espacios: funciones `sympy.<func>.md`; clases con
   su nombre real `Matrix.md`, `Interval.md`; metodos `Objeto.metodo.md` (`Matrix.det.md`);
   conceptos `concepto_<tema>.md`.
3. **Frontmatter de nota de API**:

   ```yaml
   ---
   title: <nombre> — <descripcion breve sin tildes>
   aliases: [<2-3 alias>]
   tags: [sympy, api/<funcion|clase|metodo|objeto>, <submodulo>/<tematica>]
   lib: sympy
   tipo: funcion|clase|metodo|concepto
   obj: <Clase>        # solo si es metodo/atributo
   retorna: <tipo>
   requiere: [...]
   draft: false
   ---
   ```

4. **Estructura de nota** (lo mas consultado arriba; incluye solo lo que aporte): `# titulo`,
   parrafo que/cuando, `## Firma`, `## Valor de retorno` (tabla), `## Formas basicas de llamada`,
   `## Parametros en detalle`, `## Casos de uso`, `## Errores comunes` (tabla
   error/causa/solucion), `## Notas relacionadas`. Las clases: constructor, atributos/metodos
   (tabla), `.doit()` si aplica, ejemplo, relacionadas.
5. **Codigo Python ejecutable** y con la salida exacta en comentario (p.ej. `# 2*sqrt(2)`).
   VERIFICA ejecutando SymPy antes de afirmar una salida.
6. **index.md = NOTA MADRE RICA** (Reglas §2), NO un listado. Cada index debe APORTAR: que es el
   directorio, modelo mental, ejemplo unificador, una seccion `## Como se relacionan` con tabla
   de decision (cuando usar cada hijo) y la lista de hijos anotando su relacion. Frontmatter del
   index: `title`, `tags: [sympy, indice]`, **`draft: false`**.
7. **Wikilinks**: a nota hoja por basename `[[sympy.diff]]`; a un index de carpeta SIEMPRE con
   ruta `[[sympy.matrices/creacion/index | creacion]]`, y a la raiz `[[SymPy/index | SymPy]]`
   (el basename `index` colisiona: nunca uses `[[index]]` solo); en TABLAS escapa el pipe `\|`;
   NUNCA wikilinks en headers, codigo, frontmatter ni titulos. Cierra cada nota con
   `## Notas relacionadas`.
8. **No enlaces fuera del roadmap**: solo wikilinkea notas que existan o esten en `Tree SymPy.md`.
   Para objetos NO documentados (`Eq`, `Function`, etc.) usa formato de codigo, NO wikilink.
   Cross-refs a notas de SciPy/NumPy (otra rama) SI son validos como referencia.

## Flujo por directorio (repite para cada submodulo)

1. Mira en `Tree SymPy.md` la estructura del submodulo (subcarpetas y notas). Las carpetas e
   `index.md` ya existen (stubs).
2. **Lanza subagentes en paralelo, uno por subcarpeta**, cada uno con: (a) que lea
   `Librerias/SymPy/Reglas.md`, un modelo de nota SciPy via
   `git show main:"Librerias/SciPy/scipy.integrate/cuadratura/scipy.integrate.quad.md"` (funcion)
   o `git show main:"Librerias/SciPy/scipy.interpolate/CubicSpline.md"` (clase), un modelo de
   nota en-repo ya escrita, y un modelo de INDEX RICO en-repo
   (`Librerias/SymPy/sympy.solvers/algebraicas/index.md`); (b) que escriba SUS notas hoja y
   **reescriba su `index.md` de subcarpeta como nota madre rica** (draft:false); (c) que NO
   toque nada fuera de su subcarpeta. Recuerdale en MAYUSCULAS el SIN TILDES.
   - Si el submodulo tiene una clase/nota en su raiz (p.ej. `Matrix.md` en `sympy.matrices/`),
     encargala a un subagente dedicado o escribela tu.
3. **El `index.md` de seccion** (el del submodulo) escribelo TU a mano tras leer las notas hijas:
   nota madre rica con tabla "Como se relacionan" entre las subcarpetas (draft:false).
4. **Verifica** (scripts abajo): conteo de hojas, 0 tildes, frontmatter completo, 0 enlaces
   fuera de roadmap, indices draft:false. Arregla lo que aparezca (desenlaza off-roadmap a codigo).
5. **Actualiza `Tree SymPy.md`**: añade `✅ ` delante de cada nota nueva en el bloque de arbol;
   pon el submodulo como `✅ N/N completo` en la tabla de estado; actualiza el contador
   "Roadmap: X / ~99" y el Total.
6. **Commit** en la rama (no hace falta push salvo que el usuario lo pida):
   `git add "Librerias/SymPy"` + commit `feat(sympy): redactar <submodulo> (N notas) + index ricos`.

## Scripts de verificacion (ajusta C a la carpeta del submodulo)

```bash
C="Librerias/SymPy/sympy.matrices"
# 1) tildes prohibidas (debe ser 0)
grep -rlnE '[áéíóúÁÉÍÓÚüÜ]' "$C"/**/*.md 2>/dev/null | grep -v index.md || echo "0 ok"
# 2) frontmatter + enlaces fuera de roadmap: script python que cruce los [[links]] contra los
#    basenames en disco y los planificados en "Tree SymPy.md" (ver patrones en commits previos).
# 3) sync_tree (lo importante es "0 hojas con ✅ sin archivo"; ignora el ruido de index.md/Reglas.md):
python3 .claude/skills/tree-libreria/sync_tree.py "Librerias/SymPy"
```

## Notas finales

- `sync_tree.py` cuenta los `index.md` y `Reglas.md` como "en disco pero no en Tree": es RUIDO
  conocido e inofensivo (no hay permiso para parchear el script). Lo que importa es que NO haya
  hojas con ✅ en el Tree sin archivo en disco.
- Trabaja directorio a directorio y reporta al usuario al terminar cada uno (que escribiste,
  verificacion, nuevo estado X/99) antes de seguir con el siguiente.
- Para `sympy.matrices/`: subcarpetas `creacion/` (eye, zeros, ones, diag) y `operaciones/`
  (Matrix.det, Matrix.inv, Matrix.rref, Matrix.eigenvals, Matrix.eigenvects, Matrix.nullspace),
  mas la clase `Matrix.md` en la raiz del submodulo. Modelo de clase util ya escrito:
  `Librerias/SymPy/sympy.polys/Poly.md`.

Empieza por `sympy.matrices/`. Si algo de las convenciones no esta claro, lee `Reglas.md` y una
nota ya escrita (p.ej. `sympy.solvers/algebraicas/sympy.solve.md`) antes de preguntar.
