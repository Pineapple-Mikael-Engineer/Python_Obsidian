---
title: scipy.signal.convolve — convolucion de dos arrays N-dimensionales
aliases:
  - convolve
  - scipy.signal.convolve
  - convolucion senal nucleo
tags:
  - scipy
  - api/funcion
  - procesamiento-senales
lib: scipy
tipo: funcion
mod: scipy.signal
retorna: ndarray
requiere:
  - numpy
draft: false
---

# scipy.signal.convolve — convolucion de dos arrays N-dimensionales

Calcula la **convolucion** de dos arrays N-dimensionales `in1 * in2`: desliza el segundo array (el **nucleo** o respuesta al impulso) sobre el primero (la **senal**), lo **invierte** y suma los productos solapados. Es la operacion base de los sistemas LTI: si `in2` es la respuesta al impulso `h`, entonces `convolve(x, h)` es la salida del sistema ante la entrada `x`. Devuelve un `ndarray`; su tamano depende de `mode`. La diferencia con `correlate` es que la convolucion **invierte** el segundo array antes de deslizarlo.

> Para senales grandes, la convolucion directa es lenta (coste `O(N*M)`). Usa `method='fft'`, o las funciones dedicadas `fftconvolve` / `oaconvolve`, que aprovechan la FFT y escalan mucho mejor.

## Firma

```python
scipy.signal.convolve(
    in1,                 # array_like: primera senal de entrada (N-D)
    in2,                 # array_like: segunda senal / nucleo (mismo n de dimensiones que in1)
    mode='full',         # str: 'full' | 'same' | 'valid' -> tamano de salida
    method='auto',       # str: 'auto' | 'direct' | 'fft' -> algoritmo interno
) -> ndarray
```

## Valor de retorno

| Tipo | Significado |
|------|-------------|
| `ndarray` | Convolucion discreta de `in1` con `in2`; tamano segun `mode`, dtype promocionado de ambas entradas |

```python
y = convolve(x, h)        # senal de salida del sistema LTI
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Convolucion completa | `convolve(x, h)` |
| Salida del tamano de la senal | `convolve(x, h, mode='same')` |
| Solo solape completo | `convolve(x, h, mode='valid')` |
| Forzar FFT (senales grandes) | `convolve(x, h, method='fft')` |
| Forzar algoritmo directo | `convolve(x, h, method='direct')` |

## Parametros en detalle

### `in1`, `in2` (obligatorios)

Los dos arrays a convolucionar. Deben tener el **mismo numero de dimensiones** (1D con 1D, 2D con 2D, etc.). Conceptualmente `in1` es la senal e `in2` el nucleo / respuesta al impulso, pero la convolucion es **conmutativa**: `convolve(a, b)` y `convolve(b, a)` dan el mismo resultado (salvo el recorte de `mode='same'`, que se refiere a `in1`).

```python
import numpy as np
from scipy.signal import convolve

x = np.array([1, 2, 3])
h = np.array([0, 1, 0.5])
convolve(x, h)            # → [0.  1.  2.5  4.  1.5]   (tamano 3+3-1 = 5)
```

### `mode`

Controla el tamano de la salida. Si `in1` tiene tamano `N` e `in2` tamano `M`:

| Valor | Tamano (1D) | Que conserva |
|-------|-------------|--------------|
| `'full'` | `N + M - 1` | Todo el solape, incluso parcial en los bordes (por defecto) |
| `'same'` | `N` | Centrado, mismo tamano que `in1` |
| `'valid'` | `max(N, M) - min(N, M) + 1` | Solo posiciones de **solape completo**, sin efecto de borde |

```python
x = np.ones(5)
h = np.ones(3)
convolve(x, h, mode='full')    # → [1. 2. 3. 3. 3. 2. 1.]  (7 valores)
convolve(x, h, mode='same')    # → [2. 3. 3. 3. 2.]        (5 valores)
convolve(x, h, mode='valid')   # → [3. 3. 3.]              (3 valores)
```

### `method`

Elige el algoritmo. `'direct'` suma los productos (exacto, lento en grande); `'fft'` convoluciona via transformada de Fourier (mucho mas rapido cuando ambos arrays son grandes, con error de redondeo de punto flotante). Con `'auto'` SciPy estima cual conviene segun los tamanos.

```python
ruido = np.random.randn(100_000)
nucleo = np.ones(2_000) / 2_000
y = convolve(ruido, nucleo, method='fft')   # FFT: ordenes de magnitud mas rapido que 'direct'
```

## Casos de uso

### Suavizado por media movil

Un nucleo de unos normalizado promedia cada muestra con sus vecinas, atenuando el ruido de alta frecuencia.

```python
import numpy as np
from scipy.signal import convolve

senal = np.array([1, 5, 2, 8, 3, 9, 4], dtype=float)
k = 3
nucleo = np.ones(k) / k                       # media movil de 3 muestras
suave = convolve(senal, nucleo, mode='same')
suave    # → [2.   2.67 5.   4.33 6.67 5.33 4.33]  aprox
```

### Respuesta de un sistema LTI

Si `h` es la respuesta al impulso del sistema, la salida ante `x` es su convolucion.

```python
x = np.array([1, 0, 0, 0], dtype=float)       # impulso unitario
h = np.array([0.5, 0.3, 0.2])                 # respuesta al impulso
y = convolve(x, h)
y    # → [0.5 0.3 0.2 0.  0.  0.]  (la salida reproduce h)
```

## Buenas practicas

1. Para suavizado, **normaliza** el nucleo (`np.ones(k)/k`) para no escalar la amplitud de la senal.
2. Usa `mode='same'` cuando necesites alinear la salida con la entrada (misma longitud, mismo eje temporal).
3. Usa `mode='valid'` si quieres descartar los efectos de borde donde el solape es parcial.
4. Para senales largas, prefiere `method='fft'` o directamente `fftconvolve`; para nucleos muy largos sobre senales muy largas, `oaconvolve` (overlap-add) es la opcion mas eficiente en memoria.
5. Asegurate de que ambas entradas tengan el mismo numero de dimensiones; mezclar 1D con 2D lanza error.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Salida mas larga de lo esperado | `mode='full'` da `N+M-1` | Usar `mode='same'` si quieres el tamano de `in1` |
| `ValueError: in1 and in2 should have the same dimensionality` | Una entrada es 1D y la otra 2D | Igualar el n de dimensiones de ambas |
| Amplitud de la senal alterada al suavizar | Nucleo sin normalizar | Dividir el nucleo por su suma (`np.ones(k)/k`) |
| Convolucion lenta con arrays grandes | `method='direct'` con N y M grandes | Usar `method='fft'`, `fftconvolve` u `oaconvolve` |
| Confundir resultado con correlacion | `convolve` invierte el segundo array | Usar `correlate` si no quieres la inversion |

## Limitaciones

- La convolucion directa escala como `O(N*M)`; se vuelve impracticable para senales y nucleos grandes sin `method='fft'`.
- `mode='valid'` exige que una entrada no sea mayor que la otra en ninguna dimension; si no, no hay solape completo.
- La via FFT introduce error de redondeo de punto flotante y asume condiciones de contorno circulares antes del recorte; no es bit-exacta frente a `'direct'`.
- Para convolucion 2D especifica de imagenes con control de borde y origen, existe `convolve2d`.

## Notas relacionadas

- [[scipy.signal.correlate]]
- [[scipy.signal.find_peaks]]
- [[concepto_relacion_numpy]]
