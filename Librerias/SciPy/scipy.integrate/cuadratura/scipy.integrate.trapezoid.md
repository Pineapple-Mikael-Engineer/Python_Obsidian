---
title: scipy.integrate.trapezoid — regla del trapecio sobre datos muestreados
aliases:
  - trapezoid
  - scipy.integrate.trapezoid
  - trapz
  - regla del trapecio
tags:
  - scipy
  - api/funcion
  - integracion
lib: scipy
tipo: funcion
mod: scipy.integrate
retorna: float
requiere:
  - numpy
  - scipy.integrate.simpson
draft: false
---

# scipy.integrate.trapezoid — regla del trapecio sobre datos muestreados

Integra **datos ya muestreados** (un array `y`) aplicando la **regla del trapecio** (interpolacion lineal por tramos). NO recibe una funcion callable: recibe muestras. Las abscisas se dan via `x` o, si el muestreo es uniforme, via `dx`. Devuelve un **float** (o un array si se reduce un eje de un arreglo nD). Es el metodo mas simple y robusto: no asume suavidad, pero es menos preciso que `simpson` en funciones suaves.

> Distincion clave: `trapezoid` integra un **array de muestras** `y` (datos tabulados). `quad`/`dblquad` integran una **funcion callable**. Si tienes la funcion y no los datos, usa `quad`.

## Firma

```python
scipy.integrate.trapezoid(
    y,             # array_like: valores muestreados a integrar
    x=None,        # array_like | None: abscisas de las muestras (no uniformes permitidas)
    dx=1.0,        # float: espaciado entre muestras (solo si x is None)
    axis=-1,       # int: eje a lo largo del cual integrar
) -> float
```

> Nota historica: antes se llamaba `trapz` (nombre **deprecado** en SciPy a favor de `trapezoid`). Existe ademas `numpy.trapezoid` (antes `numpy.trapz`) con la misma semantica; la version de SciPy es equivalente y se mantiene por coherencia del submodulo `integrate`.

## Valor de retorno

| Tipo | Significado |
|------|-------------|
| `float` | Integral aproximada del array completo (caso 1D) |
| `ndarray` | Si `y` es nD: integral a lo largo de `axis`, reduciendo esa dimension |

## Formas basicas de llamada

| Situacion | Llamada |
|-----------|---------|
| Muestreo uniforme con paso conocido | `trapezoid(y, dx=h)` |
| Abscisas explicitas (uniformes o no) | `trapezoid(y, x=x)` |
| Muestreo uniforme paso 1 | `trapezoid(y)` |
| Array nD, integrar un eje | `trapezoid(Y, x=x, axis=0)` |

## Parametros en detalle

### `y` (obligatorio)

Array de **valores ya muestreados** a integrar. La funcion no evalua nada: solo une los puntos con segmentos rectos y suma las areas de los trapecios. Proviene de `y = f(x)` evaluado en una rejilla o de mediciones.

```python
import numpy as np
from scipy.integrate import trapezoid

x = np.linspace(0, np.pi, 100)
y = np.sin(x)                  # datos muestreados
trapezoid(y, x=x)             # → ~1.9998   (∫ sin x dx en [0, pi] ≈ 2)
```

### `x`

Abscisas de las muestras; admite **espaciado no uniforme**. Si se da `x`, se ignora `dx`. Debe igualar a `y` en longitud a lo largo de `axis`.

```python
x = np.array([0.0, 0.5, 2.0])   # paso irregular
y = np.array([0.0, 1.0, 0.0])
trapezoid(y, x=x)                # → 1.0   (area de los dos trapecios)
```

### `dx`

Espaciado **uniforme**, usado solo si `x is None`. Por defecto `1.0`.

```python
h = 0.01
x = np.arange(0, 1 + h, h)
trapezoid(np.exp(x), dx=h)    # → ~1.7183   (∫ e^x en [0,1] = e - 1)
```

### `axis`

Eje del array nD a lo largo del cual integrar; permite integrar muchas series simultaneamente.

## Casos de uso

### Integrar una señal/series temporales muestreadas

```python
import numpy as np
from scipy.integrate import trapezoid

# Distancia recorrida: ∫ v(t) dt a partir de velocidad muestreada (datos GPS)
t = np.array([0, 1, 2, 3, 4, 5])          # s
v = np.array([0, 2, 5, 6, 4, 0])          # m/s (mediciones)
distancia = trapezoid(v, x=t)             # → 18.0 m
```

### Carga acumulada de una corriente medida

```python
# Carga Q = ∫ i(t) dt con muestreo uniforme a 1 kHz
fs = 1000.0
t = np.arange(0, 0.01, 1/fs)
i = 0.5 * np.ones_like(t)                 # corriente constante 0.5 A
Q = trapezoid(i, dx=1/fs)                 # → ~0.005 C
```

### Integrar varias columnas por eje

```python
# Matriz (n_muestras, n_canales): integrar cada canal en el tiempo
Y = np.random.rand(201, 3)
t = np.linspace(0, 1, 201)
integrales = trapezoid(Y, x=t, axis=0)    # shape (3,)
```

## Buenas practicas

1. Usa `trapezoid` para **datos muestreados** crudos o ruidosos: no asume suavidad y es muy robusto.
2. Si tienes una funcion callable (no datos), usa `quad`: control de error y precision muy superiores.
3. Para datos **suaves y densos**, `simpson` suele dar mas precision con el mismo muestreo; el trapecio es la opcion segura cuando no hay garantia de suavidad.
4. Pasa `x` para muestreo no uniforme; usa `dx` solo con paso constante.
5. Usa `trapezoid`, no el antiguo `trapz` (deprecado).
6. Asegura `len(x) == y.shape[axis]` para evitar errores de forma.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Pasar una funcion como `y` | Espera un array, no un callable | Evaluar `y = f(x)`, o usar `quad` |
| Usar `trapz` y ver deprecacion | `trapz` fue renombrado | Usar `trapezoid` (o `np.trapezoid`) |
| Resultado escalado mal | `dx=1.0` por defecto con paso real != 1 | Pasar `dx` correcto o `x` |
| `ValueError` de longitudes | `x` e `y` no coinciden en `axis` | Igualar longitudes |
| Precision baja en curva muy curvada | El trapecio sub/sobreestima | Mas muestras o usar `simpson` |

## Limitaciones

- Solo integra **datos muestreados**; no evalua funciones ni estima cota de error.
- Menos preciso que `simpson` para funciones suaves (asume tramos lineales).
- No es adaptativo: la precision depende enteramente del muestreo.
- No maneja limites infinitos ni singularidades: eso corresponde a `quad`.

## Notas relacionadas

- [[scipy.integrate.simpson]]
- [[scipy.integrate.quad]]
- [[concepto_relacion_numpy]]
