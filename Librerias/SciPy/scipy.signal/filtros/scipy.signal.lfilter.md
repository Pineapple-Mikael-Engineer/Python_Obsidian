---
title: scipy.signal.lfilter — aplica un filtro causal 1D (con retardo de fase)
aliases:
  - lfilter
  - scipy.signal.lfilter
  - filtrado causal
tags:
  - scipy
  - api/funcion
  - procesamiento-senales
lib: scipy
tipo: funcion
mod: scipy.signal
retorna: ndarray o tuple (y, zf)
requiere:
  - numpy
  - scipy.signal.butter
draft: false
---

# scipy.signal.lfilter — aplica un filtro causal 1D (con retardo de fase)

**Aplica** a la señal `x` un filtro digital ya diseñado (coeficientes `b, a`) en **forma directa II transpuesta**, recorriendo la señal una sola vez de principio a fin. Por ser **causal** (cada salida depende solo de muestras presentes y pasadas), introduce **retardo y distorsion de fase**: la señal filtrada queda desplazada en el tiempo. Esa misma causalidad lo hace apto para **procesamiento en tiempo real o por bloques (streaming)**, donde no se dispone de muestras futuras. Con el parametro de estado `zi` se puede filtrar una señal larga por trozos manteniendo continuidad.

> Recibe los coeficientes de `butter`; no disenia. Contrasta con `filtfilt`, que filtra ida y vuelta para lograr fase cero (sin retardo) pero necesita la señal completa. Para el formato `sos` usa su variante `sosfilt`.

## Firma

```python
scipy.signal.lfilter(
    b,                 # array: coeficientes del numerador (de butter)
    a,                 # array: coeficientes del denominador (de butter)
    x,                 # array: señal de entrada a filtrar
    axis=-1,           # int: eje a lo largo del cual se filtra
    zi=None            # array | None: estado inicial del filtro (para streaming)
) -> ndarray | tuple
```

## Valor de retorno

| Caso | Devuelve | Significado |
|------|----------|-------------|
| Sin `zi` | `y` | Señal filtrada (misma forma que `x`), con retardo de fase |
| Con `zi` | `(y, zf)` | Señal filtrada **y** estado final `zf`, para encadenar el siguiente bloque |

```python
y = lfilter(b, a, x)                # uso simple
y, zf = lfilter(b, a, x, zi=zi)     # uso con estado (streaming)
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Filtrado causal basico | `lfilter(b, a, x)` |
| Filtrar por columnas en 2D | `lfilter(b, a, X, axis=0)` |
| Con estado inicial (continuidad) | `lfilter(b, a, x, zi=zi)` |
| Estado inicial en reposo escalado | `zi = lfilter_zi(b, a) * x[0]` |
| Equivalente con formato sos | `sosfilt(sos, x)` |

## Parametros en detalle

### `b`, `a` (obligatorios)

Coeficientes del filtro, tal cual los devuelve `butter` con `output='ba'`. `a[0]` debe ser distinto de cero (SciPy normaliza por el si no es 1). Si diseñaste con `output='sos'`, usa `sosfilt` en su lugar.

```python
import numpy as np
from scipy.signal import butter, lfilter

fs = 1000.0
t = np.arange(0, 1.0, 1/fs)
x = np.sin(2*np.pi*5*t) + 0.5*np.sin(2*np.pi*150*t)

b, a = butter(4, 30, btype='low', fs=fs)   # DISEÑO
y = lfilter(b, a, x)                         # APLICACION causal
# y atenua los 150 Hz, pero los 5 Hz salen DESPLAZADOS en el tiempo (retardo)
```

### `x` (obligatorio)

Señal de entrada. A diferencia de `filtfilt`, no hay requisito de longitud minima: `lfilter` procesa muestra a muestra, asi que admite señales cortas y bloques pequeños.

### `axis`

Eje sobre el que se filtra cuando `x` es multidimensional. Por defecto `-1` (ultimo eje).

### `zi`

**Estado inicial** del filtro (las condiciones de retardo internas). Es la clave del filtrado por bloques: al pasar `zi`, la funcion devuelve tambien el estado final `zf`, que se alimenta como `zi` del siguiente bloque para que el resultado sea identico a filtrar la señal entera de una vez. Para arrancar sin transitorio brusco se inicializa con `lfilter_zi(b, a)` escalado por la primera muestra.

```python
import numpy as np
from scipy.signal import butter, lfilter, lfilter_zi

b, a = butter(3, 0.1)
zi = lfilter_zi(b, a) * senal[0]      # estado en reposo, escalado

# Filtrar por bloques (streaming) manteniendo continuidad
salida = []
for bloque in bloques:                 # cada bloque llega en tiempo real
    y, zi = lfilter(b, a, bloque, zi=zi)
    salida.append(y)
```

## Casos de uso

### Filtrado en tiempo real de un sensor por bloques

```python
import numpy as np
from scipy.signal import butter, lfilter, lfilter_zi

fs = 500.0
b, a = butter(4, 20, btype='low', fs=fs)   # pasa-bajos a 20 Hz
zi = lfilter_zi(b, a) * 0.0                  # arranque en reposo

def procesar(bloque):                        # se llama segun llega cada bloque
    global zi
    y, zi = lfilter(b, a, bloque, zi=zi)     # continuidad entre bloques
    return y
```

### Procesamiento causal cuando el retardo es aceptable

```python
# Si solo importa atenuar ruido y no la alineacion temporal exacta
b, a = butter(2, 0.15)
y = lfilter(b, a, ruidosa)
# mas barato que filtfilt: una sola pasada, pero introduce retardo de fase
```

### Comparar retardo frente a fase cero

```python
from scipy.signal import filtfilt
y_causal    = lfilter(b, a, x)    # desplazado en el tiempo (retardo)
y_fase_cero = filtfilt(b, a, x)   # alineado con x (sin retardo)
```

## Buenas practicas

1. Usa `lfilter` cuando necesites **causalidad**: tiempo real, streaming o simular un filtro fisico realizable.
2. Para filtrar señales largas por trozos, **propaga `zi`** entre bloques con `lfilter_zi`; asi evitas discontinuidades.
3. Si la alineacion temporal importa y tienes la señal completa, prefiere `filtfilt` (fase cero) en lugar de `lfilter`.
4. Con `output='sos'`, usa `sosfilt` por estabilidad numerica en orden alto.
5. Inicializa `zi` con `lfilter_zi(b, a) * x[0]` para arrancar sin un transitorio abrupto al inicio.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| La señal sale desplazada en el tiempo | `lfilter` es causal e introduce retardo de fase | Usar `filtfilt` si necesitas fase cero |
| Saltos entre bloques al filtrar por trozos | No se propago el estado `zi` | Reusar el `zf` devuelto como `zi` del siguiente bloque |
| `ValueError` por forma de `zi` | `zi` mal dimensionado | Construirlo con `lfilter_zi(b, a)` y escalar |
| Transitorio fuerte al inicio | Estado inicial en cero con señal no nula | Inicializar `zi = lfilter_zi(b, a) * x[0]` |
| Inestabilidad con orden alto | Coeficientes `ba` mal condicionados | Diseñar con `sos` y usar `sosfilt` |

## Limitaciones

- Introduce **retardo y distorsion de fase**: no preserva la posicion temporal de eventos.
- Filtra una sola vez; la atenuacion es la del orden diseñado (no se duplica como en `filtfilt`).
- Con `output='sos'` no es la herramienta adecuada: usar `sosfilt`.
- El manejo de continuidad por bloques recae en gestionar bien `zi`; un descuido produce discontinuidades.

## Notas relacionadas

- [[scipy.signal.butter]]
- [[scipy.signal.filtfilt]]
- [[scipy.signal.sosfilt]]
