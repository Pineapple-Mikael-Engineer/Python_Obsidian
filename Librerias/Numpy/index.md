---
title: NumPy — libreria de arrays N-dimensionales
tags:
  - numpy
  - indice
draft: false
---

# NumPy — libreria de arrays N-dimensionales

NumPy es la libreria fundamental del ecosistema cientifico de Python: provee el tipo [[concepto_ndarray|ndarray]], un array N-dimensional de datos homogeneos almacenado en memoria contigua, junto con cientos de operaciones vectorizadas que operan sobre el directamente sin bucles Python. Pandas, SciPy, scikit-learn y Matplotlib se apoyan en el `ndarray` como estructura de datos base. Usar NumPy es la diferencia entre procesar millones de elementos en milisegundos o en segundos.

## Ejemplo rapido

```python
import numpy as np

# Crear una matriz 3x3 de flotantes
A = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]], dtype=np.float64)

# Operacion vectorizada: no requiere bucle
B = A * 2 + np.arange(3)   # broadcasting automatico
print(B.shape)              # (3, 3)
print(B.sum(axis=0))        # reduccion por columnas
```

## Como navegar el vault

| Modulo / seccion | Contenido | Indice |
|---|---|---|
| `conceptos_transversales/` | El modelo mental de NumPy: ndarray, shapes, dtypes, broadcasting, vistas, ufuncs, axis… | [[Librerias/Numpy/conceptos_transversales/index\|conceptos_transversales]] |
| `np/` | Funciones del namespace raiz: creacion, manipulacion de forma, seleccion, operaciones, reducciones, estadisticas, conjuntos, io, polinomios | [[Librerias/Numpy/np/index\|np]] |
| `np.ndarray/` | Atributos (`shape`, `dtype`, `strides`, `flags`…) y metodos del objeto base (`reshape`, `copy`, `flatten`…) | [[Librerias/Numpy/np.ndarray/index\|np.ndarray]] |
| `np.linalg/` | Algebra lineal: productos, sistemas de ecuaciones, inversas, determinantes, normas, eigenvalores, descomposiciones | [[Librerias/Numpy/np.linalg/index\|np.linalg]] |
| `np.random/` | Generacion de numeros aleatorios: uniformes, normales, discretas, especiales, permutaciones, semilla | [[Librerias/Numpy/np.random/index\|np.random]] |

## Notas relacionadas

- [[concepto_ndarray]]
- [[concepto_broadcasting]]
- [[concepto_vectorizacion]]
