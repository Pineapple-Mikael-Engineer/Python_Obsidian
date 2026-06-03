---
title: scipy.fft.rfft — FFT de entrada real (solo frecuencias no redundantes)
aliases:
  - rfft
  - scipy.fft.rfft
  - fft real
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

# scipy.fft.rfft — FFT de entrada real (solo frecuencias no redundantes)

Calcula la **DFT de una señal real** aprovechando su **simetria hermitica**: como el espectro de una señal real cumple `X[-k] = conj(X[k])`, la mitad negativa es redundante y `rfft` no la calcula. Recibe un array real de longitud `n` y devuelve solo las **`n//2 + 1` frecuencias no negativas** (complejas), desde DC hasta la frecuencia de Nyquist. Frente a `fft` esto significa la **mitad de memoria** y mas velocidad para el caso real, que es el habitual en analisis de señales fisicas. Su inversa es `irfft` y su eje de frecuencias lo da `rfftfreq`.

> Regla: si la entrada es estrictamente real, usa `rfft` en vez de `fft`. Si la entrada es compleja, `rfft` no aplica (descartaria informacion); ahi va `fft`.

## Firma

```python
scipy.fft.rfft(
    x,              # array_like: secuencia REAL de entrada
    n=None,         # int | None: longitud de la transformada (padding/truncado)
    axis=-1,        # int: eje sobre el que transformar
    norm=None,      # str | None: 'backward' (def) | 'ortho' | 'forward'
    overwrite_x=False,  # bool: permite sobrescribir x
    workers=None,   # int | None: hilos para paralelizar
    plan=None,      # objeto plan (avanzado)
) -> ndarray  # complejo, longitud n//2 + 1
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `ndarray` complejo | `n//2 + 1` sobre `axis` | Frecuencias de 0 (DC) a Nyquist, sin la mitad negativa |

```python
X = rfft(x)        # solo frecuencias >= 0
len(X)             # == n//2 + 1   (n = longitud de x)
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Espectro de señal real | `rfft(x)` |
| Forzar longitud (padding/truncado) | `rfft(x, n=2048)` |
| Normalizacion ortonormal | `rfft(x, norm='ortho')` |
| Por eje en lote 2D | `rfft(M, axis=1)` |
| Paralelizar | `rfft(x, workers=-1)` |

## Parametros en detalle

### `x` (obligatorio)

Secuencia **real**. Si se le pasa un array complejo, SciPy ignora la parte imaginaria (no es lo deseado): para entrada compleja usar `fft`.

```python
import numpy as np
from scipy.fft import rfft, rfftfreq

fs = 1000
t = np.arange(0, 1, 1/fs)
x = np.sin(2*np.pi*60*t)          # tono real de 60 Hz
X = rfft(x)
X.shape    # → (501,)   = len(x)//2 + 1   (frente a 1000 de fft)
```

### `n`

Longitud de la transformada sobre `axis`. `n > len(x)` aplica zero-padding; `n < len(x)` trunca. El tamaño de salida es `n//2 + 1`.

### `axis`

Eje a transformar en arrays multidimensionales (p. ej. un lote de señales por filas).

### `norm`

Igual que en `fft`: `'backward'` (def), `'ortho'` o `'forward'` controlan el factor de escala. Debe coincidir con el de `irfft` para reconstruir bien.

### `workers`

Hilos para paralelizar; `workers=-1` usa todos los nucleos. Especialmente util en lotes grandes de señales reales.

## Casos de uso

### Analisis espectral de una señal real

```python
import numpy as np
from scipy.fft import rfft, rfftfreq

fs = 1000
t = np.arange(0, 1, 1/fs)
x = np.sin(2*np.pi*60*t) + 0.4*np.sin(2*np.pi*200*t)

X = rfft(x)
freqs = rfftfreq(len(x), d=1/fs)   # eje de frecuencias para rfft
mag = np.abs(X)

freqs[np.argmax(mag)]   # → 60.0 Hz   (pico dominante)
```

### Espectro de amplitud de un solo lado

```python
N = len(x)
amp = 2.0/N * np.abs(rfft(x))   # amplitud real por frecuencia (un lado)
amp[0] /= 2                     # DC no se duplica
```

## Buenas practicas

1. Usa `rfft` siempre que la señal sea real: mitad de memoria y mas rapido que `fft`.
2. Empareja `rfft` con `rfftfreq` (no `fftfreq`) para etiquetar el eje: `rfftfreq` solo da las frecuencias no negativas.
3. Para reconstruir usa `irfft` y, si forzaste `n`, pasa el mismo `n` a `irfft` para recuperar la longitud original.
4. Al convertir a amplitud de un solo lado, duplica todas las componentes menos DC (y Nyquist si `n` es par).
5. Mantén el mismo `norm` entre `rfft` e `irfft`.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Eje de frecuencias no cuadra | Se uso `fftfreq` en vez de `rfftfreq` | Usar `rfftfreq(n, d)` |
| Longitud reconstruida cambia | `irfft` asume `n` par por defecto | Pasar el `n` original a `irfft` |
| Amplitudes a la mitad | No se duplico el espectro de un lado | Multiplicar por 2 (salvo DC/Nyquist) |
| Resultado raro con entrada compleja | `rfft` es solo para señales reales | Usar `fft` para entrada compleja |
| Esperar `n` salidas | `rfft` devuelve `n//2 + 1` | Es el comportamiento correcto |

## Limitaciones

- Solo valida para entrada **real**; descarta la parte imaginaria si se le pasa una señal compleja.
- La salida no es directamente invertible con `ifft`: requiere `irfft`.
- Como `irfft` no puede inferir si `n` original era par o impar, hay que pasarle `n` para recuperar la longitud exacta.

## Notas relacionadas

- [[scipy.fft.fft]]
- [[scipy.fft.ifft]]
- [[scipy.fft.fftfreq]]
- [[concepto_relacion_numpy]]
