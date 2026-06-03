---
title: scipy.signal.filtfilt — aplica un filtro con fase cero (ida y vuelta)
aliases:
  - filtfilt
  - scipy.signal.filtfilt
  - filtrado fase cero
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
  - scipy.signal.butter
draft: false
---

# scipy.signal.filtfilt — aplica un filtro con fase cero (ida y vuelta)

**Aplica** a la señal `x` un filtro ya diseñado (coeficientes `b, a`), pasandolo **hacia adelante y luego hacia atras**. El resultado tiene **fase cero**: no desplaza la señal en el tiempo, asi que los picos, flancos y eventos quedan alineados con la señal original. Como filtra dos veces, el **orden efectivo se duplica** y la atenuacion tambien. Esto exige conocer toda la señal de antemano, por lo que `filtfilt` es la herramienta de **procesamiento offline** (en lote, no en streaming).

> Recibe los coeficientes que produce `butter`; no disenia nada. Para el formato `sos` usa su variante `sosfiltfilt`, mas estable. Contrasta con `lfilter`, que filtra una sola vez y **si** introduce retardo de fase.

## Firma

```python
scipy.signal.filtfilt(
    b,                 # array: coeficientes del numerador (de butter)
    a,                 # array: coeficientes del denominador (de butter)
    x,                 # array: señal de entrada a filtrar
    axis=-1,           # int: eje a lo largo del cual se filtra
    padtype='odd',     # str | None: 'odd' | 'even' | 'constant' | None
    padlen=None,       # int | None: longitud del padding en los bordes
    method='pad',      # str: 'pad' (defecto) | 'gust' (metodo de Gustafsson)
    irlen=None         # int | None: longitud de respuesta impulsiva (con 'gust')
) -> ndarray
```

## Valor de retorno

| Tipo | Significado |
|------|-------------|
| `ndarray` | Señal filtrada, **misma forma** que `x`, alineada en el tiempo (fase cero) |

```python
y = filtfilt(b, a, x)   # y.shape == x.shape
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Filtrado fase cero basico | `filtfilt(b, a, x)` |
| Filtrar por columnas de una matriz | `filtfilt(b, a, X, axis=0)` |
| Controlar el padding de bordes | `filtfilt(b, a, x, padlen=50)` |
| Sin padding (señal corta) | `filtfilt(b, a, x, padtype=None)` |
| Equivalente con formato sos | `sosfiltfilt(sos, x)` |

## Parametros en detalle

### `b`, `a` (obligatorios)

Coeficientes del filtro, tal cual los devuelve `butter` con `output='ba'`. `b` es el numerador y `a` el denominador de la funcion de transferencia. Si diseñaste con `output='sos'`, no uses `filtfilt`: usa `sosfiltfilt`.

```python
import numpy as np
from scipy.signal import butter, filtfilt

fs = 1000.0
t = np.arange(0, 1.0, 1/fs)
x = np.sin(2*np.pi*5*t) + 0.5*np.sin(2*np.pi*150*t)

b, a = butter(4, 30, btype='low', fs=fs)   # DISEÑO
y = filtfilt(b, a, x)                       # APLICACION fase cero
# y mantiene los 5 Hz alineados en el tiempo; atenua los 150 Hz
```

### `x` (obligatorio)

Señal de entrada. Debe ser lo bastante larga respecto al `padlen` por defecto (`3 * max(len(a), len(b))`); señales muy cortas obligan a reducir `padlen` o usar `padtype=None`.

### `axis`

Eje sobre el que se filtra cuando `x` es multidimensional. Por defecto `-1` (ultimo eje). Para una matriz de señales en columnas, `axis=0` filtra cada columna.

### `padtype`, `padlen`

Controlan el **padding** que se añade en los bordes antes de filtrar, para reducir los transitorios de arranque. `padtype='odd'` (defecto) refleja la señal de forma impar; `None` desactiva el padding. `padlen` fija cuantas muestras se extienden; reducelo si la señal es corta.

### `method`

`'pad'` (defecto) usa extension de bordes. `'gust'` aplica el metodo de Gustafsson, que maneja las condiciones iniciales sin extender la señal; util en señales muy cortas.

## Casos de uso

### Suavizar la lectura de un sensor sin desfasar los eventos

```python
import numpy as np
from scipy.signal import butter, filtfilt

fs = 200.0                                    # Hz
b, a = butter(3, 10, btype='low', fs=fs)      # pasa-bajos a 10 Hz
lectura_suave = filtfilt(b, a, lectura_ruidosa)
# los maximos quedan en el MISMO instante que en la señal cruda (fase cero)
```

### Eliminar deriva y red electrica de un ECG offline

```python
# ECG ya grabado completo en disco -> procesamiento offline ideal para filtfilt
b, a = butter(2, [0.5, 40], btype='band', fs=500)
ecg_filtrado = filtfilt(b, a, ecg)
```

### Filtrar varias señales (canales) a la vez

```python
# X: matriz (n_muestras, n_canales); filtrar cada canal por columnas
b, a = butter(4, 0.2)
Y = filtfilt(b, a, X, axis=0)
```

## Buenas practicas

1. Reserva `filtfilt` para **procesamiento offline**, cuando tengas la señal completa; es la mayor ventaja de la fase cero.
2. Si diseñaste con `output='sos'`, usa `sosfiltfilt` en lugar de `filtfilt`: mas estable en orden alto.
3. Recuerda que el orden efectivo se **duplica**; disenia el filtro pensando en ello (un orden 4 actua como orden 8).
4. Para señales cortas, baja `padlen` o usa `padtype=None`/`method='gust'` para evitar errores de longitud.
5. No la uses en tiempo real: necesita datos futuros (el paso hacia atras), lo que es imposible en streaming.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `The length of the input vector x must be greater than padlen` | Señal mas corta que el padding | Bajar `padlen`, usar `padtype=None` o `method='gust'` |
| Esperaba retardo y la señal sale alineada | `filtfilt` es fase cero por diseño | Si quieres retardo causal, usar `lfilter` |
| Inestabilidad con orden alto | Coeficientes `ba` mal condicionados | Diseñar con `sos` y usar `sosfiltfilt` |
| Atenuacion mayor de la esperada | El filtrado doble duplica el orden efectivo | Diseñar con la mitad del orden objetivo |
| Filtra el eje equivocado en 2D | `axis` por defecto es `-1` | Pasar `axis` explicito (p. ej. `axis=0`) |

## Limitaciones

- **No sirve para tiempo real ni streaming**: el paso hacia atras requiere conocer toda la señal.
- Duplica el orden efectivo y la atenuacion; hay que tenerlo en cuenta al diseñar.
- Con `output='sos'` no es la herramienta adecuada: usar `sosfiltfilt`.
- Los bordes pueden tener transitorios residuales si el padding no es adecuado.

## Notas relacionadas

- [[scipy.signal.butter]]
- [[scipy.signal.lfilter]]
- [[scipy.signal.sosfiltfilt]]
