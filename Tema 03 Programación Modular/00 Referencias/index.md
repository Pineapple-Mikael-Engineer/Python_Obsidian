---
title: Referencias
order: 0
draft: false
description: Catálogo de archivos especiales y glosario modular — material de consulta rápida del tema
tags:
  - Index
  - Tema
aliases:
  - Referencias del Tema
  - Referencias Modular
---
# Referencias

Material **transversal** al capítulo: catálogos y glosarios que se consultan desde cualquier otra sección y que no pertenecen a un tema concreto. Notas de **consulta rápida**, no de desarrollo conceptual: aquí se localiza un nombre o se fija un término; el desarrollo vive en la sección correspondiente.

## Notas de referencia

- [[Catalogo de Archivos Especiales | Catálogo de Archivos Especiales]] — tabla de los archivos y atributos del sistema modular (`__init__.py`, `__main__.py`, `__version__.py`, `__all__`, `__name__`, `__path__`, `__package__`): propósito, dónde vive cada uno y su snippet típico.
- [[Glosario Modular | Glosario Modular]] — definición breve de los términos del paradigma modular: módulo, paquete, namespace, import absoluto/relativo, cohesión, acoplamiento, `sys.path`, `importlib`, etc.

## Cuándo se consultan

| Desde | Se consulta | Para |
| ----- | ----------- | ---- |
| [[51 Archivos Especiales/index \| Archivos Especiales]] | Catálogo de Archivos Especiales | Recordar la firma y ubicación de un archivo `__x__` |
| [[60 Diseno de APIs Modulares/index \| Diseño de APIs Modulares]] | Catálogo de Archivos Especiales | Mapear necesidad de exposición → `__all__` |
| Cualquier sección | Glosario Modular | Fijar el significado preciso de un término |
