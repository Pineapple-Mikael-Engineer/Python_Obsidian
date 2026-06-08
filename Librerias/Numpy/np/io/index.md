---
title: np/io — lectura y escritura de arrays en disco
tags:
  - numpy
  - indice
draft: false
---

# np/io — lectura y escritura de arrays en disco

Este grupo cubre las funciones para persistir y recuperar ndarrays en el sistema de archivos. El eje de decision principal es el formato: texto (CSV y similares) o binario NumPy (`.npy`/`.npz`).

El formato texto es portable — cualquier lenguaje puede leerlo — pero pierde precision en flotantes y es significativamente mas lento. El formato binario preserva dtype, shape y orden de memoria exactamente, y la carga es mucho mas rapida. Para arrays que no caben en RAM, `np.memmap` permite operar sobre ellos directamente desde disco sin cargarlos completamente.

## Notas de la carpeta

- [[np.loadtxt]] — carga arrays desde archivos de texto delimitados (CSV, espacio, tabulador). Simple y directo para datos limpios sin valores faltantes ni cabeceras complejas.
- [[np.savetxt]] — guarda un array 1D o 2D como texto. Control de precision con `fmt=` y encabezados con `header=`. Genera archivos legibles pero mas grandes y mas lentos de cargar que el binario.
- [[np.genfromtxt]] — version robusta de `loadtxt`: maneja valores faltantes (`filling_values`), permite saltar lineas irregulares, y soporta dtypes mixtos por columna. Mas flexible pero mas lento.
- [[np.save]] — guarda un array en formato binario `.npy`. Preserva dtype, shape y orden de memoria exactamente. La carga posterior con `np.load` es mucho mas rapida que cualquier formato texto.
- [[np.load]] — carga un archivo `.npy` (devuelve ndarray directamente) o `.npz` (devuelve un objeto tipo dict con los arrays nombrados). Punto de entrada unico para ambos formatos binarios.
- [[np.savez]] — guarda multiples arrays en un archivo `.npz` (ZIP sin comprimir). Cada array se nombra como keyword argument: `np.savez('datos.npz', x=arr1, y=arr2)`.
- [[np.savez_compressed]] — igual que `savez` pero con compresion DEFLATE. Archivos significativamente mas pequenos; escritura y lectura mas lentas. Util cuando el espacio en disco importa mas que la velocidad de IO.
- [[np.memmap]] — mapea un archivo binario directamente a memoria sin cargarlo completamente. Permite leer y escribir en arrays mas grandes que la RAM disponible, accediendo solo a los segmentos necesarios.
