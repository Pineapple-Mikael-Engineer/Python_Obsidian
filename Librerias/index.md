---
title: Librerias — documentacion de librerias de Python
aliases:
  - Librerias
  - Librerías
  - libraries
tags:
  - indice
  - librerias
order: 0
draft: false
---

# Librerías de Python

Este directorio documenta librerías de Python como un **grafo de conocimiento navegable**: cada elemento de la API (una función, un método, una clase, un concepto) es una nota consultable de forma aislada, conectada con sus vecinas por wikilinks. La meta es que la documentación sea **escalable** (muchas notas sin degradarse), **navegable** (un graph limpio), **consistente entre librerías** e **integrada con Git** (una rama por librería). El estándar que gobierna todas las notas vive en [[Estandarizan Directorio Librerias|el estándar base de librerías]]; cada librería lo especializa con su propio `Tree` (el mapa de notas) y sus `Reglas` dentro de su carpeta `_private/`.

## Las librerías documentadas

Ocho librerías, agrupadas por su papel en el ecosistema científico, de visualización e ingeniería de Python.

### Núcleo numérico y matemático

| Librería | Qué resuelve |
|----------|--------------|
| [[Numpy/index\|NumPy]] | el motor de arrays N-dimensionales; la base sobre la que se apoya casi todo lo demás |
| [[SciPy/index\|SciPy]] | algoritmos científicos sobre NumPy (optimización, integración, álgebra lineal, señales) |
| [[SymPy/index\|SymPy]] | matemática simbólica exacta (álgebra, cálculo, ecuaciones con símbolos, no con números) |

### Visualización y animación

| Librería | Qué resuelve |
|----------|--------------|
| [[Matplotlib/index\|Matplotlib]] | visualización 2D con el modelo Figure / Axes / Artists |
| [[VisPy/index\|VisPy]] | visualización científica interactiva acelerada por GPU (OpenGL) |
| [[Manim/index\|Manim]] | animación matemática orientada a objetos (la tríada Scene / Mobject / Animation) |

### Interfaz y dominio

| Librería | Qué resuelve |
|----------|--------------|
| [[PyQt6/index\|PyQt6]] | GUI de escritorio orientada a objetos (widgets, señales y slots) |
| [[CoolProp/index\|CoolProp]] | propiedades termodinámicas de fluidos (la capa de ingeniería) |

## Cómo está organizado

Cada librería sigue el mismo patrón, definido en [[Estandarizan Directorio Librerias|el estándar base]]:

- **Carpetas** = organización temática interna (no se duplica en tags lo que ya dice el path).
- **Tags** = agrupación global cruzada entre librerías (`<libreria>`, `api/<tipo>`, dominio funcional).
- **Frontmatter** = metadata consultable (tipo, retorno, herencia, dependencias).
- **`index.md`** = la nota madre de cada carpeta: no solo lista a sus hijas, también enseña el grupo con ejemplos y recetas.
- **`_private/`** = el `Tree` (mapa y roadmap de notas) y las `Reglas` (convenciones específicas de esa librería).

El naming de los archivos imita la documentación oficial (`np.mean.md`, `ndarray.reshape.md`, `Circle.md`, `concepto_broadcasting.md`): el nombre del archivo va en ASCII, mientras que el contenido usa español normal con tildes y ñ.

## Notas relacionadas

- [[Estandarizan Directorio Librerias]] — el estándar base que gobierna todas las notas de librerías
