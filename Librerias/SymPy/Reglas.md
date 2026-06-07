---
title: Reglas — SymPy
draft: true
tags:
  - sympy
  - reglas
---

# 📐 Reglas de redaccion — SymPy

Convenciones especificas para documentar **SymPy** (matematica simbolica) en el vault.
Especializan el [[Estandarizan Directorio Librerias | estandar base de librerias]]; ante
conflicto, manda el estandar base. El **donde** vive cada nota lo define [[Tree SymPy]].

---

## 1. Naming de archivos (API-style)

| Tipo de nota | Patron | Ejemplo |
|--------------|--------|---------|
| Funcion top-level | `sympy.<funcion>.md` | `sympy.solve.md`, `sympy.integrate.md` |
| Clase / objeto | `<NombreReal>.md` | `Symbol.md`, `Matrix.md`, `Interval.md`, `Poly.md` |
| Metodo de objeto | `<Objeto>.<metodo>.md` | `Matrix.det.md`, `Expr.subs.md` |
| Concepto transversal | `concepto_<tema>.md` | `concepto_expr_arbol.md` |
| Agrupacion de afines | `sympy.<tema>.md` | `sympy.trigonometricas.md` (sin, cos…) |
| **Indice de carpeta** | `index.md` | uno por **cada** directorio |

- **Sin tildes** en nombres de archivo y **tambien en titulo y cuerpo** (solo se conserva la ñ), igual que SciPy/NumPy. El nombre de archivo evita ademas espacios y signos.
- El nombre del archivo = exactamente lo que se wikilinkea (`[[sympy.solve]]`).
- Clases con su **nombre real** de la API, respetando mayusculas (`Matrix`, `FiniteSet`, `Rational`).

---

## 2. Indice por carpeta (`index.md`) — OBLIGATORIO

> [!regla]
> **Cada directorio lleva su `index.md`** como **nota madre de pleno derecho** —tan importante
> como una nota de API—, no un simple listado. Debe **aportar informacion nueva**: que es el
> directorio, el modelo mental y **como se relacionan sus hijos** (cuando usar cada uno).

El `index.md` de una carpeta NO se limita a repetir las descripciones de sus notas. Estructura:

1. `# titulo` y un parrafo que explica **que es** este submodulo/tematica y **su papel** dentro
   de SymPy (el porque, no solo el que).
2. Un **ejemplo de codigo unificador** o la idea clave que hilvana las notas de la carpeta.
3. `## Como se relacionan` (o `## Mapa ...`): una **tabla de decision/comparacion** que diga
   *cuando usar cada hijo* y como se conectan entre si (p.ej. `solve` vs `solveset`, funcion vs
   clase-sin-evaluar). Esta es la informacion nueva que justifica el index.
4. `## Subtemas` / `## Notas`: la lista de hijos, pero anotando **su relacion**, no solo su
   descripcion. Subcarpetas con ruta `[[sympy.core/simbolos/index | …]]`; notas hoja por basename
   `[[sympy.symbols | …]]`. Marca *(pendiente)* solo las notas aun no escritas.
5. `## Notas relacionadas` (padre, Tree, conceptos afines).

Frontmatter de un `index.md`:

```yaml
---
title: <ruta corta> — <descripcion breve>
tags:
  - sympy
  - indice
draft: true
---
```

> `index.md` es un **hub de navegacion**, no una nota de API: no lleva `lib/tipo/retorna`,
> y `sync_tree.py` lo ignora en su conteo de cobertura.

---

## 3. Frontmatter de una nota de API

```yaml
---
title: sympy.solve — resolver ecuaciones y sistemas
aliases:
  - solve
  - resolver ecuaciones
tags:
  - sympy
  - api/funcion          # api/funcion | api/clase | api/metodo | api/objeto
  - solvers/algebraicas  # dominio funcional = rama del Tree
# --- Clasificacion ---
lib: sympy
mod: sympy.solvers       # submodulo (o sympy para top-level)
tipo: funcion
# --- Comportamiento ---
retorna: list | dict | FiniteSet
# --- Dependencias ---
requiere:
  - Symbol
  - sympy.Eq
draft: false
---
```

- `tipo`: `funcion | clase | metodo | objeto | concepto`.
- `retorna`: el tipo simbolico de salida (`Expr`, `list`, `dict`, `FiniteSet`, `Matrix`…).
- Maximo **3–5 tags**; nunca `python`, `simbolico` ni el path repetido (regla del estandar base).

---

## 4. Estructura de una nota de API (orden de capas)

Mismo molde que las notas de SciPy (lo mas consultado arriba):

1. `# title` y un parrafo de **que hace y cuando usarla**.
2. **Firma** en bloque de codigo (`sympy.solve(f, *symbols, dict=False, ...)`).
3. **Valor de retorno** (tabla tipo/forma/significado).
4. **Formas basicas de llamada** (tabla objetivo → llamada).
5. **Parametros en detalle** con ejemplos ejecutables (salida en comentarios).
6. **Casos de uso** reales de ingenieria/matematica.
7. **Errores comunes** (tabla error → causa → solucion) y **Limitaciones**.
8. `## Notas relacionadas` con los wikilinks.

> [!ejemplo]
> Todo codigo debe ser **ejecutable** y mostrar la salida exacta como comentario:
> ```python
> from sympy import symbols, solve
> x = symbols("x")
> solve(x**2 - 4, x)        # [-2, 2]
> ```

---

## 5. Notacion y criterio SymPy

> [!info] Exactitud simbolica
> SymPy es **exacto**, no flotante: `Rational(1, 3)` ≠ `0.333…`. Distinguir siempre el mundo
> simbolico del numerico. El puente a NumPy/SciPy es `lambdify`; `evalf()` da precision arbitraria.

- Crear simbolos siempre con `symbols(...)` y nombrar los **supuestos** relevantes
  (`symbols("x", real=True, positive=True)`) cuando cambien el resultado.
- Preferir y señalar **`solveset`** como alternativa moderna a `solve` donde aplique.
- Construir ecuaciones con `Eq(lhs, rhs)`; recordar que una `Expr` suelta se asume `= 0`.
- Mostrar la **auto-simplificacion** cuando sorprenda (`x + x → 2*x` sin pedirlo).
- En notas con salida "bonita", mencionar `pprint` / `init_printing` / `latex` para el render.

---

## 6. Wikilinks (resumen del estandar base)

- 1–2 apariciones por nota, en la **primera mencion significativa**; en parrafos, no en tablas.
- ❌ Nunca en headers, codigo, frontmatter ni titulos.
- A nota hoja: por basename `[[sympy.diff]]`. A `index` de carpeta: con ruta
  `[[sympy.calculus/derivadas/index | derivadas]]` (el basename `index` colisiona).
- Seccion final **obligatoria** `## Notas relacionadas`.
- Enlaces a notas de NumPy/SciPy (otra rama) son validos como referencia.

---

## 7. Flujo de trabajo

1. Diseñar/actualizar [[Tree SymPy]] (roadmap).
2. `conceptos_transversales/` + `introduccion.md` a mano (modelo mental).
3. Rellenar submodulos con subagentes (`nota-libreria`) + revision.
4. Mantener cada `index.md` al dia con su contenido.
5. `python3 .claude/skills/tree-libreria/sync_tree.py Librerias/SymPy` → marcar ✅ en el Tree.

---

## Notas relacionadas

- [[Tree SymPy]]
- [[Estandarizan Directorio Librerias]]
