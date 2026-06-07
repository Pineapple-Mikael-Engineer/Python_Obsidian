---
title: Reglas — SymPy
draft: true
tags:
  - sympy
  - reglas
---

# 📐 Reglas de redacción — SymPy

Convenciones específicas para documentar **SymPy** (matemática simbólica) en el vault.
Especializan el [[Estandarizan Directorio Librerias | estándar base de librerías]]; ante
conflicto, manda el estándar base. El **dónde** vive cada nota lo define [[Tree SymPy]].

---

## 1. Naming de archivos (API-style)

| Tipo de nota | Patrón | Ejemplo |
|--------------|--------|---------|
| Función top-level | `sympy.<funcion>.md` | `sympy.solve.md`, `sympy.integrate.md` |
| Clase / objeto | `<NombreReal>.md` | `Symbol.md`, `Matrix.md`, `Interval.md`, `Poly.md` |
| Método de objeto | `<Objeto>.<metodo>.md` | `Matrix.det.md`, `Expr.subs.md` |
| Concepto transversal | `concepto_<tema>.md` | `concepto_expr_arbol.md` |
| Agrupación de afines | `sympy.<tema>.md` | `sympy.trigonometricas.md` (sin, cos…) |
| **Índice de carpeta** | `index.md` | uno por **cada** directorio |

- **Sin tildes ni signos** en nombres de archivo (`sympy.factorint.md`, no con tilde). El título sí lleva tildes.
- El nombre del archivo = exactamente lo que se wikilinkea (`[[sympy.solve]]`).
- Clases con su **nombre real** de la API, respetando mayúsculas (`Matrix`, `FiniteSet`, `Rational`).

---

## 2. Índice por carpeta (`index.md`) — OBLIGATORIO

> [!regla]
> **Cada directorio lleva su `index.md`** como nota madre. Es lo que faltó en las otras
> librerías; aquí no se omite.

El `index.md` de una carpeta:
- Presenta en 1–2 frases qué cubre el submódulo/temática.
- Lista su **contenido**: subcarpetas (enlazadas con ruta `[[sympy.core/simbolos/index | …]]`)
  y notas hoja (enlazadas por basename `[[sympy.symbols | …]]`).
- Marca como *(pendiente)* las notas aún no redactadas.
- Cierra con `## Notas relacionadas`.

Frontmatter de un `index.md`:

```yaml
---
title: <ruta corta> — <descripción breve>
tags:
  - sympy
  - indice
draft: true
---
```

> `index.md` es un **hub de navegación**, no una nota de API: no lleva `lib/tipo/retorna`,
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
# --- Clasificación ---
lib: sympy
mod: sympy.solvers       # submódulo (o sympy para top-level)
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
- `retorna`: el tipo simbólico de salida (`Expr`, `list`, `dict`, `FiniteSet`, `Matrix`…).
- Máximo **3–5 tags**; nunca `python`, `simbolico` ni el path repetido (regla del estándar base).

---

## 4. Estructura de una nota de API (orden de capas)

Mismo molde que las notas de SciPy (lo más consultado arriba):

1. `# title` y un párrafo de **qué hace y cuándo usarla**.
2. **Firma** en bloque de código (`sympy.solve(f, *symbols, dict=False, ...)`).
3. **Valor de retorno** (tabla tipo/forma/significado).
4. **Formas básicas de llamada** (tabla objetivo → llamada).
5. **Parámetros en detalle** con ejemplos ejecutables (salida en comentarios).
6. **Casos de uso** reales de ingeniería/matemática.
7. **Errores comunes** (tabla error → causa → solución) y **Limitaciones**.
8. `## Notas relacionadas` con los wikilinks.

> [!ejemplo]
> Todo código debe ser **ejecutable** y mostrar la salida exacta como comentario:
> ```python
> from sympy import symbols, solve
> x = symbols("x")
> solve(x**2 - 4, x)        # [-2, 2]
> ```

---

## 5. Notación y criterio SymPy

> [!info] Exactitud simbólica
> SymPy es **exacto**, no flotante: `Rational(1, 3)` ≠ `0.333…`. Distinguir siempre el mundo
> simbólico del numérico. El puente a NumPy/SciPy es `lambdify`; `evalf()` da precisión arbitraria.

- Crear símbolos siempre con `symbols(...)` y nombrar los **supuestos** relevantes
  (`symbols("x", real=True, positive=True)`) cuando cambien el resultado.
- Preferir y señalar **`solveset`** como alternativa moderna a `solve` donde aplique.
- Construir ecuaciones con `Eq(lhs, rhs)`; recordar que una `Expr` suelta se asume `= 0`.
- Mostrar la **auto-simplificación** cuando sorprenda (`x + x → 2*x` sin pedirlo).
- En notas con salida "bonita", mencionar `pprint` / `init_printing` / `latex` para el render.

---

## 6. Wikilinks (resumen del estándar base)

- 1–2 apariciones por nota, en la **primera mención significativa**; en párrafos, no en tablas.
- ❌ Nunca en headers, código, frontmatter ni títulos.
- A nota hoja: por basename `[[sympy.diff]]`. A `index` de carpeta: con ruta
  `[[sympy.calculus/derivadas/index | derivadas]]` (el basename `index` colisiona).
- Sección final **obligatoria** `## Notas relacionadas`.
- Enlaces a notas de NumPy/SciPy (otra rama) son válidos como referencia.

---

## 7. Flujo de trabajo

1. Diseñar/actualizar [[Tree SymPy]] (roadmap).
2. `conceptos_transversales/` + `introduccion.md` a mano (modelo mental).
3. Rellenar submódulos con subagentes (`nota-libreria`) + revisión.
4. Mantener cada `index.md` al día con su contenido.
5. `python3 .claude/skills/tree-libreria/sync_tree.py Librerias/SymPy` → marcar ✅ en el Tree.

---

## Notas relacionadas

- [[Tree SymPy]]
- [[Estandarizan Directorio Librerias]]
