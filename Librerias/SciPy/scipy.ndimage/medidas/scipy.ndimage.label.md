---
title: scipy.ndimage.label — etiquetado de componentes conexas
aliases:
  - label
  - scipy.ndimage.label
  - componentes conexas
tags:
  - scipy
  - api/funcion
  - procesamiento-imagen
lib: scipy
tipo: funcion
mod: scipy.ndimage
retorna: tuple (ndarray, int)
requiere:
  - numpy
draft: false
---

# scipy.ndimage.label — etiquetado de componentes conexas

Identifica las **componentes conexas** de una mascara: a cada region de pixeles no nulos conectados entre si le asigna un **entero unico** (1, 2, 3, ...), dejando el fondo en `0`. Devuelve una **tupla** `(labeled_array, num_features)`: el array etiquetado (mismo tamaño que la entrada) y el **numero de regiones** encontradas. Es la **base del flujo de analisis de regiones**: primero se etiqueta, luego se mide cada objeto por su etiqueta.

> El resultado es una **tupla**, no un solo array. Lo correcto es desempaquetar: `labeled, n = label(mask)`. Tratar el retorno como un unico array es el error mas frecuente.

## Firma

```python
scipy.ndimage.label(
    input,             # array_like: mascara (los pixeles no nulos forman las regiones)
    structure=None,    # ndarray bool: define la conectividad (def: 4-vecinos en 2D)
    output=None,       # ndarray|dtype: destino opcional para el array etiquetado
) -> tuple
```

## Valor de retorno

| Posicion | Tipo | Significado |
|----------|------|-------------|
| `[0]` | `ndarray` (int) | `labeled_array`: cada region conexa marcada con un entero unico (1..n); fondo = 0 |
| `[1]` | `int` | `num_features`: numero de regiones (componentes conexas) detectadas |

```python
labeled, n = label(mask)
n                  # → numero de objetos
labeled.max()      # → n  (la etiqueta mas alta coincide con el conteo)
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Etiquetar con conectividad por defecto (4-vecinos) | `label(mask)` |
| Conectividad diagonal (8-vecinos) | `label(mask, structure=np.ones((3,3)))` |
| Contar objetos | `label(mask)[1]` |
| Solo el array etiquetado | `labeled, _ = label(mask)` |

## Parametros en detalle

### `input` (obligatorio)

Mascara de entrada. **Todo pixel no nulo** es primer plano; los `0` son fondo. Dos pixeles pertenecen a la misma region si estan conectados segun la conectividad definida por `structure`.

```python
import numpy as np
from scipy.ndimage import label

mask = np.array([[1,1,0,0,1],
                 [1,0,0,0,1],
                 [0,0,1,0,0],
                 [0,0,1,1,0]])
labeled, n = label(mask)
n                 # → 3   (tres regiones separadas)
labeled
# [[1 1 0 0 2]
#  [1 0 0 0 2]
#  [0 0 3 0 0]
#  [0 0 3 3 0]]
```

### `structure`

Define la **conectividad**: que vecinos cuentan como "tocandose". Por defecto es la conectividad-1 (en 2D, **4-vecinos**: arriba/abajo/izquierda/derecha; las diagonales NO conectan). Pasar `np.ones((3,3))` activa la conectividad-2 (**8-vecinos**, incluye diagonales), que une regiones que solo se rozan en una esquina. La eleccion cambia el **conteo** de objetos.

```python
from scipy.ndimage import generate_binary_structure
diag = generate_binary_structure(2, 2)   # 8-vecinos
label(mask, structure=diag)[1]           # puede dar menos regiones que con 4-vecinos
```

### `output`

Array (o `dtype`) destino donde escribir el etiquetado, para reutilizar memoria o forzar el tipo entero. Opcional.

## Casos de uso

### Contar objetos en una mascara binaria

Despues de limpiar el ruido con morfologia, `label` cuenta cuantas regiones quedan.

```python
import numpy as np
from scipy.ndimage import label

m = np.zeros((5,5), dtype=int)
m[0:2,0:2] = 1     # objeto A
m[3:5,3:5] = 1     # objeto B
labeled, n = label(m)
n                  # → 2
```

### Etiquetar y luego medir cada region

`label` es el primer paso del flujo de medidas: una vez etiquetadas las regiones, se pasan `labeled` e `index` a funciones como `center_of_mass`, `sum` o `mean` para medir cada objeto por separado.

```python
from scipy.ndimage import center_of_mass, sum as ndi_sum
labeled, n = label(m)
idx = range(1, n + 1)
centros = center_of_mass(m, labeled, index=idx)   # centroide de cada region
areas   = ndi_sum(m, labeled, index=idx)          # tamaño de cada region
```

## Buenas practicas

1. **Desempaqueta siempre** el retorno: `labeled, n = label(mask)`.
2. Usa `range(1, n + 1)` como `index` para iterar las regiones (las etiquetas empiezan en 1, no en 0).
3. Limpia la mascara con morfologia (apertura) **antes** de etiquetar para no contar motas de ruido como objetos. Esto se hace con la erosion y dilatacion binarias.
4. Elige la conectividad (`structure`) segun el problema: 8-vecinos une objetos que se tocan en diagonal; 4-vecinos los mantiene separados.
5. El array etiquetado encaja directamente como argumento `labels` de las funciones de medida del modulo.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Tratar el retorno como un solo array | Devuelve `(labeled_array, num_features)` | Desempaquetar: `labeled, n = label(mask)` |
| Cuenta mas/menos objetos de lo esperado | Conectividad por defecto (4-vecinos) ignora diagonales | Pasar `structure=np.ones((3,3))` para 8-vecinos |
| El ruido se cuenta como objetos | Mascara sin limpiar | Aplicar apertura morfologica antes de etiquetar |
| `index` empieza en 0 y falla | La etiqueta 0 es el fondo | Usar `range(1, n + 1)` |
| Pierde regiones validas | Mascara mal umbralizada | Revisar el umbral que genera la mascara |

## Limitaciones

- Solo etiqueta por **conexion espacial**; no separa objetos que se tocan (para eso hace falta watershed u otras tecnicas).
- La numeracion **no es estable** entre ejecuciones con mascaras distintas: las etiquetas se asignan por orden de barrido, no por tamaño ni posicion fija.
- No mide nada por si misma: solo asigna etiquetas; las magnitudes (centroide, area, intensidad) se calculan con las funciones de medida.
- El significado de `structure` cambia con la dimension del array (2D vs 3D).

## Notas relacionadas

- [[scipy.ndimage.center_of_mass]]
- [[scipy.ndimage.binary_erosion]]
