---
title: scipy.fft.fftfreq — eje de frecuencias asociado a la salida de fft
aliases:
  - fftfreq
  - scipy.fft.fftfreq
  - frecuencias de muestreo
tags:
  - scipy
  - api/funcion
  - transformada-fourier
lib: scipy
tipo: funcion
mod: scipy.fft
retorna: ndarray (float)
requiere:
  - numpy
draft: false
---

# scipy.fft.fftfreq — eje de frecuencias asociado a la salida de fft

Devuelve el **array de frecuencias de muestreo** que corresponde, bin a bin, a la salida de `fft`. Sin el, los indices del espectro no tienen significado fisico: `fftfreq` traduce cada posicion del array a una frecuencia real (en Hz si `d` esta en segundos). Recibe la **longitud** `n` de la señal y el **espaciado** `d` entre muestras (`d = 1/fs`), y devuelve un `ndarray` de `n` frecuencias ordenadas segun la convencion de la FFT: `[0, positivas..., negativas...]`. Es el **compañero imprescindible** de `fft` para etiquetar el eje X del espectro.

> El orden no es ascendente: empieza en DC (0), sube por las positivas hasta casi Nyquist y luego salta a las negativas. Para obtener un eje monotono centrado en 0 se aplica `fftshift` tanto a las frecuencias como al espectro.

## Firma

```python
scipy.fft.fftfreq(
    n,          # int: longitud de la ventana / numero de muestras
    d=1.0,      # float: espaciado entre muestras (d = 1/fs)
) -> ndarray  # float, longitud n
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `ndarray` float | `(n,)` | Frecuencias de cada bin, orden `[0, +, -]` |

```python
freqs = fftfreq(n, d=1/fs)   # freqs[k] = frecuencia del bin k de fft
# valores: f = [0, 1, ..., n/2-1, -n/2, ..., -1] / (d*n)
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Eje en muestras (d=1) | `fftfreq(n)` |
| Eje en Hz dada fs | `fftfreq(n, d=1/fs)` |
| Centrar en 0 para graficar | `fftshift(fftfreq(n, d))` |
| Solo frecuencias positivas | `freqs[freqs >= 0]` |

## Parametros en detalle

### `n` (obligatorio)

Numero de muestras de la señal (la misma longitud que se paso o se obtuvo de `fft`). El array resultante tiene exactamente `n` frecuencias, una por bin del espectro.

```python
import numpy as np
from scipy.fft import fft, fftfreq

fs = 8                       # Hz
x = np.array([0, 1, 0, -1, 0, 1, 0, -1.0])
freqs = fftfreq(len(x), d=1/fs)
freqs   # → [ 0.,  1.,  2.,  3., -4., -3., -2., -1.]
```

### `d`

Espaciado temporal entre muestras, es decir el inverso de la frecuencia de muestreo: `d = 1/fs`. Si se deja en `1.0`, las frecuencias salen en ciclos por muestra (no en Hz). Pasar el `d` correcto es lo que da significado fisico al eje.

```python
fs = 500
freqs = fftfreq(1000, d=1/fs)   # frecuencias en Hz
freqs.min(), freqs.max()        # → (-250.0, 249.5)   Nyquist = fs/2
```

## Casos de uso

### Etiquetar el espectro de una señal

El uso canonico: `fft` da el espectro, `fftfreq` da el eje X, y se grafica solo el lado positivo con el modulo.

```python
import numpy as np
from scipy.fft import fft, fftfreq

fs = 500
t = np.arange(0, 1, 1/fs)
x = np.sin(2*np.pi*50*t)

X = fft(x)
freqs = fftfreq(len(x), d=1/fs)

pos = freqs >= 0
# eje: freqs[pos]    amplitud: np.abs(X[pos])
freqs[pos][np.argmax(np.abs(X[pos]))]   # → 50.0 Hz
```

### Centrar el espectro en 0 con fftshift

Para una vista simetrica `[-fs/2, fs/2]` se reordenan frecuencias y espectro con `fftshift`.

```python
from scipy.fft import fftshift
f_c = fftshift(freqs)        # frecuencias en orden ascendente
X_c = fftshift(X)            # espectro alineado con f_c
```

## Buenas practicas

1. Pasa siempre `d = 1/fs` para obtener Hz; dejar `d=1.0` da ciclos por muestra, rara vez lo que se quiere.
2. Usa la **misma `n`** que la longitud real de la señal (o el `n` que pasaste a `fft`).
3. Para graficar, queda con `freqs >= 0` o aplica `fftshift` a frecuencias y espectro juntos.
4. Para la salida de `rfft` usa `rfftfreq`, que devuelve solo las `n//2 + 1` frecuencias no negativas; `fftfreq` no encaja con `rfft`.
5. Recuerda que la maxima frecuencia representable es Nyquist = `fs/2`.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Frecuencias en orden raro | Es la convencion `[0,+,-]` de la FFT | Usar `fftshift` para ordenar |
| Eje en valores extraños (0..0.5) | `d` omitido (queda en 1.0) | Pasar `d = 1/fs` |
| Longitud no coincide con rfft | Se uso `fftfreq` con salida de `rfft` | Usar `rfftfreq(n, d)` |
| Frecuencia maxima inesperada | Confundir Nyquist con fs | Nyquist = `fs/2`, no `fs` |
| `fftshift` solo a freqs | No se desplazo tambien el espectro | Aplicar `fftshift` a ambos |

## Limitaciones

- Solo describe el eje; no calcula nada del espectro (eso lo hace `fft`).
- No es valido para la salida de `rfft`: para ese caso existe `rfftfreq`.
- El orden nativo no es monotono; para ejes ascendentes hay que combinar con `fftshift`.

## Notas relacionadas

- [[scipy.fft.fft]]
- [[scipy.fft.rfft]]
- [[scipy.fft.ifft]]
- [[concepto_relacion_numpy]]
