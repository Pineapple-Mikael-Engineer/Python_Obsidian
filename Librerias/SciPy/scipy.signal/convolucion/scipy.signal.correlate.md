---
title: scipy.signal.correlate — correlacion cruzada de dos arrays N-dimensionales
aliases:
  - correlate
  - scipy.signal.correlate
  - correlacion cruzada
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

# scipy.signal.correlate — correlacion cruzada de dos arrays N-dimensionales

Calcula la **correlacion cruzada** de dos arrays N-dimensionales: desliza `in2` sobre `in1` y, para cada desplazamiento (lag), suma los productos solapados **sin invertir** el segundo array. Mide la **similitud** entre ambas senales en funcion del desfase: el **pico** del resultado indica el desplazamiento en el que mas se parecen. Devuelve un `ndarray`. Es la herramienta para detectar un patron dentro de una senal o estimar el retardo entre dos senales.

> Convolucion vs correlacion: ambas deslizan y suman productos, pero la **convolucion invierte** (voltea) el segundo array y la **correlacion no**. Por eso la convolucion modela la salida de un sistema LTI, mientras que la correlacion mide parecido / alineamiento. Para senales simetricas (nucleo par) ambas coinciden.

## Firma

```python
scipy.signal.correlate(
    in1,                 # array_like: primera senal de entrada (N-D)
    in2,                 # array_like: segunda senal / patron (mismo n de dimensiones que in1)
    mode='full',         # str: 'full' | 'same' | 'valid' -> tamano de salida
    method='auto',       # str: 'auto' | 'direct' | 'fft' -> algoritmo interno
) -> ndarray
```

## Valor de retorno

| Tipo | Significado |
|------|-------------|
| `ndarray` | Correlacion cruzada de `in1` con `in2`; el indice del maximo marca el lag de mayor similitud |

```python
c = correlate(senal, patron)        # el pico de c indica el desfase
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Correlacion completa | `correlate(a, b)` |
| Salida del tamano de `in1` | `correlate(a, b, mode='same')` |
| Solo solape completo | `correlate(a, b, mode='valid')` |
| Forzar FFT (senales grandes) | `correlate(a, b, method='fft')` |
| Mapear indices a lags | `correlation_lags(len(a), len(b))` |

## Parametros en detalle

### `in1`, `in2` (obligatorios)

Las dos senales a correlacionar; deben tener el **mismo numero de dimensiones**. A diferencia de `convolve`, la correlacion **no es conmutativa**: `correlate(a, b)` es la version reflejada de `correlate(b, a)`. Por convencion `in1` es la senal larga donde se busca e `in2` el patron / plantilla.

```python
import numpy as np
from scipy.signal import correlate

a = np.array([0, 0, 1, 2, 1, 0, 0], dtype=float)
b = np.array([1, 2, 1], dtype=float)        # patron a localizar
c = correlate(a, b, mode='same')
int(np.argmax(c))    # → 3   (posicion central del patron en a)
```

### `mode`

Igual que en `convolve`: define el tamano de salida. Con `in1` de tamano `N` e `in2` de tamano `M`:

| Valor | Tamano (1D) | Uso tipico |
|-------|-------------|------------|
| `'full'` | `N + M - 1` | Todos los lags, incluido solape parcial (por defecto) |
| `'same'` | `N` | Salida alineada con `in1` |
| `'valid'` | `max(N, M) - min(N, M) + 1` | Solo lags de solape completo |

### `method`

Identico a `convolve`: `'direct'` (exacto, lento en grande), `'fft'` (rapido para senales grandes, con error de redondeo) y `'auto'` (SciPy decide). Para estimar retardos sobre senales largas, `'fft'` es lo habitual.

### `correlation_lags` (funcion auxiliar)

`correlate` devuelve un array de valores, pero **no** el vector de desplazamientos. `scipy.signal.correlation_lags(len(in1), len(in2), mode=...)` genera los lags correspondientes a cada indice, de modo que `lags[np.argmax(c)]` da el desfase en muestras.

```python
from scipy.signal import correlate, correlation_lags

c = correlate(s1, s2, mode='full')
lags = correlation_lags(len(s1), len(s2), mode='full')
desfase = lags[np.argmax(c)]        # retardo en muestras entre s1 y s2
```

## Casos de uso

### Deteccion de patron / plantilla

Localizar donde aparece un patron conocido dentro de una senal: el maximo de la correlacion marca la posicion de mejor coincidencia.

```python
import numpy as np
from scipy.signal import correlate

senal = np.zeros(20)
patron = np.array([1.0, 0.8, 0.6])
senal[10:13] = patron               # incrustamos el patron en la posicion 10
c = correlate(senal, patron, mode='valid')
int(np.argmax(c))    # → 10   (inicio del patron detectado)
```

### Estimacion de retardo entre dos senales

Dos sensores captan la misma fuente con un desfase; la correlacion cruzada lo recupera.

```python
import numpy as np
from scipy.signal import correlate, correlation_lags

base = np.random.randn(500)
retardo_real = 7
desplazada = np.roll(base, retardo_real)

c = correlate(desplazada, base, mode='full')
lags = correlation_lags(len(desplazada), len(base), mode='full')
lags[np.argmax(c)]    # → 7   (retardo estimado en muestras)
```

## Buenas practicas

1. Usa `correlation_lags` para traducir el indice del pico a un desfase real en muestras; no asumas que el centro es lag cero.
2. Para comparar similitud independientemente de la escala, **normaliza** o usa la correlacion normalizada (restar media, dividir por la norma) antes de buscar el pico.
3. Para senales largas, `method='fft'` acelera la estimacion de retardo de forma drastica.
4. Recuerda que `correlate(a, b)` no es simetrica: fija un orden consistente (senal, patron) y respetalo al interpretar el signo del lag.
5. Si el patron y el nucleo de un filtro coinciden salvo inversion, no confundas correlacion con convolucion: revisa si necesitas o no el reflejo.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Interpretar el indice del pico como el lag | El indice no es el desplazamiento directo | Mapear con `correlation_lags(...)` |
| Esperar el mismo resultado que `convolve` | La correlacion no invierte `in2` | Usar `convolve` si quieres la inversion |
| Pico poco fiable por amplitudes dispares | Senales sin normalizar | Restar media y dividir por la norma antes de correlacionar |
| `ValueError` por dimensionalidad distinta | `in1` y `in2` con distinto n de dimensiones | Igualar las dimensiones de ambas entradas |
| Lento con senales grandes | `method='direct'` | Cambiar a `method='fft'` |

## Limitaciones

- Como `convolve`, la via directa escala `O(N*M)`; sin `method='fft'` no es viable para senales muy largas.
- No devuelve los lags: hay que generarlos con `correlation_lags` y emparejarlos con la salida.
- La correlacion cruda depende de la amplitud; para comparar forma se necesita normalizacion previa.
- Para correlacion 2D de imagenes con control de borde existe `correlate2d`; para autocorrelacion basta con `correlate(x, x)`.

## Notas relacionadas

- [[scipy.signal.convolve]]
- [[scipy.signal.find_peaks]]
- [[concepto_relacion_numpy]]
