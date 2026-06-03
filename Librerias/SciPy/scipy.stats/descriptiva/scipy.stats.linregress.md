---
title: scipy.stats.linregress — regresion lineal por minimos cuadrados (LinregressResult)
aliases:
  - linregress
  - scipy.stats.linregress
  - regresion lineal simple
tags:
  - scipy
  - api/funcion
  - estadistica
lib: scipy
tipo: funcion
mod: scipy.stats
retorna: LinregressResult
requiere:
  - numpy
draft: false
---

# scipy.stats.linregress — regresion lineal por minimos cuadrados (LinregressResult)

Ajusta una **recta** `y = slope * x + intercept` a dos variables por **minimos cuadrados ordinarios** y devuelve, en una sola llamada, la pendiente, la ordenada, el coeficiente de correlacion, el p-valor del contraste y los errores estandar. Es la herramienta directa para **regresion lineal simple** (una variable predictora). Devuelve un objeto-resultado **LinregressResult** (namedtuple ampliado) cuyos campos se acceden por atributo. El coeficiente de determinacion es `r² = rvalue**2`. Para modelos **no lineales** (exponenciales, potencias, sigmoides, ajustes con varios parametros) no sirve: ahi se usan rutinas de ajuste de curvas.

> `rvalue` es el coeficiente de correlacion de Pearson del ajuste; eleva al cuadrado para obtener `r²`, la fraccion de varianza explicada por la recta. El `pvalue` contrasta H0: pendiente = 0 (la recta no aporta informacion).

## Firma

```python
scipy.stats.linregress(
    x,                       # array_like: predictor; o array 2D de 2 columnas/filas si y=None
    y=None,                  # array_like: respuesta (misma longitud que x)
    alternative='two-sided', # str: 'two-sided' | 'greater' | 'less' (para el p-valor de la pendiente)
) -> LinregressResult
```

## Valor de retorno

Objeto **LinregressResult**. Acceso por atributo (preferido) o desempaquetado de los 5 primeros campos.

| Campo | Tipo | Significado |
|-------|------|-------------|
| `slope` | `float` | Pendiente de la recta ajustada |
| `intercept` | `float` | Ordenada en el origen (valor de `y` cuando `x=0`) |
| `rvalue` | `float` | Coeficiente de correlacion de Pearson; `r² = rvalue**2` |
| `pvalue` | `float` | p-valor del contraste H0: pendiente = 0 |
| `stderr` | `float` | Error estandar de la **pendiente** |
| `intercept_stderr` | `float` | Error estandar de la **ordenada** (solo por atributo, no en desempaquetado) |

```python
res = linregress(x, y)
res.slope, res.intercept                 # parametros de la recta
res.rvalue**2                            # coeficiente de determinacion r²
res.intercept_stderr                     # solo accesible por atributo
slope, intercept, r, p, se = linregress(x, y)   # desempaquetado de los 5 primeros
```

> Al desempaquetar solo salen los **5 primeros** campos (`slope, intercept, rvalue, pvalue, stderr`). `intercept_stderr` queda fuera del orden posicional: hay que pedirlo como atributo.

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Ajuste de recta | `res = linregress(x, y)` |
| Desempaquetar parametros | `m, b, r, p, se = linregress(x, y)` |
| Coeficiente de determinacion | `linregress(x, y).rvalue**2` |
| Entrada como matriz de 2 columnas | `linregress(M)` |
| Contraste unilateral de pendiente | `linregress(x, y, alternative='greater')` |

## Parametros en detalle

### `x`, `y`

`x` es el predictor e `y` la respuesta, vectores 1D de **igual longitud**. Si `y=None`, `x` debe ser un array 2D con **dos** columnas (o filas), que se interpretan como las dos variables.

```python
import numpy as np
from scipy.stats import linregress

x = np.array([0, 1, 2, 3, 4, 5])
y = np.array([1.1, 2.9, 5.2, 6.8, 9.1, 11.0])   # aprox. y = 2x + 1
res = linregress(x, y)
res.slope        # → ~1.98
res.intercept    # → ~1.0
res.rvalue**2    # → ~0.999   (la recta explica casi toda la varianza)
```

### `alternative`

Hipotesis alternativa del p-valor de la **pendiente**: `'two-sided'` (defecto, pendiente != 0), `'greater'` (pendiente > 0) o `'less'` (pendiente < 0). No cambia los parametros ajustados, solo el `pvalue`.

## Casos de uso

### Ajuste de recta a datos experimentales y r²

```python
import numpy as np
from scipy.stats import linregress

# Ley de Hooke: fuerza vs elongacion -> la pendiente es la constante k
elongacion = np.array([0.00, 0.02, 0.04, 0.06, 0.08, 0.10])   # m
fuerza     = np.array([0.0, 1.0, 2.1, 2.9, 4.1, 5.0])          # N
res = linregress(elongacion, fuerza)
k = res.slope            # → ~50 N/m   (constante del resorte)
res.rvalue**2            # → ~0.998    (ajuste excelente)
res.stderr               # incertidumbre de k
```

### Predecir con la recta ajustada e informar incertidumbre

```python
res = linregress(elongacion, fuerza)
x_nuevo = 0.05
y_pred = res.slope * x_nuevo + res.intercept   # fuerza estimada a 0.05 m
res.intercept_stderr                            # error de la ordenada
```

### Decidir si la pendiente es significativa

```python
res = linregress(x, y)
if res.pvalue < 0.05:
    "Hay relacion lineal significativa (pendiente != 0)"
```

## Buenas practicas

1. Reporta `r² = rvalue**2`, no `rvalue` a secas, como medida de bondad del ajuste.
2. Acompaña `slope` e `intercept` de sus errores (`stderr`, `intercept_stderr`) para comunicar incertidumbre.
3. Inspecciona un grafico de dispersion y los residuos: un `r²` alto no garantiza que la recta sea el modelo correcto.
4. Recuerda que `intercept_stderr` **no** sale al desempaquetar; accede por atributo.
5. Limpia los `NaN` antes de llamar: `linregress` no tiene `nan_policy` y propaga `NaN` al resultado.
6. Si el patron es claramente curvo (exponencial, potencia, sigmoide), no fuerces una recta: usa un ajuste no lineal con [[scipy.optimize.curve_fit]] o, para residuos generales, [[scipy.optimize.least_squares]].

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Informar `rvalue` como bondad del ajuste | La fraccion explicada es `r²` | Usar `res.rvalue**2` |
| `intercept_stderr` no aparece al desempaquetar | El desempaquetado da solo 5 campos | Acceder por atributo `res.intercept_stderr` |
| Resultado lleno de `NaN` | Datos con huecos; no hay `nan_policy` | Filtrar `NaN` antes de llamar |
| Forzar recta a datos curvos | El modelo lineal no aplica | Usar `curve_fit` / `least_squares` |
| `ValueError` por longitudes distintas | `x` e `y` deben coincidir en tamaño | Alinear los arrays |
| Interpretar p-valor como calidad del ajuste | El `pvalue` contrasta solo pendiente = 0 | Mirar `r²` y residuos para la calidad |

## Limitaciones

- Solo **regresion lineal simple**: una variable predictora y una recta; no hace regresion multiple.
- No ajusta modelos **no lineales**; para eso, ajuste de curvas o minimos cuadrados generales.
- Sensible a **outliers**, como todo minimos cuadrados ordinario.
- No tiene parametro `nan_policy`: hay que limpiar los datos faltantes manualmente.
- El `pvalue` y los errores estandar asumen residuos aproximadamente normales y homocedasticos.

## Notas relacionadas

- [[scipy.stats.pearsonr]]
- [[scipy.stats.spearmanr]]
- [[scipy.optimize.curve_fit]]
- [[scipy.optimize.least_squares]]
