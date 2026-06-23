---
title: Estandar Numpy
draft: true
---

# Estándar de Notas — NumPy

> **v2 (refactor).** Sube la vara: las notas dejan de describir firmas "a lo obvio" y pasan a
> explicar **cada parámetro**, el **comportamiento del eje en N-D**, la **vectorización**, el
> **retorno desambiguado** y la **matemática** de la operación. NumPy es un sistema matemático
> sobre tensores; las notas deben reflejarlo.

## 🎯 Objetivo

Documentar NumPy como lo que es: un **lenguaje de transformaciones sobre tensores** (`ndarray`).
Cada nota debe servir para **releer y entender de verdad** una función, no solo recordar su nombre.
El lector ya sabe que existe `np.sum`; viene a la nota a entender *cómo se comporta su `axis` en 3D*,
*qué retorna exactamente* y *por qué es más rápido que un bucle*.

## 🧠 Filosofía base

- **Conceptos → gobiernan** (`broadcasting`, `vectorizacion`, `axis`, `dtype`, `views_vs_copias`).
- **Funciones → implementan** transformaciones sobre tensores.
- **ndarray → estructura base.**
- La librería es **matemática**: usa notación `$...$` / `$$...$$` siempre que aclare.

---

## 📁 Tipos de notas y naming

| Tipo | Ubicación | Archivo |
|---|---|---|
| Concepto | `conceptos_transversales/` | `concepto_<tema>.md` |
| Función | `np/<tematica>/` | `np.<funcion>.md` |
| Método | `np.ndarray/metodos/<sub>/` | `ndarray.<metodo>.md` |
| Atributo | `np.ndarray/atributos/` | `ndarray.<attr>.md` |
| Submódulo | `np.<submodulo>/<tematica>/` | `np.<submodulo>.<func>.md` |
| Índice de carpeta | cada directorio | `index.md` |

Naming API-style con el nombre real (`np.sum.md`, `ndarray.reshape.md`). El archivo = lo que se
wikilinkea.

> [!important] Idioma: NumPy SÍ usa tildes
> A diferencia de SciPy/SymPy/VisPy/PyQt6, NumPy se redacta con **ortografía española normal
> (con tildes)**, como Matplotlib. El código va tal cual.

---

## 🧠 Frontmatter (se conserva el esquema)

```yaml
---
title: np.sum — suma (reduce) los elementos a lo largo de un eje
aliases: [sum, np.sum, suma]
tags: [numpy, api/funcion, reducciones]
lib: numpy
mod: np                      # np | np.linalg | np.random | np.ndarray ...
tipo: funcion                # funcion | metodo | atributo | clase | submodulo | concepto
retorna: ndarray | escalar   # ser preciso; la ambigüedad se resuelve en el cuerpo
inplace: false
requiere:                    # conceptos necesarios para entenderla
  - concepto_axis_parametro
  - concepto_vectorizacion
draft: false
---
```

- Máximo **3–5 tags** (`numpy` + `api/<tipo>` + `<dominio>`); nunca `python`, `datos`, ni el path.
- `retorna`: si es ambiguo (escalar **o** ndarray), decláralo así y **desambígualo en el cuerpo**.

---

## 🧩 Estructura del cuerpo — el LISTÓN (nota de función)

El orden es fijo; la **profundidad se adapta** a la función, pero las secciones marcadas con ⭐ son
**obligatorias siempre que apliquen** (son justo lo que faltaba en la v1).

1. **`# título` + párrafo** — qué hace, cuándo se usa y la **idea en una frase** (incluida la
   intuición matemática: "reduce un eje", "contrae una dimensión compartida").

2. ⭐ **`## La idea en una fórmula`** — TRES piezas (las que apliquen). El objetivo es que se vea
   **cómo la entrada se convierte en la salida**, no solo "qué hace":

   **(a) El mapa de shapes** — la relación general entrada → salida en notación $(n_0,\dots,n_k)$,
   como una transformación explícita de la forma. Es la pieza más importante y la que faltaba:
   $$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{sum, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

   **(b) La fórmula por índices** — cómo se calcula cada elemento de la salida a partir de los de la
   entrada (el sumatorio / la contracción), enmarcada sobre los ejes del tensor:
   - elemento a elemento: $z_i = x_i + y_i$
   - reducción de un eje: $s_j = \sum_{i} a_{ij}$
   - contracción: $C_{ij} = \sum_k A_{ik} B_{kj}$

   **(c) Visual con matrices / arrays pequeños** cuando aclare: un `(2,3)` concreto antes → después,
   o un esquema de qué eje se contrae. Imprescindible en funciones N-D no obvias.

   > [!example] Por qué el mapa de shapes es obligatorio (caso `np.inner`)
   > Para `np.inner(a, b)` con `a.shape = (n_0,…,n_{p-1}, t)` y `b.shape = (m_0,…,m_{q-1}, t)` (último
   > eje común de tamaño $t$), la forma de salida es la concatenación de los ejes que sobreviven:
   > $$ (n_0,\dots,n_{p-1},\,t),\ (m_0,\dots,m_{q-1},\,t)\ \longrightarrow\ (n_0,\dots,n_{p-1},\,m_0,\dots,m_{q-1}) $$
   > $$ C_{\,i_0\dots i_{p-1},\ j_0\dots j_{q-1}} \;=\; \sum_{t} a_{\,i_0\dots i_{p-1}\,t}\; b_{\,j_0\dots j_{q-1}\,t} $$
   > Sin este mapa, "`np.inner` de dos arrays N-D" es impredecible; con él, es mecánico. **Toda nota
   > de una función que cambie el shape debe incluir su mapa de shapes así.**

   Si la función no es matemática (p. ej. `reshape`), el mapa de shapes **es** el corazón de la nota.

3. **`## Firma`** — completa, con tipos y valores por defecto en un bloque ```python.

4. ⭐ **`## Los parámetros en detalle`** — **TODOS** los parámetros, incluidos los "aburridos"
   (`out`, `where`, `dtype`, `casting`, `order`, `initial`, `keepdims`...). Por cada uno: qué hace,
   **valores válidos**, **cuándo importa de verdad** y un mini-ejemplo. Nada de "array de entrada"
   a secas. Si un parámetro tiene trampa (overflow del acumulador, `casting` estricto), dilo aquí.

5. ⭐ **`## El eje y el caso N-D`** (cuando hay `axis` o el resultado depende de la dimensión) —
   el comportamiento explicado en **1D, 2D y N-D**: qué eje se **colapsa/contrae**, cómo queda el
   shape, qué hace `keepdims`, y un ejemplo con un tensor `(d0, d1, d2)`. Esta sección es la que
   convierte la nota en útil para casos reales.

6. ⭐ **`## Vectorización`** — el **modelo vectorizado frente al bucle Python equivalente** (mostrar
   ambos), qué hace NumPy por debajo (ufunc/BLAS/broadcasting) y por qué importa. Enlaza
   [[concepto_vectorizacion]]. No hace falta benchmark, sí el contraste conceptual.

7. ⭐ **`## Valor de retorno`** — tabla **desambiguada**: `entrada (shape, dtype)` + parámetros →
   **shape y dtype EXACTOS de salida**, y **cuándo escalar vs ndarray vs 0-d**. Incluir las reglas
   de promoción de `dtype` cuando apliquen. Cero "devuelve un ndarray" sin más.

8. ⭐ **`## Casos de uso`** — **abundantes** y progresivos, no 1–2 de relleno. Para cualquier función
   no trivial, **al menos un ejemplo trabajado en N-D (3D+)** que muestre los **arrays y la salida
   concretos** (los valores, no solo el `.shape`). La regla: si el comportamiento en dimensiones
   altas no es obvio, hay que **verlo** con un ejemplo ejecutado, no solo describirlo. Cubrir también
   broadcasting y los casos límite. (En funciones triviales como `np.sum`/`np.zeros` basta con pocos.)

9. **`## Errores comunes`** — tabla `| Error | Causa | Solución |`.

10. **`## Notas relacionadas`** — wikilinks (conceptos que gobiernan + funciones hermanas).

> [!regla] Las 5 secciones ⭐ son la diferencia con la v1
> La fórmula, los parámetros completos, el eje/N-D, la vectorización y el retorno desambiguado son
> exactamente lo que hacía inútiles a las notas viejas. Si una nota no las necesita (una creación
> trivial como `np.zeros`), se omiten **conscientemente**, no por pereza.

---

## 🧩 Estructura de una nota de CONCEPTO

Los conceptos son el **modelo mental**; no llevan firma/parámetros. Estructura:

1. `# título` + **Definición fundamental** — 1–2 frases potentes de qué es.
2. `## Por qué existe` — la motivación (sin X tedioso vs con X directo).
3. `## La regla / el modelo central` — la regla mínima a memorizar, con **`$$` / tablas** cuando
   aplique: el **mapa de shapes** de `axis`, las reglas de alineación de `broadcasting`, la
   promoción de `dtype`, los strides de `ndarray`...
4. `## Ejemplos progresivos` — Nivel 1/2/3, **incluyendo N-D con valores concretos**.
5. `## Casos que fallan` — los errores típicos con su porqué.
6. `## Relación con otros conceptos` — wikilinks.

Misma vara matemática que las funciones: el concepto que gobierna el mapa de shapes (`axis`,
`shape`, `broadcasting`, `indexing`) debe **mostrar la transformación de forma** con notación
general $(n_0,\dots,n_k)$, no solo describirla en prosa.

---

## 🧠 Conectar tensor ↔ operación (transversal)

Siempre que se pueda, enmarca la función como una operación sobre los **ejes** de un tensor:
- `axis` = el **modo/eje** del tensor sobre el que se opera.
- una reducción **elimina** un eje; `keepdims` lo deja en tamaño 1.
- un producto/contracción **suma sobre un eje compartido** y lo elimina.
- broadcasting = **alinear ejes** por la derecha. Ver [[concepto_broadcasting]] y [[concepto_shape]].

---

## 🔗 Wikilinks (igual que el estándar base)

- 1–2 por nota, en la primera mención relevante, en prosa (no en tablas/headers/código/frontmatter).
- A concepto por basename (`[[concepto_axis_parametro]]`); a `index` de carpeta con ruta.
- `## Notas relacionadas` obligatoria al final.

---

## 🧩 Cobertura (coverage)

El refactor también **detecta y rellena huecos**: funciones de NumPy de uso común que nunca se
documentaron. Al refactorizar un grupo, listar las funciones faltantes de esa temática y crearlas
con el mismo listón (no solo mejorar las existentes). Mantener [[Tree Numpy]] sincronizado.

---

## 🧠 Filosofía final

- NumPy = sistema matemático sobre tensores.
- ndarray = estructura base · funciones = transformaciones · conceptos = reglas del sistema.
- Una nota útil explica **el eje, la forma, el tipo y la matemática**, no solo el nombre.
