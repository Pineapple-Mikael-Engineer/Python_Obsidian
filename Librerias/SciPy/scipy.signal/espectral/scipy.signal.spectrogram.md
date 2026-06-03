---
title: scipy.signal.spectrogram — evolucion del espectro a lo largo del tiempo (STFT)
aliases:
  - spectrogram
  - scipy.signal.spectrogram
  - espectrograma
  - STFT por segmentos
tags:
  - scipy
  - api/funcion
  - analisis-espectral
lib: scipy
tipo: funcion
mod: scipy.signal
retorna: tuple (ndarray, ndarray, ndarray)
requiere:
  - numpy
  - scipy.signal.welch
draft: false
---

# scipy.signal.spectrogram — evolucion del espectro a lo largo del tiempo (STFT)

Calcula como **evoluciona el contenido en frecuencia de una señal a lo largo del tiempo**. Aplica una transformada de Fourier de tiempo corto (STFT): divide la señal en segmentos solapados y calcula el espectro de potencia de cada uno, de modo que cada columna del resultado es el espectro en un instante. Conceptualmente es `welch` **sin promediar los segmentos**, conservando cada uno como una franja temporal. Es la herramienta para señales **no estacionarias** (chirps, voz, transitorios). Devuelve una **tupla** `(f, t, Sxx)`.

> En SciPy reciente, la API moderna para STFT es la clase `ShortTimeFFT`, que reemplaza progresivamente a esta funcion (y a la antigua `stft`); `spectrogram` sigue vigente y conveniente para visualizacion rapida. El promediado de segmentos en una sola PSD lo hace en cambio [[scipy.signal.welch]].

## Firma

```python
scipy.signal.spectrogram(
    x,                       # array_like: señal de entrada
    fs=1.0,                  # float: frecuencia de muestreo en Hz
    window=('tukey', 0.25),  # str | tuple | array: ventana por segmento
    nperseg=None,            # int: muestras por segmento (resolucion temporal)
    noverlap=None,           # int: solape (default nperseg // 8)
    nfft=None,               # int: longitud de FFT
    detrend='constant',      # str | callable | False: quita tendencia
    return_onesided=True,    # bool: espectro de un solo lado (señal real)
    scaling='density',       # 'density' (V^2/Hz) | 'spectrum' (V^2)
    axis=-1,                 # int: eje temporal
    mode='psd',              # 'psd' | 'complex' | 'magnitude' | 'angle' | 'phase'
) -> tuple
```

## Valor de retorno

Devuelve la tupla `(f, t, Sxx)`. Desempaquetado tipico: `f, t, Sxx = spectrogram(...)`.

| Posicion | Nombre | Tipo | Forma | Significado |
|----------|--------|------|-------|-------------|
| `[0]` | `f` | `ndarray` | `(nf,)` | Frecuencias del espectro (eje vertical, en Hz si se dio `fs`) |
| `[1]` | `t` | `ndarray` | `(nt,)` | Instantes centrales de cada segmento (eje horizontal, en s) |
| `[2]` | `Sxx` | `ndarray` | `(nf, nt)` | Matriz 2D de potencia: filas = frecuencia, columnas = tiempo |

`Sxx[i, j]` es la potencia en la frecuencia `f[i]` en el instante `t[j]`. Esa matriz es lo que se grafica como mapa de calor tiempo-frecuencia.

```python
f, t, Sxx = spectrogram(x, fs=1000)
f.shape, t.shape, Sxx.shape   # → ((129,), (M,), (129, M))
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Espectrograma con defaults | `spectrogram(x, fs)` |
| Mas resolucion temporal (segmentos cortos) | `spectrogram(x, fs, nperseg=128)` |
| Mas resolucion en frecuencia (segmentos largos) | `spectrogram(x, fs, nperseg=2048)` |
| Solape alto (visual mas suave) | `spectrogram(x, fs, nperseg=256, noverlap=224)` |
| Magnitud en vez de PSD | `spectrogram(x, fs, mode='magnitude')` |

## Parametros en detalle

### `x` (obligatorio)

Señal a analizar, tipicamente 1D. Su contenido espectral puede cambiar en el tiempo (de ahi el espectrograma).

### `fs`

Frecuencia de muestreo en Hz. Determina las unidades reales de `f` (Hz) y de `t` (segundos). Sin ella, ambos ejes quedan normalizados.

### `nperseg`

Muestras por segmento. Fija el **compromiso tiempo-frecuencia**: segmentos cortos → buena localizacion temporal pero baja resolucion en frecuencia; segmentos largos → al reves. Es el parametro mas decisivo de la forma del espectrograma.

### `noverlap`

Solape entre segmentos. Por defecto `nperseg // 8`; subirlo (p. ej. 7/8 de `nperseg`) genera mas columnas y un mapa visualmente mas continuo, sin añadir informacion nueva.

### `window`

Ventana por segmento; default `('tukey', 0.25)` (rectangular con bordes suavizados). Para mayor control de fuga se usan `'hann'` o `'hamming'`.

### `mode`

Que devolver en `Sxx`: `'psd'` (default, densidad de potencia), `'magnitude'`, `'angle'`/`'phase'` (fase) o `'complex'` (STFT compleja completa). Para visualizar potencia, `'psd'` es lo habitual.

## Casos de uso

### Visualizar un chirp (frecuencia que sube con el tiempo)

```python
import numpy as np
from scipy.signal import spectrogram, chirp
import matplotlib.pyplot as plt

fs = 8000.0
t_sig = np.arange(0, 2, 1/fs)
# Chirp lineal de 100 Hz a 2000 Hz
x = chirp(t_sig, f0=100, f1=2000, t1=2, method='linear')

f, t, Sxx = spectrogram(x, fs, nperseg=256)
plt.pcolormesh(t, f, 10*np.log10(Sxx + 1e-12), shading='gouraud')
plt.ylabel('Hz'); plt.xlabel('s')
# → mapa de calor con una banda diagonal que asciende de 100 a 2000 Hz
```

### Instante de maxima energia y su frecuencia dominante

```python
# Frecuencia dominante en cada instante
f_dom = f[np.argmax(Sxx, axis=0)]
f_dom[:3]    # → frecuencias que crecen columna a columna (chirp ascendente)
```

## Buenas practicas

1. **Pasa `fs`** para que los ejes salgan en Hz y segundos reales.
2. Elige `nperseg` segun lo que importe: corto para captar transitorios rapidos, largo para separar frecuencias.
3. Visualiza en escala logaritmica: `10*np.log10(Sxx)` (en dB) revela detalles que la escala lineal aplasta; añade un piso `+ 1e-12` para evitar `log(0)`.
4. Usa `pcolormesh(t, f, Sxx)` respetando el orden `(t, f, Sxx)`: `t` al eje X, `f` al eje Y.
5. Sube `noverlap` para un mapa visualmente continuo sin cambiar la resolucion real.
6. Desempaqueta los tres elementos: `f, t, Sxx = spectrogram(...)`.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Tratar el retorno como dos arrays | Devuelve `(f, t, Sxx)`, tres elementos | Desempaquetar los tres |
| Ejes invertidos en `pcolormesh` | Orden incorrecto de argumentos | Usar `pcolormesh(t, f, Sxx)` |
| Espectrograma "lavado" sin detalle | Escala lineal aplasta el rango | Graficar `10*np.log10(Sxx)` en dB |
| `log(0)` o `-inf` al pasar a dB | Bins con potencia cero | Sumar piso: `Sxx + 1e-12` |
| No se ve la evolucion temporal | `nperseg` demasiado grande | Reducir `nperseg` para mas columnas |
| Bandas de frecuencia borrosas | `nperseg` demasiado pequeño | Aumentar `nperseg` |

## Limitaciones

- Sujeto al **principio de incertidumbre tiempo-frecuencia**: no se puede tener a la vez alta resolucion temporal y espectral; `nperseg` arbitra el compromiso.
- Para una unica PSD global (señal estacionaria) usar `welch`; para una estimacion directa unica, `periodogram`.
- En SciPy reciente la API recomendada para STFT es `ShortTimeFFT`, mas flexible (inversion, escalados); `spectrogram` queda como atajo de visualizacion.
- En modo `'psd'` no conserva la fase; para reconstruir la señal se necesita `mode='complex'` o `ShortTimeFFT`.

## Notas relacionadas

- [[scipy.signal.welch]]
- [[scipy.signal.periodogram]]
- [[concepto_relacion_numpy]]
