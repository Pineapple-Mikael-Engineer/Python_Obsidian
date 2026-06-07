---
title: np/seleccion — funciones de seleccion y filtrado de arrays
tags:
  - numpy
  - indice
draft: false
---

# np/seleccion — funciones de seleccion y filtrado de arrays

`seleccion/` agrupa las funciones de NumPy para extraer, filtrar o modificar elementos de un array segun condiciones booleanas o indices explcitos. Se diferencian del indexado basico de NumPy en que operan de forma vectorizada y permiten patrones mas complejos que una simple mascara.

## Tabla de decision

| Necesito… | Funcion |
|-----------|---------|
| Elegir entre dos valores segun una condicion | [[np.where]] |
| Elegir entre N alternativas con N condiciones | [[np.select]] |
| Extraer elementos por lista de indices | [[np.take]] |
| Escribir valores en posiciones por lista de indices | [[np.put]] |
| Acotar valores entre un minimo y un maximo | [[np.clip]] |
| Elegir elementos de un conjunto de arrays segun indices | [[np.choose]] |
| Obtener las posiciones donde se cumple una condicion | [[np.nonzero]] |

## Ejemplo rapido

```python
import numpy as np

arr = np.array([-3, 0, 5, -1, 8])

# Reemplazar negativos por cero
np.where(arr < 0, 0, arr)          # [0, 0, 5, 0, 8]

# Acotar entre -1 y 6
np.clip(arr, -1, 6)                # [-1, 0, 5, -1, 6]

# Posiciones de valores positivos
np.nonzero(arr > 0)                # (array([2, 4]),)

# Extraer por indices
np.take(arr, [0, 2, 4])            # [-3, 5, 8]
```

## Notas de la carpeta

- [[np.where]] — seleccion condicional elemento a elemento (dos modos: seleccion e indices)
- [[np.take]] — extraccion por lista de indices
- [[np.put]] — escritura in-place por lista de indices
- [[np.clip]] — acotacion de valores entre minimo y maximo
- [[np.choose]] — seleccion elemento a elemento entre N arrays usando un indice
- [[np.select]] — seleccion entre N alternativas con N condiciones independientes
- [[np.nonzero]] — posiciones donde el array es distinto de cero (o donde la condicion es True)
