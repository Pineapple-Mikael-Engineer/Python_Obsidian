---
title: scipy.stats.shapiro — test de normalidad de Shapiro-Wilk
aliases:
  - shapiro
  - scipy.stats.shapiro
  - Shapiro-Wilk
  - test de normalidad
tags:
  - scipy
  - api/funcion
  - tests
lib: scipy
tipo: funcion
mod: scipy.stats
retorna: ShapiroResult (statistic, pvalue)
requiere:
  - numpy
draft: false
---

# scipy.stats.shapiro — test de normalidad de Shapiro-Wilk

Contrasta si una **muestra** `x` proviene de una **distribucion normal**. Recibe un unico array de observaciones y devuelve un **objeto-resultado** con `.statistic` (el estadistico W, entre 0 y 1; cuanto mas cerca de 1, mas normal parece la muestra) y `.pvalue`, desempaquetable como tupla. Es uno de los tests de normalidad mas potentes en muestras **pequeñas a medianas**.

> Direccion del contraste: aqui H0 es que la muestra **es** normal. Por eso un `pvalue` **alto** apoya la normalidad y uno **bajo** la rechaza. Es el sentido inverso al habitual cuando uno "quiere" un resultado significativo.

## Firma

```python
scipy.stats.shapiro(
    x,   # array_like: la muestra (1D); n entre 3 y unos 5000
) -> ShapiroResult
```

## Valor de retorno

Objeto-resultado (`ShapiroResult`, tipo Bunch) con acceso por atributo y desempaquetable como tupla.

| Atributo | Tipo | Significado |
|----------|------|-------------|
| `statistic` | `float` | Estadistico W de Shapiro-Wilk (0 a 1; ~1 = mas normal) |
| `pvalue` | `float` | p-valor del contraste |

```python
W, p = shapiro(x)        # desempaquetado como tupla
res = shapiro(x)         # o como objeto
res.statistic, res.pvalue
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Test de normalidad de una muestra | `shapiro(x)` |
| Acceder al estadistico W | `shapiro(x).statistic` |
| Acceder al p-valor | `shapiro(x).pvalue` |

## Parametros en detalle

### `x` (obligatorio)

La muestra 1D a evaluar. Necesita al menos **3 observaciones**. Por encima de unos pocos miles de puntos el test se vuelve hipersensible (ver Limitaciones).

```python
import numpy as np
from scipy.stats import shapiro

rng = np.random.default_rng(0)
datos = rng.normal(loc=0, scale=1, size=50)   # muestra normal
W, p = shapiro(datos)
W    # → ~0.98  (cercano a 1)
p    # → p alto (> 0.05) -> no se rechaza la normalidad
```

```python
# Muestra claramente no normal (exponencial)
datos = rng.exponential(scale=1.0, size=50)
W, p = shapiro(datos)
p    # → p bajo (< 0.05) -> se rechaza la normalidad
```

## Casos de uso

### Comprobar el supuesto de un t-test

```python
import numpy as np
from scipy.stats import shapiro

residuos = np.array([...])
W, p = shapiro(residuos)
if p < 0.05:
    print("Residuos no normales: revisar el modelo o usar test no parametrico")
```

### Inspeccionar normalidad de las diferencias antes de un test pareado

```python
diff = antes - despues
res = shapiro(diff)
res.pvalue    # apoya o no el supuesto de normalidad de las diferencias
```

## Interpretacion del p-valor

- **H0**: la muestra **proviene de una distribucion normal**.
- **H1**: la muestra **no** es normal.
- Se fija `alfa` (p. ej. 0.05) **antes** de ver los datos.
- Si `pvalue < alfa` → se **rechaza H0**: hay evidencia de que la muestra **no** es normal.
- Si `pvalue >= alfa` → **no se rechaza H0**: la muestra es **compatible** con la normalidad (no la demuestra, solo no la contradice).

```python
alfa = 0.05
W, p = shapiro(x)
if p < alfa:
    print("Se rechaza la normalidad")
else:
    print("No hay evidencia contra la normalidad")
```

> Cuidado con la asimetria de la decision: "no rechazar" no prueba normalidad; solo indica falta de evidencia en contra, algo comun en muestras pequeñas por baja potencia.

## Buenas practicas

1. Combina el test con una inspeccion grafica (histograma, Q-Q plot): el test resume, el grafico explica.
2. Usalo en muestras pequeñas-medianas, donde es mas potente y mas informativo.
3. No lo apliques a n muy grande sin contexto: detectara desviaciones triviales sin relevancia practica.
4. Para chequear normalidad en un t-test pareado, testea las **diferencias**, no cada grupo por separado.
5. Si se rechaza la normalidad, considera alternativas no parametricas o una transformacion de los datos.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Interpretar p alto como "es normal" | No rechazar no es demostrar H0 | Reportar como "compatible con normal" |
| Aplicarlo a n enorme | Hipersensible, rechaza por nada | Usar tamaño del efecto / graficos |
| Testear grupos en vez de diferencias (pareado) | El supuesto es sobre `a - b` | Aplicar a las diferencias |
| Pasar menos de 3 datos | Tamaño insuficiente | Reunir mas observaciones |
| Confundir W con el p-valor | `statistic` es W, no la probabilidad | Usar `.pvalue` para decidir |

## Limitaciones

- **Poco fiable con n muy grande**: con miles de puntos detecta desviaciones minimas e irrelevantes y casi siempre rechaza.
- Pensado para muestras 1D; no evalua normalidad multivariante.
- Baja potencia con n muy pequeño: puede no rechazar aunque haya no-normalidad.
- Solo contrasta normalidad; para ajuste a otras distribuciones usar `kstest` o `anderson`.

## Notas relacionadas

- [[scipy.stats.kstest]]
- [[scipy.stats.ttest_ind]]
- [[OptimizeResult]]
