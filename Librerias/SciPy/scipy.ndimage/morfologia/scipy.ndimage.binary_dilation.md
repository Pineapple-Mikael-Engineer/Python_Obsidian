---
title: scipy.ndimage.binary_dilation — dilatacion morfologica binaria
aliases:
  - binary_dilation
  - scipy.ndimage.binary_dilation
  - dilatacion binaria
tags:
  - scipy
  - api/funcion
  - procesamiento-imagen
lib: scipy
tipo: funcion
mod: scipy.ndimage
retorna: ndarray (bool)
requiere:
  - numpy
draft: false
---

# scipy.ndimage.binary_dilation — dilatacion morfologica binaria

**Dilata** (engorda) el **primer plano** de una mascara binaria. Un pixel se activa como verdadero si el elemento estructurante, centrado sobre el, **TOCA** el objeto en al menos un punto. El efecto neto es **expandir los bordes**, **rellenar huecos pequeños** dentro de los objetos y **conectar regiones proximas** separadas por una brecha estrecha. Devuelve un `ndarray` **booleano** del mismo tamaño que la entrada.

> Es la operacion **dual de la erosion**. Donde `binary_erosion` exige que TODO el elemento estructurante caiga dentro del objeto (y por eso encoge), `binary_dilation` solo exige que TOQUE el objeto (y por eso expande). Una dilatacion seguida de una erosion (cierre) rellena huecos sin engordar globalmente.

## Firma

```python
scipy.ndimage.binary_dilation(
    input,               # array_like: mascara binaria (se interpreta por verdad/falsedad)
    structure=None,      # ndarray bool: elemento estructurante (def: conectividad-1, cruz)
    iterations=1,        # int: numero de dilataciones sucesivas
    mask=None,           # array_like: pixeles que pueden cambiar (los demas se congelan)
    output=None,         # ndarray: array destino opcional
    border_value=0,      # 0|1: valor asumido fuera del borde de la imagen
    origin=0,            # int|tuple: desplazamiento del elemento estructurante
    brute_force=False,   # bool: estrategia de iteracion
) -> ndarray
```

## Valor de retorno

| Tipo | Significado |
|------|-------------|
| `ndarray` (dtype `bool`) | Mascara dilatada: `True` donde el elemento estructurante toca el primer plano original |

```python
out = binary_dilation(mask)
out.dtype    # → dtype('bool')
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Dilatacion por defecto (cruz 3x3) | `binary_dilation(mask)` |
| Dilatacion mas fuerte (cuadrado 3x3) | `binary_dilation(mask, structure=np.ones((3,3)))` |
| Engordar varios pasos | `binary_dilation(mask, iterations=3)` |
| Limitar a una region | `binary_dilation(mask, mask=region)` |
| Rellenar huecos (cierre) | `binary_erosion(binary_dilation(mask))` |

## Parametros en detalle

### `input` (obligatorio)

Mascara a dilatar. Se interpreta por **verdad/falsedad**: cualquier valor no nulo es primer plano. Habitualmente un array `bool`; la salida siempre es booleana.

```python
import numpy as np
from scipy.ndimage import binary_dilation

mask = np.array([[0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,1,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0]], dtype=bool)
binary_dilation(mask).astype(int)
# → el punto central crece a una cruz (sus 4 vecinos se activan)
# [[0 0 0 0 0]
#  [0 0 1 0 0]
#  [0 1 1 1 0]
#  [0 0 1 0 0]
#  [0 0 0 0 0]]
```

### `structure`

**Elemento estructurante**: la vecindad con la que se "pinta" alrededor de cada pixel del objeto. Por defecto es la **conectividad-1** (cruz: 4 vecinos ortogonales en 2D). Un elemento mayor (`np.ones((3,3))`, 8 vecinos) dilata **mas** por pasada. Se genera con `generate_binary_structure`.

```python
from scipy.ndimage import generate_binary_structure
cruz = generate_binary_structure(2, 1)   # cruz (def)
cuad = generate_binary_structure(2, 2)   # cuadrado 3x3 (8-vecinos)
```

### `iterations`

Repite la dilatacion `n` veces; a mas iteraciones, mas se expande el objeto y mas grandes son los huecos/brechas que llega a rellenar o cerrar.

### `mask`

Solo los pixeles donde `mask` es verdadero pueden cambiar; el resto se **congela**. Util para confinar el crecimiento a una zona (p. ej. dilatar dentro de una region de interes sin invadir lo demas).

### `border_value`

Valor asumido **fuera** de los limites de la imagen. Por defecto `0` (fondo). Rara vez hace falta cambiarlo en dilatacion, salvo que quieras que el exterior cuente como primer plano.

## Erosion vs dilatacion (contraste)

| Aspecto | `binary_erosion` | `binary_dilation` |
|---------|------------------|-------------------|
| Condicion del pixel | El elemento **cabe entero** dentro del objeto | El elemento **toca** el objeto |
| Efecto en el primer plano | Encoge / adelgaza | Expande / engorda |
| Uso tipico | Eliminar motas, romper puentes finos | Rellenar huecos, conectar regiones |
| Composicion limpia ruido | Apertura: erosion → dilatacion | Cierre: dilatacion → erosion |
| Dualidad | Erosionar primer plano = dilatar fondo | Dilatar primer plano = erosionar fondo |

## Casos de uso

### Rellenar huecos pequeños y conectar regiones

Una dilatacion une fragmentos separados por una brecha estrecha.

```python
import numpy as np
from scipy.ndimage import binary_dilation

m = np.zeros((1,7), dtype=bool)
m[0,1] = m[0,2] = True
m[0,4] = m[0,5] = True     # dos fragmentos con un hueco en el medio
binary_dilation(m).astype(int)
# → [0 1 1 1 1 1 1]   (el hueco de 1 pixel se cierra y los fragmentos se conectan)
```

### Cierre: rellenar sin engordar (dilatacion + erosion)

El patron comun es **dilatar y luego erosionar** (cierre morfologico): la dilatacion rellena huecos y la erosion devuelve a los objetos su tamaño aproximado. Es exactamente lo que hace `binary_closing`.

```python
from scipy.ndimage import binary_erosion
cerrado = binary_erosion(binary_dilation(m))   # equivalente a binary_closing(m)
```

## Buenas practicas

1. Trabaja sobre arrays `bool` (`mask = imagen > umbral`) antes de dilatar.
2. Para **rellenar huecos sin engordar** los objetos, usa el cierre (dilatacion + erosion) en vez de una dilatacion sola.
3. Recuerda la simetria: dilatar es lo opuesto a erosionar; combinar ambos en el orden correcto define apertura y cierre.
4. Controla la intensidad con `iterations` o `structure`, no con multiples llamadas manuales.
5. Para crecimiento confinado a una zona, usa el parametro `mask`.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Los objetos se funden entre si | Demasiadas `iterations` o elemento grande | Reducir iteraciones o elemento mas pequeño |
| Salida entera esperada | La salida siempre es `bool` | Convertir con `.astype(int)` |
| Confundir efecto con erosion | Dilatacion **expande**, no encoge | Usar `binary_erosion` si se busca adelgazar |
| El hueco no se cierra | Brecha mayor que el alcance de la dilatacion | Subir `iterations` o usar elemento mayor |
| Crecimiento invade zonas no deseadas | Sin `mask` el crecimiento es global | Pasar `mask=region` para confinarlo |

## Limitaciones

- Opera sobre **mascaras binarias**; para escala de grises existe `grey_dilation`.
- Una dilatacion aislada **siempre engorda** tambien lo valido: para preservar tamaño hay que componerla con una erosion (cierre).
- El resultado depende del **elemento estructurante** elegido; la conectividad cambia que huecos se rellenan y que regiones se conectan.
- No etiqueta ni mide regiones; solo transforma la mascara.

## Notas relacionadas

- [[scipy.ndimage.binary_erosion]]
- [[scipy.ndimage.label]]
