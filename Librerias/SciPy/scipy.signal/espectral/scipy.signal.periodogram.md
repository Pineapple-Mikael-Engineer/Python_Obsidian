---
title: scipy.signal.periodogram — estimacion basica de la PSD (un solo periodograma)
aliases:
  - periodogram
  - scipy.signal.periodogram
  - periodograma
  - PSD directa
tags:
  - scipy
  - api/funcion
  - analisis-espectral
lib: scipy
tipo: funcion
mod: scipy.signal
retorna: tuple (ndarray, ndarray)
requiere:
  - numpy
  - scipy.fft
draft: false
---

# scipy.signal.periodogram — estimacion basica de la PSD (un solo periodograma)

Estima la **densidad espectral de potencia (PSD)** calculando **un unico periodograma** sobre toda la señal: aplica una ventana, hace la FFT y eleva al cuadrado la magnitud, sin promediar nada. Es la estimacion espectral **mas directa y rapida**, pero tambien la mas **ruidosa**: su varianza no disminuye aunque se alargue la señal. Sirve como primer vistazo o para fines didacticos; para señales reales casi siempre se prefiere el promediado de Welch. Devuelve una **tupla** `(f, Pxx)`.

> Contraste esencial: `periodogram` usa **una sola ventana** sobre toda la señal (alta varianza); `welch` parte la señal en segmentos y **promedia** sus periodogramas (baja varianza). Es el mismo estimador base, uno sin promediar y otro promediado, ver [[scipy.signal.welch]].

## Firma

```python
scipy.signal.periodogram(
    x,                    # array_like: señal de entrada
    fs=1.0,               # float: frecuencia de muestreo en Hz
    window='boxcar',      # str | tuple | array: ventana (default rectangular)
    nfft=None,            # int: longitud de FFT (zero-padding si > len(x))
    detrend='constant',   # str | callable | False: quita tendencia
    return_onesided=True, # bool: espectro de un solo lado (señal real)
    scaling='density',    # 'density' (V^2/Hz) | 'spectrum' (V^2)
    axis=-1,              # int: eje a lo largo del cual calcular
) -> tuple
```

## Valor de retorno

Devuelve la tupla `(f, Pxx)`. Desempaquetado tipico: `f, Pxx = periodogram(...)`.

| Posicion | Nombre | Tipo | Forma | Significado |
|----------|--------|------|-------|-------------|
| `[0]` | `f` | `ndarray` | `(nfft//2 + 1,)` | Frecuencias del espectro (en Hz si se dio `fs`) |
| `[1]` | `Pxx` | `ndarray` | igual que `f` | Densidad espectral de potencia por frecuencia |

A diferencia de `welch`, aqui la resolucion en frecuencia es maxima (usa toda la señal) pero la estimacion fluctua fuertemente entre bins vecinos.

```python
f, Pxx = periodogram(x, fs=1000)
f.shape, Pxx.shape   # → ((N//2 + 1,), (N//2 + 1,))  con N = len(x)
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| PSD directa con defaults | `periodogram(x, fs)` |
| Reducir fuga con ventana | `periodogram(x, fs, window='hann')` |
| Zero-padding para suavizar el grid | `periodogram(x, fs, nfft=4096)` |
| Potencia por bin | `periodogram(x, fs, scaling='spectrum')` |

## Parametros en detalle

### `x` (obligatorio)

Señal de entrada, tipicamente 1D. Toda la señal entra como una sola ventana; no hay segmentacion.

### `fs`

Frecuencia de muestreo en Hz. Sin ella, las frecuencias salen normalizadas en `[0, 0.5]` ciclos por muestra.

```python
import numpy as np
from scipy.signal import periodogram

fs = 1000.0
t = np.arange(0, 2, 1/fs)
x = np.sin(2*np.pi*100*t)
f, Pxx = periodogram(x, fs)
f[np.argmax(Pxx)]    # → 100.0   (tono limpio, señal sin ruido)
```

### `window`

Por defecto `'boxcar'` (ventana rectangular, sin atenuar bordes), lo que maximiza la fuga espectral. Para señales con tonos de amplitudes muy distintas conviene `'hann'` o `'hamming'` para reducir esa fuga.

### `nfft`

Longitud de la FFT. Si es mayor que `len(x)` aplica zero-padding, lo que **interpola** el espectro (grid mas fino) pero no añade resolucion real ni reduce la varianza.

### `scaling`

`'density'` (default) en `V^2/Hz`, comparable entre señales; `'spectrum'` en `V^2`, potencia por bin, util para leer amplitud de tonos discretos.

## Casos de uso

### Estimacion rapida y su alta varianza frente a Welch

```python
import numpy as np
from scipy.signal import periodogram, welch

fs = 1000.0
t = np.arange(0, 10, 1/fs)
x = np.sin(2*np.pi*60*t) + np.random.randn(t.size)

f_p, P_per = periodogram(x, fs)          # 1 ventana: muy ruidoso
f_w, P_wel = welch(x, fs, nperseg=1024)  # promedio: suave

P_per.std() > P_wel.std()    # → True   (el periodograma fluctua mas)
```

### Espectro de un tono puro (sin ruido)

```python
# Sin ruido el periodograma ya identifica el tono con nitidez
f, Pxx = periodogram(np.sin(2*np.pi*250*t), fs)
f[np.argmax(Pxx)]    # → 250.0
```

## Buenas practicas

1. **Pasa `fs`** para frecuencias en Hz; sin ello quedan normalizadas.
2. Usalo como **primer diagnostico** o con señales limpias; para señales ruidosas, migra a `welch`.
3. Cambia `window='boxcar'` por `'hann'` cuando convivan tonos fuertes y debiles (menos fuga).
4. No esperes que alargar la señal reduzca el ruido del estimador: solo afina el grid, no la varianza.
5. Usa `nfft` mayor para interpolar visualmente el espectro, recordando que no es resolucion real.
6. Desempaqueta la tupla: `f, Pxx = periodogram(...)`.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| PSD muy ruidosa / dentada | Naturaleza del periodograma (sin promediar) | Usar `welch` para reducir varianza |
| Frecuencias en `[0, 0.5]` | No se paso `fs` | Pasar `fs` real |
| Fuga espectral oculta tonos debiles | Ventana `boxcar` por defecto | Usar `window='hann'` u otra |
| Creer que mas muestras suaviza el espectro | El periodograma no es consistente en varianza | Promediar segmentos con `welch` |
| Tratar el retorno como un array | Devuelve `(f, Pxx)` | Desempaquetar la tupla |

## Limitaciones

- Estimador de **alta varianza**: ruidoso e inconsistente, no mejora al crecer la señal.
- Asume estacionariedad; para espectro variable en el tiempo usar `spectrogram`.
- No promedia ni segmenta: para el estandar practico de PSD usar `welch`.
- No entrega fase; solo magnitud de potencia.

## Notas relacionadas

- [[scipy.signal.welch]]
- [[scipy.signal.spectrogram]]
- [[concepto_relacion_numpy]]
