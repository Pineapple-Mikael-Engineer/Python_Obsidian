---
title: scipy.fft.fft — transformada discreta de Fourier 1D (espectro complejo)
aliases:
  - fft
  - scipy.fft.fft
  - transformada de fourier
tags:
  - scipy
  - api/funcion
  - transformada-fourier
lib: scipy
tipo: funcion
mod: scipy.fft
retorna: ndarray (complejo)
requiere:
  - numpy
draft: false
---

# scipy.fft.fft — transformada discreta de Fourier 1D (espectro complejo)

Calcula la **Transformada Discreta de Fourier** (DFT) de una secuencia 1D mediante el algoritmo **FFT**. Recibe un array `x` (real o complejo) y devuelve un array **complejo del mismo tamaño** con el espectro: cada elemento es la amplitud compleja (modulo y fase) de una frecuencia. La salida sigue la **convencion fftfreq**: primero la componente continua (DC), luego las frecuencias positivas, luego las negativas. Para conocer a que frecuencia corresponde cada bin se usa el array de `fftfreq`, y para el modulo (amplitud) se aplica `np.abs` sobre la salida.

> `scipy.fft` es preferible a `numpy.fft`: es mas rapido, soporta mas tipos de dato y permite paralelizar con `workers`. La API es compatible, asi que migrar es casi solo cambiar el import.

## Firma

```python
scipy.fft.fft(
    x,              # array_like: secuencia de entrada (real o compleja)
    n=None,         # int | None: longitud de la transformada (zero-padding o truncado)
    axis=-1,        # int: eje sobre el que transformar (ultimo por defecto)
    norm=None,      # str | None: 'backward' (def) | 'ortho' | 'forward'
    overwrite_x=False,  # bool: permite sobrescribir x para ahorrar memoria
    workers=None,   # int | None: numero de hilos para paralelizar
    plan=None,      # objeto plan precalculado (avanzado)
) -> ndarray  # complejo
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `ndarray` complejo | misma que `x` (o con `n` en `axis`) | Espectro: amplitud compleja por frecuencia |

```python
X = fft(x)        # X[k] = amplitud compleja de la frecuencia k
np.abs(X)         # modulo (amplitud) de cada componente
np.angle(X)       # fase de cada componente
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Espectro de una señal | `fft(x)` |
| Forzar longitud (padding/truncado) | `fft(x, n=1024)` |
| Normalizacion ortonormal | `fft(x, norm='ortho')` |
| Transformar a lo largo de un eje | `fft(M, axis=0)` |
| Paralelizar | `fft(x, workers=-1)` |

## Parametros en detalle

### `x` (obligatorio)

Secuencia de entrada. Puede ser real o compleja; en ambos casos la salida es **compleja**. Si la señal es estrictamente real, conviene usar `rfft` para evitar la mitad redundante del espectro.

```python
import numpy as np
from scipy.fft import fft, fftfreq

fs = 100                              # frecuencia de muestreo (Hz)
t = np.arange(0, 1, 1/fs)            # 1 s de señal
x = np.sin(2*np.pi*5*t)             # tono puro de 5 Hz
X = fft(x)
X.shape    # → (100,)   espectro complejo del mismo tamaño
```

### `n`

Longitud de la transformada. Si `n > len(x)` aplica **zero-padding** (mas resolucion espectral aparente); si `n < len(x)` **trunca** la señal. Por defecto usa `len(x)` sobre `axis`.

```python
X = fft(x, n=256)   # interpola el espectro con relleno de ceros
X.shape             # → (256,)
```

### `axis`

Eje sobre el que se transforma. Util con arrays 2D donde cada fila o columna es una señal independiente.

### `norm`

Controla el factor de escala entre directa e inversa:

| `norm` | fft escala por | ifft escala por |
|--------|----------------|-----------------|
| `'backward'` (def) | 1 | 1/n |
| `'ortho'` | 1/√n | 1/√n |
| `'forward'` | 1/n | 1 |

Usar `'ortho'` cuando se necesita que la transformada **conserve la energia** (Parseval) y que directa e inversa sean simetricas.

### `workers`

Numero de hilos para paralelizar transformadas independientes (p. ej. multiples ejes o lotes). `workers=-1` usa todos los nucleos. No tiene equivalente en `numpy.fft`.

## Casos de uso

### Identificar la frecuencia dominante

```python
import numpy as np
from scipy.fft import fft, fftfreq

fs = 500
t = np.arange(0, 1, 1/fs)
x = np.sin(2*np.pi*50*t) + 0.5*np.sin(2*np.pi*120*t)

X = fft(x)
freqs = fftfreq(len(x), d=1/fs)
mag = np.abs(X)

# pico en el lado positivo del espectro
pos = freqs > 0
freqs[pos][np.argmax(mag[pos])]   # → 50.0 Hz
```

### Espectro de amplitud normalizado

```python
N = len(x)
mag = 2.0/N * np.abs(X[:N//2])   # un solo lado, escalado a amplitud real
```

## Buenas practicas

1. Acompaña siempre `fft` con `fftfreq` para etiquetar el eje de frecuencias; sin el, los indices no tienen significado fisico.
2. Para el espectro visible usa `np.abs(X)` (modulo); la fase con `np.angle(X)`.
3. Si la señal es **real**, prefiere `rfft`: la mitad del computo y de la memoria.
4. Usa `workers=-1` en lotes grandes para aprovechar todos los nucleos.
5. Elige `norm='ortho'` si necesitas conservacion de energia o simetria directa/inversa.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Espectro "espejado" inesperado | Mitad negativa del array no interpretada | Usar `fftfreq` y quedarse con `freqs >= 0` |
| Amplitudes que no cuadran | Falta el factor 1/N | Escalar por `1/N` (o `2/N` para un solo lado) |
| Frecuencias mal etiquetadas | `d` incorrecto en `fftfreq` | Pasar `d = 1/fs` |
| Usar `fft` con señal real | Computa mitad redundante | Cambiar a `rfft` |
| Resultado solo real esperado | `fft` siempre devuelve complejo | Trabajar con `np.abs`/`np.angle` |

## Limitaciones

- Devuelve **siempre** un array complejo, incluso para entrada real (usar `rfft` en ese caso).
- La resolucion en frecuencia es `fs/n`: para distinguir frecuencias cercanas hace falta mas muestras o mas `n`.
- No aplica ventana: el espectro de señales no periodicas en la ventana sufre fuga espectral (leakage); ventanear antes si procede.

## Notas relacionadas

- [[scipy.fft.ifft]]
- [[scipy.fft.rfft]]
- [[scipy.fft.fftfreq]]
- [[concepto_relacion_numpy]]
