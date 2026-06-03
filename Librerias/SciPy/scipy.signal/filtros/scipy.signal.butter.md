---
title: scipy.signal.butter — disenia un filtro Butterworth (no lo aplica)
aliases:
  - butter
  - scipy.signal.butter
  - filtro butterworth
tags:
  - scipy
  - api/funcion
  - procesamiento-senales
lib: scipy
tipo: funcion
mod: scipy.signal
retorna: tuple (b, a) o ndarray sos
requiere:
  - numpy
draft: false
---

# scipy.signal.butter — disenia un filtro Butterworth (no lo aplica)

**Disenia** un filtro Butterworth y devuelve sus **coeficientes**; no toca la señal. El filtro Butterworth se caracteriza por una respuesta en frecuencia **maximamente plana en la banda de paso** (sin rizado), a cambio de una transicion mas suave hacia la banda de rechazo. La funcion solo calcula el filtro a partir del orden `N` y la frecuencia de corte `Wn`; quien filtra de verdad es `filtfilt` o `lfilter`, que reciben estos coeficientes.

> Flujo central del procesamiento de señales: **`butter` DISEÑA → `filtfilt`/`lfilter` APLICAN**. Separar diseño y aplicacion permite reutilizar el mismo filtro sobre muchas señales y elegir como aplicarlo (fase cero offline o causal en tiempo real).

## Firma

```python
scipy.signal.butter(
    N,                 # int: orden del filtro (mas orden -> transicion mas abrupta)
    Wn,                # float | [f1, f2]: frecuencia(s) de corte
    btype='low',       # str: 'low' | 'high' | 'band' | 'bandstop'
    analog=False,      # bool: False -> filtro digital; True -> analogico
    output='ba',       # str: 'ba' (b, a) | 'sos' (RECOMENDADO) | 'zpk'
    fs=None            # float: frecuencia de muestreo; si se da, Wn va en Hz
) -> tuple | ndarray
```

## Valor de retorno

| `output` | Devuelve | Significado |
|----------|----------|-------------|
| `'ba'` (defecto) | `(b, a)` | Dos arrays: coeficientes del numerador `b` y denominador `a` |
| `'sos'` | `sos` | Array `(n_secciones, 6)`: secciones de segundo orden, estable |
| `'zpk'` | `(z, p, k)` | Ceros, polos y ganancia |

```python
sos = butter(4, 0.2, output='sos')   # diseño recomendado
b, a = butter(4, 0.2)                 # forma clasica (b, a)
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Pasa-bajos, corte normalizado | `butter(4, 0.2)` |
| Pasa-altos | `butter(4, 0.1, btype='high')` |
| Pasa-banda | `butter(4, [0.1, 0.4], btype='band')` |
| Rechaza-banda (notch ancho) | `butter(4, [0.45, 0.55], btype='bandstop')` |
| Con frecuencia de muestreo en Hz | `butter(4, 50, fs=1000)` |
| Salida sos (estable) | `butter(8, 0.2, output='sos')` |

## Parametros en detalle

### `N` (obligatorio)

Orden del filtro. A mayor orden, la transicion entre banda de paso y rechazo es mas abrupta (filtro mas selectivo), pero crece el coste y la fragilidad numerica en formato `ba`. Ordenes altos (≳ 8) deben usar `output='sos'` para no degradarse.

### `Wn` (obligatorio)

Frecuencia(s) de corte. Su interpretacion depende de `fs`:

- **Sin `fs`**: normalizada en `0-1`, donde `1` es la frecuencia de Nyquist (mitad de la de muestreo). Una señal a 1000 Hz tiene Nyquist en 500 Hz, asi que `Wn=0.2` equivale a 100 Hz.
- **Con `fs`**: se interpreta directamente en **Hz**.

Para `btype='band'` o `'bandstop'`, `Wn` debe ser una pareja `[f_baja, f_alta]`.

```python
import numpy as np
from scipy.signal import butter

# Corte a 100 Hz en una señal muestreada a 1000 Hz, dos formas equivalentes:
sos1 = butter(4, 0.2, output='sos')           # normalizado: 100/500 = 0.2
sos2 = butter(4, 100, fs=1000, output='sos')  # en Hz, pasando fs
np.allclose(sos1, sos2)   # → True
```

### `btype`

Tipo de respuesta: `'low'` (deja pasar bajas frecuencias), `'high'` (altas), `'band'` (una banda intermedia) y `'bandstop'` (rechaza una banda). Los dos ultimos exigen `Wn=[f1, f2]`.

### `output`

Formato de los coeficientes devueltos:

- `'ba'` (defecto): coeficientes `b, a` de la funcion de transferencia. Comodo pero **numericamente fragil** en orden alto (los polos se acumulan y se pierden cifras).
- `'sos'`: cascada de secciones de segundo orden. **Recomendado** por estabilidad numerica; se aplica con `sosfilt` o `sosfiltfilt`.

```python
# En orden alto, 'ba' puede volverse inestable; 'sos' lo evita
sos = butter(10, 0.3, output='sos')
sos.shape   # → (5, 6)   (10/2 = 5 secciones de segundo orden)
```

### `fs`

Frecuencia de muestreo en Hz. Si se proporciona, `Wn` se especifica en Hz en vez de normalizado, lo que suele ser mas legible. Internamente SciPy hace la normalizacion contra Nyquist.

### `analog`

`False` (defecto) disenia un filtro **digital** (el caso habitual al trabajar con señales muestreadas). `True` produce un filtro analogico continuo (uso teorico o de diseño de hardware).

## Casos de uso

### Pasa-bajos para quitar ruido de alta frecuencia de un sensor

```python
import numpy as np
from scipy.signal import butter, sosfiltfilt

fs = 1000.0                                   # Hz, muestreo del sensor
t = np.arange(0, 1.0, 1/fs)
limpio = np.sin(2*np.pi*5*t)                  # señal util a 5 Hz
ruido  = 0.4*np.sin(2*np.pi*120*t)            # interferencia a 120 Hz
x = limpio + ruido

sos = butter(4, 30, btype='low', fs=fs, output='sos')  # corte a 30 Hz
y = sosfiltfilt(sos, x)                       # aqui se APLICA el filtro
# y conserva los 5 Hz y atenua los 120 Hz
```

### Pasa-altos para eliminar la deriva de linea base de un ECG

```python
# La deriva de linea base es una oscilacion muy lenta (< 0.5 Hz)
sos = butter(2, 0.5, btype='high', fs=500, output='sos')
# luego: ecg_sin_deriva = sosfiltfilt(sos, ecg)
```

### Pasa-banda para aislar una banda de vibracion mecanica

```python
# Aislar energia entre 50 y 150 Hz de un acelerometro a 2 kHz
sos = butter(6, [50, 150], btype='band', fs=2000, output='sos')
```

## Buenas practicas

1. Usa `output='sos'` por defecto, sobre todo con `N` mayor que 4; evita inestabilidad numerica.
2. Pasa `fs` y expresa `Wn` en Hz: es mas legible y menos propenso a errores que normalizar a mano.
3. Recuerda que `butter` **solo disenia**: necesitas `filtfilt`/`sosfiltfilt` (offline) o `lfilter`/`sosfilt` (causal) para filtrar.
4. Sube el orden con cautela; un orden alto da mas selectividad pero tambien mas ringing y retardo de grupo.
5. Para diseño de pasa-banda, ordena `Wn=[f_baja, f_alta]` con `f_baja < f_alta` y ambas por debajo de Nyquist.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| La señal no cambia | Se diseño el filtro pero nunca se aplico | Pasar `sos`/`(b,a)` a `sosfiltfilt`/`filtfilt`/`lfilter` |
| `ValueError: Wn ... must be ... 0 and 1` | `Wn` normalizado fuera de `(0, 1)` sin `fs` | Normalizar contra Nyquist o pasar `fs` y usar Hz |
| Banda diseña mal o lanza error | `btype='band'` con `Wn` escalar | Usar `Wn=[f1, f2]` para band/bandstop |
| Filtro inestable en orden alto | `output='ba'` acumula error numerico | Usar `output='sos'` |
| Resultado raro al filtrar | Confundir normalizado y Hz | Ser coherente: o todo normalizado, o todo con `fs` |

## Limitaciones

- No filtra: solo calcula coeficientes; la aplicacion es un paso aparte.
- El formato `'ba'` pierde precision numerica en ordenes altos; preferir `'sos'`.
- Butterworth prioriza planitud en banda de paso a costa de una transicion mas lenta; si necesitas transicion mas abrupta considera Chebyshev (`cheby1`/`cheby2`) o eliptico (`ellip`).
- `Wn` siempre se referencia a Nyquist; un corte cerca de Nyquist puede comportarse mal.

## Notas relacionadas

- [[scipy.signal.filtfilt]]
- [[scipy.signal.lfilter]]
- [[scipy.signal.sosfiltfilt]]
- [[concepto_relacion_numpy]]
