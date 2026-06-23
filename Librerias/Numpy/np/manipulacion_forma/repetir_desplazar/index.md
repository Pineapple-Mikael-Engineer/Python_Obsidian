---
title: np/manipulacion_forma/repetir_desplazar — duplicar, rotar y rellenar elementos
tags:
  - numpy
  - indice
draft: false
---

# np/manipulacion_forma/repetir_desplazar — duplicar, rotar y rellenar elementos

Esta carpeta agrupa las funciones que **reorganizan los elementos** de un único array sin combinarlo
con otros: dos lo **agrandan duplicando datos** ([[np.repeat]], [[np.tile]]), una lo **agranda
rellenando** un borde ([[np.pad]]) y otra **conserva el tamaño rotando** los elementos ([[np.roll]]).
Todas devuelven un array nuevo (copia); ninguna modifica la entrada.

El grupo existe porque estos patrones aparecen sin parar en simulación, procesado de señales y visión
por computador: construir un kernel repetido, expandir una secuencia corta, dar margen a una imagen
antes de convolucionar o implementar correlación circular.

## La distinción clave: repeat vs tile (elemento vs bloque)

Las dos funciones que duplican lo hacen en **unidades distintas**, y confundirlas da resultados que
*parecen* correctos pero significan otra cosa:

$$ [\,1,2,3\,] \;\xrightarrow{\ \text{repeat},\ r=2\ }\; [\,1,1,2,2,3,3\,] \qquad\text{(repite el ELEMENTO)} $$

$$ [\,1,2,3\,] \;\xrightarrow{\ \text{tile},\ \text{reps}=2\ }\; [\,1,2,3,1,2,3\,] \qquad\text{(repite el BLOQUE)} $$

```python
import numpy as np
a = np.array([1, 2, 3])
np.repeat(a, 2)   # [1, 1, 2, 2, 3, 3]   → cada elemento, in situ
np.tile(a, 2)     # [1, 2, 3, 1, 2, 3]   → el array entero, como mosaico
```

## Funciones

### [[np.repeat]] — repite cada elemento r veces
Estira un eje duplicando cada elemento `r` veces consecutivas: $(\dots,n_p,\dots)\to(\dots,n_p\cdot r,\dots)$.
Con `repeats` como array permite cuentas **desiguales** por elemento. Útil para expandir etiquetas por
conteo, hacer upsample de imágenes píxel a píxel o duplicar muestras de un dataset.

### [[np.tile]] — repite el array entero como mosaico
Embaldosa el bloque completo `reps` veces por eje: cada dimensión se multiplica por su `reps`. Útil
para construir dameros, kernels periódicos o replicar un vector como filas de una matriz. A menudo el
broadcasting evita tener que materializarlo.

### [[np.roll]] — desplaza circularmente
Rota los elementos `shift` posiciones a lo largo de `axis`; lo que sale por un extremo entra por el
otro. El **shape se conserva** y no se pierde ningún dato. Útil para correlación circular, desfases de
señales periódicas y diferencias con retardo (`a - np.roll(a, 1)`).

### [[np.pad]] — añade relleno alrededor
Agranda el array añadiendo un borde: cada eje crece por lo que se pida antes y después,
$(n_0,\dots)\to(n_0+p_0,\dots)$. El `mode` (`'constant'`, `'edge'`, `'reflect'`, `'wrap'`...) decide
con qué se rellena. Es el padding de imágenes y convoluciones, y la versión "no circular" de `roll`.

## Tabla de funciones

| Función | Qué hace al shape | Unidad / efecto | Devuelve |
|---|---|---|---|
| [[np.repeat]] | el eje crece: $n_p \to n_p\cdot r$ | repite cada **elemento** | copia |
| [[np.tile]] | cada dim por su `reps` | repite el **bloque** entero | copia |
| [[np.roll]] | shape **conservado** | rota circularmente | copia |
| [[np.pad]] | cada eje $n_i \to n_i + p_i$ | rellena un **borde** | copia |

## Ejemplo comparativo: agrandar de cuatro maneras

```python
import numpy as np
a = np.array([1, 2, 3])

np.repeat(a, 2)               # [1, 1, 2, 2, 3, 3]          → elemento
np.tile(a, 2)                 # [1, 2, 3, 1, 2, 3]          → bloque
np.roll(a, 1)                 # [3, 1, 2]                   → rota (mismo tamaño)
np.pad(a, (1, 1))             # [0, 1, 2, 3, 0]             → rellena borde
```

## Notas relacionadas

- [[concepto_shape]] — el mapa de shapes de cada transformación
- [[concepto_axis_parametro]] — a lo largo de qué eje actúan `repeat` y `roll`
- [[concepto_broadcasting]] — la alternativa sin materializar (`tile`)
- [[Librerias/Numpy/np/manipulacion_forma/index|manipulacion_forma]] — la familia completa de forma
