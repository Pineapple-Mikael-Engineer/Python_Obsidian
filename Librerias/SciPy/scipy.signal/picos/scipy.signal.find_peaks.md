---
title: scipy.signal.find_peaks — deteccion y filtrado de picos en una senal 1D
aliases:
  - find_peaks
  - scipy.signal.find_peaks
  - deteccion de picos
tags:
  - scipy
  - api/funcion
  - procesamiento-senales
lib: scipy
tipo: funcion
mod: scipy.signal
retorna: tuple (ndarray, dict)
requiere:
  - numpy
draft: false
---

# scipy.signal.find_peaks — deteccion y filtrado de picos en una senal 1D

Detecta los **maximos locales** (picos) de una senal **1D** —puntos mayores que sus dos vecinos inmediatos— y los **filtra** segun criterios opcionales (altura, separacion, prominencia, anchura). Devuelve una **tupla** `(peaks, properties)`: `peaks` es el array de **indices** de los picos que pasan los filtros y `properties` es un `dict` con las propiedades calculadas (`peak_heights`, `prominences`, `widths`, ...). Es la herramienta estandar para contar eventos o localizar maximos relevantes ignorando el ruido.

> El parametro mas robusto es **`prominence`**: mide cuanto **sobresale** un pico respecto a su entorno (la caida minima a ambos lados antes de subir mas alto). A diferencia de `height`, que mira la altura absoluta, la prominencia distingue picos reales de pequenas ondulaciones del ruido aunque esten en zonas altas de la senal.

## Firma

```python
scipy.signal.find_peaks(
    x,                   # array_like 1D: senal de entrada
    height=None,         # float | (min,max) | array: altura absoluta minima (y/o maxima)
    threshold=None,      # float | (min,max): desnivel minimo respecto a los vecinos INMEDIATOS
    distance=None,       # float >=1: separacion minima entre picos, en muestras
    prominence=None,     # float | (min,max): prominencia minima (cuanto sobresale del entorno)
    width=None,          # float | (min,max): anchura minima del pico, en muestras
    wlen=None,           # int: ventana para acotar el calculo de prominencia
    rel_height=0.5,      # float: altura relativa a la que se mide width
    plateau_size=None,   # float | (min,max): tamano de mesetas planas admitidas
) -> tuple
```

## Valor de retorno

| Posicion | Tipo | Significado |
|----------|------|-------------|
| `[0]` | `ndarray` | `peaks`: indices (posiciones en `x`) de los picos que superan los filtros |
| `[1]` | `dict` | `properties`: propiedades calculadas (`peak_heights`, `prominences`, `widths`, `left_bases`, ...), solo de los criterios usados |

```python
peaks, props = find_peaks(x, prominence=1)
x[peaks]          # alturas de los picos detectados
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Todos los maximos locales | `find_peaks(x)` |
| Filtrar por altura absoluta | `find_peaks(x, height=2.0)` |
| Separacion minima entre picos | `find_peaks(x, distance=10)` |
| Ignorar ruido por prominencia | `find_peaks(x, prominence=0.5)` |
| Combinar criterios | `find_peaks(x, height=1, distance=20, prominence=0.5)` |
| Contar picos detectados | `len(find_peaks(x, prominence=1)[0])` |

## Parametros en detalle

### `x` (obligatorio)

Senal **unidimensional**. Solo detecta maximos **estrictos** frente a los vecinos inmediatos (con `plateau_size` se admiten mesetas). Los extremos del array nunca se consideran picos. Para detectar **minimos**, aplicar `find_peaks(-x)`.

```python
import numpy as np
from scipy.signal import find_peaks

x = np.array([0, 2, 1, 3, 1, 0, 4, 0])
peaks, _ = find_peaks(x)
peaks    # → [1 3 6]   (indices de los maximos locales)
```

### `height`

Altura **absoluta** minima (o rango `(min, max)`). Filtra por el valor de `x` en el pico. Util cuando la linea base es estable, pero **fragil** si la senal tiene deriva: un pico pequeno sobre una zona alta puede colarse y uno grande en zona baja quedar fuera.

```python
peaks, props = find_peaks(x, height=2.5)
peaks                  # → [3 6]
props['peak_heights']  # → [3. 4.]
```

### `distance`

Separacion **minima en muestras** entre picos (`>= 1`). Cuando dos picos estan mas cerca, se conserva el **mas alto**. Ideal para evitar detecciones multiples sobre un mismo evento ancho.

```python
peaks, _ = find_peaks(x, distance=3)   # fuerza >=3 muestras entre picos
```

### `prominence`

**Prominencia** minima: cuanto sobresale el pico de su entorno, medida como la altura sobre la menor de las dos "cuencas" que lo rodean antes de encontrar un pico mas alto. Es el filtro **mas robusto** frente al ruido y a la deriva de la linea base, porque mide forma local en vez de nivel absoluto. `wlen` limita la ventana de busqueda y acelera el calculo en senales largas.

```python
ruido = np.random.randn(1000) * 0.1
senal = ruido.copy()
senal[200] += 3        # pico real y prominente
peaks, props = find_peaks(senal, prominence=1)
peaks                  # → [200]   (el ruido de prominencia <1 se descarta)
props['prominences']   # → [~3.0]
```

### `width`

Anchura minima del pico **en muestras**, medida por defecto a media altura relativa (`rel_height=0.5`). Filtra picos demasiado estrechos (a menudo artefactos) y rellena `properties` con `widths`, `width_heights`, `left_ips`, `right_ips`.

### `threshold`

Desnivel minimo respecto a los vecinos **inmediatos** (solo las dos muestras contiguas). No confundir con `prominence`, que considera todo el entorno: `threshold` es un criterio muy local y rara vez es el mas adecuado para separar senal de ruido.

## Casos de uso

### Contar eventos en una senal

Numero de latidos, pulsos o picos relevantes en un registro.

```python
import numpy as np
from scipy.signal import find_peaks

t = np.linspace(0, 4 * np.pi, 1000)
señal = np.sin(t) + 0.05 * np.random.randn(1000)
peaks, _ = find_peaks(señal, prominence=0.5)
len(peaks)    # → ~2   (los maximos del seno, sin contar el ruido)
```

### Detectar maximos relevantes ignorando ruido

Combinar prominencia (robustez) con distancia (un pico por evento).

```python
peaks, props = find_peaks(señal, prominence=0.5, distance=50)
señal[peaks]          # alturas de los picos validos
props['prominences']  # cuanto sobresale cada uno
```

## Buenas practicas

1. Empieza por **`prominence`**: es el filtro que mejor separa picos reales del ruido y de la deriva de la linea base.
2. Anade **`distance`** para garantizar un solo pico por evento cuando los picos son anchos o vienen en racimos.
3. Reserva **`height`** para cuando la linea base sea estable y conozcas un umbral fisico claro.
4. Detecta **minimos** invirtiendo la senal: `find_peaks(-x)`.
5. Inspecciona el `dict` `properties` (`prominences`, `widths`) para **calibrar** los umbrales de forma cuantitativa en lugar de a ojo.
6. En senales largas, fija `wlen` para acotar el calculo de prominencia y ganar velocidad.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Tratar el retorno como un solo array | Devuelve `(peaks, properties)` | Desempaquetar: `peaks, props = find_peaks(...)` |
| Demasiados picos espurios | Sin filtros o solo `height` con ruido | Usar `prominence` (y opcionalmente `distance`) |
| `properties` vacio para una clave | Esa propiedad solo se calcula si se filtra por ella | Pasar el criterio (`prominence=`, `width=`) para poblarla |
| Picos en los bordes no detectados | Los extremos nunca son picos | Hacer padding o tratar los bordes aparte |
| No detecta minimos | `find_peaks` solo busca maximos | Invertir la senal: `find_peaks(-x)` |
| Mesetas planas ignoradas | Por defecto exige maximo estricto | Usar `plateau_size` para admitir mesetas |

## Limitaciones

- Solo opera sobre senales **1D**; para datos 2D / imagenes hay que recurrir a otras tecnicas.
- Detecta exclusivamente **maximos locales**; minimos requieren invertir la senal.
- No suaviza la senal: sobre datos muy ruidosos conviene filtrar antes (media movil, filtro paso bajo) para que la prominencia sea fiable.
- Los picos en los extremos del array nunca se reportan, aunque sean los mayores.

## Notas relacionadas

- [[scipy.signal.convolve]]
- [[scipy.signal.correlate]]
- [[concepto_objetos_resultado]]
