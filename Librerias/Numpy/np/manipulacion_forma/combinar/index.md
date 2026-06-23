---
title: np/manipulacion_forma/combinar — unir arrays en uno
tags:
  - numpy
  - indice
draft: false
---

# np/manipulacion_forma/combinar — unir arrays en uno

Las seis funciones de esta carpeta toman varios arrays separados y los **fusionan en uno solo**. Todas devuelven una **copia**: no existe vista al combinar buffers de memoria independientes. Todo el grupo se entiende a través de una sola pregunta sobre el [[concepto_shape|shape]]: ¿el resultado tiene el **mismo número de ejes** que las entradas, o **uno más**?

## La distinción central: eje existente vs. eje nuevo

Es la división que organiza el grupo entero y la fuente más común de errores de shape en NumPy.

**[[np.concatenate]] hace crecer un eje que ya existe.** Los arrays deben tener el mismo `ndim` y coincidir en todos los ejes salvo en el de unión, cuya longitud se suma. El `ndim` no cambia:

$$
(n_0,\dots,a,\dots),(n_0,\dots,b,\dots)\;\xrightarrow{\ \text{axis}=p\ }\;(n_0,\dots,a+b,\dots)
$$

**[[np.stack]] inserta un eje nuevo.** Todos los arrays deben tener **exactamente el mismo shape**; aparece una dimensión de tamaño $r$ (el número de arrays). El `ndim` sube en 1:

$$
\underbrace{(n_0,\dots,n_{k-1}),\dots,(n_0,\dots,n_{k-1})}_{r\ \text{arrays}}\;\xrightarrow{\ \text{stack, axis}=p\ }\;(n_0,\dots,\overbrace{r}^{\text{nuevo}},\dots,n_{k-1})
$$

Dos vectores `(5,)`: con `concatenate` dan `(10,)` (mismo `ndim`, más elementos); con `stack` dan `(2, 5)` (aparece un eje). Elegir entre ellos es elegir si quieres el mismo número de ejes o uno más.

## Los atajos: concatenate/stack por un eje fijo

Las otras cuatro funciones son **atajos** de las dos base con el eje ya elegido (y, algunas, una promoción de dimensión automática). Saber a qué eje van es saber qué hacen.

| Función | Une por | ¿Eje nuevo? | Promoción / caso 1D | Equivale a |
|---|---|---|---|---|
| [[np.concatenate]] | eje libre (`axis`) | No | 1D concatena en eje 0 | — (es la base) |
| [[np.stack]] | eje **nuevo** | Sí (`ndim + 1`) | trata cada array como elemento | — (es la base) |
| [[np.vstack]] | eje 0 (filas) | No | 1D `(n,)` → fila `(1, n)` | `concatenate(axis=0)` |
| [[np.hstack]] | eje 1 (columnas); eje 0 en 1D | No | 1D se aplana en eje 0 | `concatenate(axis=1)` |
| [[np.dstack]] | eje 2 (profundidad) | No | 2D `(m,n)` → `(m, n, 1)` | `concatenate(axis=2)` |
| [[np.column_stack]] | eje 1 (columnas) | No | 1D `(n,)` → columna `(n, 1)` | `hstack` tras promover |

El detalle clave de los atajos es la **promoción de dimensión**: `vstack` convierte vectores en filas, `column_stack` los convierte en columnas, `dstack` los lleva a profundidad. Por eso resuelven casos que `concatenate` no resolvería sin un `reshape` previo.

## El requisito común: shapes compatibles

Combinar nunca inventa datos: exige que las formas encajen.

- **concatenate y los atajos por eje existente**: todos los shapes iguales **salvo en el eje de unión** (que se suma). Mismo `ndim`.
- **stack**: todos los shapes **idénticos** (es lo más estricto).

Si las formas no encajan, NumPy lanza un error de dimensiones antes de copiar nada.

## Guía de elección

| Situación | Función recomendada |
|---|---|
| Arrays con el mismo `ndim`, eje a elegir | [[np.concatenate]] |
| Construir un lote desde muestras de igual shape | [[np.stack]] |
| Añadir filas a una matriz | [[np.vstack]] |
| Añadir columnas (desde arrays 2D) | [[np.hstack]] |
| Construir una matriz desde vectores 1D | [[np.column_stack]] |
| Apilar imágenes o capas en profundidad | [[np.dstack]] |

## Ejemplo: construir una matriz de datos

```python
import numpy as np

tiempo = np.linspace(0, 1, 100)      # (100,)
senal = np.sin(2 * np.pi * tiempo)   # (100,)
ruido = np.random.randn(100)         # (100,)

# column_stack: cada vector 1D se convierte en una columna
datos = np.column_stack([tiempo, senal, ruido])   # (100, 3)

# Equivalente explícito con concatenate (hay que crear el eje de columna a mano):
datos2 = np.concatenate([
    tiempo.reshape(-1, 1),
    senal.reshape(-1, 1),
    ruido.reshape(-1, 1),
], axis=1)                                          # (100, 3)
```

## Notas relacionadas

- [[concepto_shape]] — qué shapes son compatibles al combinar
- [[concepto_axis_parametro]] — el eje que crece vs. el eje que se inserta
- [[np.split]] — la operación inversa (separar un array)
