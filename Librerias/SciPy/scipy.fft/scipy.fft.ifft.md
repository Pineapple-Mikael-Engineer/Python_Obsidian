---
title: scipy.fft.ifft — transformada inversa de Fourier 1D (reconstruye la señal)
aliases:
  - ifft
  - scipy.fft.ifft
  - transformada inversa de fourier
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

# scipy.fft.ifft — transformada inversa de Fourier 1D (reconstruye la señal)

Calcula la **DFT inversa**: reconstruye la señal en el dominio del tiempo a partir de su espectro. Es la operacion opuesta a `fft`, de modo que `ifft(fft(x)) ≈ x` salvo error numerico de punto flotante. Recibe el espectro complejo y devuelve un **array complejo** del mismo tamaño; cuando ese espectro provenia de una **señal real**, la parte imaginaria de la salida es practicamente cero (residuo numerico ~1e-16), por lo que suele tomarse `np.real`.

> Convencion: con `norm='backward'` (por defecto) `ifft` aplica el factor `1/n`; `fft` no escala. Por eso ambas componen la identidad. Si se cambia `norm` en una, hay que usar el mismo en la otra.

## Firma

```python
scipy.fft.ifft(
    x,              # array_like: espectro a invertir (complejo)
    n=None,         # int | None: longitud de la transformada (padding/truncado)
    axis=-1,        # int: eje sobre el que transformar
    norm=None,      # str | None: 'backward' (def) | 'ortho' | 'forward'
    overwrite_x=False,  # bool: permite sobrescribir x
    workers=None,   # int | None: hilos para paralelizar
    plan=None,      # objeto plan (avanzado)
) -> ndarray  # complejo
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `ndarray` complejo | misma que `x` (o con `n` en `axis`) | Señal reconstruida en el dominio del tiempo |

```python
x_rec = ifft(X)        # señal reconstruida (compleja)
np.real(x_rec)         # parte util si el espectro venia de señal real
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Reconstruir desde el espectro | `ifft(X)` |
| Tras filtrar en frecuencia | `ifft(X_filtrado)` |
| Con la misma normalizacion que la directa | `ifft(X, norm='ortho')` |
| A lo largo de un eje | `ifft(M, axis=0)` |

## Parametros en detalle

### `x` (obligatorio)

El espectro complejo a invertir, tipicamente la salida de `fft` (posiblemente modificada). El orden de las frecuencias debe seguir la convencion de `fftfreq` (DC, positivas, negativas); no aplicar `fftshift` antes de invertir.

```python
import numpy as np
from scipy.fft import fft, ifft

x = np.array([1.0, 2.0, 3.0, 4.0])
X = fft(x)
x_rec = ifft(X)
np.allclose(x_rec.real, x)   # → True   (ifft(fft(x)) ≈ x)
np.max(np.abs(x_rec.imag))   # → ~1e-16  (residuo numerico)
```

### `n`

Longitud de la inversa. Con `n` mayor hace zero-padding del espectro; con menor lo trunca. Por defecto usa la longitud de `x` sobre `axis`.

### `norm`

Debe coincidir con el usado en la transformada directa para recuperar la señal a la escala correcta. Con `'backward'` (def) `ifft` divide por `n`; con `'forward'` no escala; con `'ortho'` divide por `√n`.

### `workers`

Numero de hilos para paralelizar inversiones independientes; `workers=-1` usa todos los nucleos.

## Casos de uso

### Filtrado en el dominio de la frecuencia

El flujo clasico es `fft` para pasar a frecuencia, anular o atenuar los bins no deseados y `ifft` para volver al tiempo. Aqui se elimina una componente de alta frecuencia (ruido) y se reconstruye la señal limpia.

```python
import numpy as np
from scipy.fft import fft, ifft, fftfreq

fs = 500
t = np.arange(0, 1, 1/fs)
señal = np.sin(2*np.pi*5*t)               # señal util a 5 Hz
ruido = 0.6*np.sin(2*np.pi*120*t)        # ruido a 120 Hz
x = señal + ruido

X = fft(x)
freqs = fftfreq(len(x), d=1/fs)
X[np.abs(freqs) > 30] = 0                 # filtro paso-bajo brusco
x_limpio = ifft(X).real                   # señal reconstruida sin ruido
```

### Verificar reconstruccion exacta

```python
np.allclose(ifft(fft(x)), x)   # → True
```

## Buenas practicas

1. Toma `np.real(ifft(...))` cuando el espectro provino de una señal real: descarta el residuo imaginario.
2. Usa el **mismo `norm`** en `fft` e `ifft`; mezclarlos cambia la escala del resultado.
3. No apliques `fftshift` al espectro antes de invertir; `ifft` espera el orden nativo de `fftfreq`.
4. Para señales reales considera el par `rfft`/`irfft`: mas eficiente y `irfft` devuelve real directamente.
5. Al filtrar, modifica de forma simetrica las frecuencias positivas y negativas para que la salida siga siendo real.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Salida con parte imaginaria grande | Filtrado asimetrico del espectro | Anular bins en pares `±f` simetricos |
| Amplitud reconstruida erronea | `norm` distinto en fft e ifft | Usar el mismo `norm` en ambas |
| Señal "desordenada" tras invertir | `fftshift` aplicado antes de `ifft` | Invertir sobre el orden nativo de `fftfreq` |
| Comparacion `==` falla | Error de punto flotante | Usar `np.allclose`, no igualdad exacta |
| Esperar salida real | `ifft` siempre devuelve complejo | Tomar `.real` o usar `irfft` |

## Limitaciones

- Devuelve **siempre** complejo; para señales reales `irfft` es mas directo y eficiente.
- La reconstruccion es exacta solo hasta el epsilon de punto flotante, no bit a bit.
- Filtrar poniendo bins a cero produce ondulaciones (efecto Gibbs); para filtros suaves usar diseño de filtros de `scipy.signal`.

## Notas relacionadas

- [[scipy.fft.fft]]
- [[scipy.fft.rfft]]
- [[scipy.fft.fftfreq]]
- [[concepto_relacion_numpy]]
