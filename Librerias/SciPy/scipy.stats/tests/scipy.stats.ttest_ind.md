---
title: scipy.stats.ttest_ind — t-test de dos muestras independientes
aliases:
  - ttest_ind
  - scipy.stats.ttest_ind
  - t-test independiente
  - test de Welch
tags:
  - scipy
  - api/funcion
  - tests
lib: scipy
tipo: funcion
mod: scipy.stats
retorna: TtestResult (statistic, pvalue)
requiere:
  - numpy
draft: false
---

# scipy.stats.ttest_ind — t-test de dos muestras independientes

Contrasta si **dos grupos independientes** (sin emparejar) tienen la **misma media poblacional**. Recibe dos arrays de observaciones `a` y `b` que no necesitan tener la misma longitud. Devuelve un **objeto-resultado** con atributos `.statistic` (el estadistico t) y `.pvalue`, desempaquetable como tupla `(t, p)`.

> Independiente vs pareado: `ttest_ind` es para grupos distintos de sujetos (control vs tratamiento). Si los datos son medidas repetidas del mismo sujeto (antes/despues) el test correcto es `ttest_rel`.

Por defecto asume varianzas iguales (`equal_var=True`); en la practica suele preferirse `equal_var=False` (test de Welch), mas robusto cuando las varianzas o los tamaños difieren.

## Firma

```python
scipy.stats.ttest_ind(
    a,                       # array_like: muestra del grupo 1
    b,                       # array_like: muestra del grupo 2
    axis=0,                  # int | None: eje sobre el que se calcula
    equal_var=True,          # bool: True -> Student; False -> Welch
    nan_policy='propagate',  # str: 'propagate' | 'raise' | 'omit'
    alternative='two-sided', # str: 'two-sided' | 'less' | 'greater'
    ...
) -> TtestResult
```

## Valor de retorno

Objeto-resultado (`TtestResult`, tipo Bunch) con acceso por atributo y desempaquetable como tupla.

| Atributo | Tipo | Significado |
|----------|------|-------------|
| `statistic` | `float` / `ndarray` | Estadistico t observado |
| `pvalue` | `float` / `ndarray` | p-valor del contraste |
| `df` | `float` | Grados de libertad usados (utiles en Welch) |

```python
t, p = ttest_ind(a, b)          # desempaquetado como tupla
res = ttest_ind(a, b)           # o como objeto
res.statistic, res.pvalue       # acceso por atributo
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Test estandar (varianzas iguales) | `ttest_ind(a, b)` |
| Test de Welch (recomendado) | `ttest_ind(a, b, equal_var=False)` |
| Hipotesis unilateral (media a > media b) | `ttest_ind(a, b, alternative='greater')` |
| Hipotesis unilateral (media a < media b) | `ttest_ind(a, b, alternative='less')` |
| Ignorando NaN | `ttest_ind(a, b, nan_policy='omit')` |

## Parametros en detalle

### `a`, `b` (obligatorios)

Las dos muestras independientes. No requieren igual longitud. Deben ser numericas; el test compara `mean(a)` con `mean(b)`.

```python
import numpy as np
from scipy.stats import ttest_ind

control = np.array([5.1, 4.9, 5.3, 5.0, 4.8])
tratado = np.array([5.6, 5.8, 5.5, 5.9, 6.0])
t, p = ttest_ind(control, tratado)
t    # → -6.0... (negativo: media de control < media de tratado)
p    # → ~0.0003  (p < 0.05 -> medias distintas)
```

### `equal_var`

Si `True` (por defecto) usa el t-test clasico de Student, que **asume varianzas poblacionales iguales**. Si `False` aplica la correccion de **Welch**, que no lo asume y ajusta los grados de libertad. Welch es la opcion segura cuando no hay garantia de homogeneidad de varianzas o los tamaños difieren.

```python
# Mismas muestras, test de Welch:
t, p = ttest_ind(control, tratado, equal_var=False)
```

### `alternative`

Define la hipotesis alternativa H1:

- `'two-sided'` (defecto): las medias son distintas (`mean(a) != mean(b)`).
- `'less'`: `mean(a) < mean(b)`.
- `'greater'`: `mean(a) > mean(b)`.

El test unilateral concentra toda la potencia en una direccion; usarlo solo si la direccion estaba prevista de antemano.

### `nan_policy`

`'propagate'` (defecto) devuelve NaN si hay NaN; `'omit'` los descarta; `'raise'` lanza error.

## Casos de uso

### Comparar dos tratamientos

```python
import numpy as np
from scipy.stats import ttest_ind

a = np.random.default_rng(0).normal(100, 10, size=40)
b = np.random.default_rng(1).normal(106, 10, size=40)
res = ttest_ind(a, b, equal_var=False)
res.pvalue    # p pequeño -> evidencia de medias distintas
```

### Test unilateral dirigido

```python
# H1: el grupo a rinde MENOS que el grupo b
t, p = ttest_ind(a, b, alternative='less')
```

## Interpretacion del p-valor

- **H0**: las medias poblacionales de ambos grupos son iguales (`mu_a = mu_b`).
- **H1**: difieren (o `<` / `>` segun `alternative`).
- Se fija un nivel de significacion `alfa` (tipicamente 0.05) **antes** de mirar los datos.
- Si `pvalue < alfa` → se **rechaza H0**: hay evidencia de que las medias difieren.
- Si `pvalue >= alfa` → **no se rechaza H0**: no hay evidencia suficiente de diferencia (lo cual no prueba que sean iguales).

```python
alfa = 0.05
t, p = ttest_ind(a, b, equal_var=False)
if p < alfa:
    print("Se rechaza H0: las medias difieren")
else:
    print("No se rechaza H0")
```

El signo de `statistic` indica la direccion: `t < 0` sugiere `mean(a) < mean(b)`.

## Buenas practicas

1. Usa `equal_var=False` (Welch) por defecto salvo que tengas evidencia clara de varianzas iguales.
2. Fija `alfa` y la `alternative` **antes** de ver los datos para no inflar el error tipo I.
3. Verifica los supuestos: independencia de muestras y normalidad aproximada (en n pequeño comprobar normalidad con un test propio).
4. Reporta tambien el tamaño del efecto (p. ej. diferencia de medias), no solo el p-valor.
5. Para datos emparejados usa el test pareado en lugar de este; ver la nota de [[scipy.stats.ttest_rel]].

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Usar `ttest_ind` con datos pareados | Confundir grupos distintos con medidas repetidas | Usar `ttest_rel` |
| Asumir varianzas iguales sin verificar | `equal_var=True` por defecto | Usar `equal_var=False` (Welch) |
| Interpretar `p` alto como "medias iguales" | No rechazar no es aceptar H0 | Reportar falta de evidencia, no igualdad |
| `pvalue` es NaN | Hay NaN en los datos | `nan_policy='omit'` o limpiar antes |
| Test unilateral elegido tras ver datos | Inflar error tipo I (p-hacking) | Fijar `alternative` a priori |

## Limitaciones

- Asume observaciones independientes e (idealmente) distribuciones aproximadamente normales; con n pequeño y datos muy no-normales pierde validez.
- Compara solo **medias**: no detecta diferencias de forma o varianza.
- Para mas de dos grupos no es el test adecuado (usar ANOVA `f_oneway`).
- Sensible a outliers, que distorsionan medias y varianzas.

## Notas relacionadas

- [[scipy.stats.ttest_rel]]
- [[scipy.stats.shapiro]]
- [[OptimizeResult]]
