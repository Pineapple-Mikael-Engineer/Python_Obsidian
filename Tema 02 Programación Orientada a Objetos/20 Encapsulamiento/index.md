---
title: 20 Encapsulamiento
draft: false
description: Protección del estado tras una interfaz controlada
tags:
  - Index
  - Tema
aliases:
  - Encapsulamiento
  - Encapsulación
---
# Encapsulamiento

El **encapsulamiento** consiste en restringir el acceso directo al estado interno de un objeto y exponer en su lugar una **interfaz controlada**. El objeto deja de ser una bolsa de datos manipulables desde fuera y pasa a garantizar sus propios invariantes: quien lo usa interactúa con métodos y propiedades, no con los atributos crudos.

Python no tiene modificadores de acceso reales (`private`, `protected` del estilo de C++ o Java); aplica **convenciones** —el guion bajo— y un único mecanismo de ocultación parcial —el *name mangling*—. La filosofía es *"todos somos adultos responsables"*: la privacidad se señala, no se impone.

```python
class Termostato:
    def __init__(self, temp):
        self._temp = temp          # "protegido": uso interno por convención
    @property
    def temp(self):                # interfaz controlada de lectura
        return self._temp
    @temp.setter
    def temp(self, valor):         # validación al escribir
        if not -50 <= valor <= 50:
            raise ValueError("fuera de rango")
        self._temp = valor
```

## Subtemas

- [[21 Visibilidad/index | Visibilidad]] — los tres niveles convencionales: público, protegido (`_nombre`) y privado (`__nombre`) con su *name mangling*.
- [[22 Properties/index | Properties]] — `@property` y *setters*: transformar un atributo en una interfaz con validación, solo-lectura o cálculo.

## Niveles de acceso en Python

| Convención | Señal | Significado | Subtema |
| ---------- | ----- | ----------- | ------- |
| `nombre` | — | Público: parte de la API | [[21 Visibilidad/index \| Visibilidad]] |
| `_nombre` | un guion bajo | Protegido: uso interno, no toques | [[21 Visibilidad/index \| Visibilidad]] |
| `__nombre` | dos guiones bajos | Privado: *name mangling* a `_Clase__nombre` | [[21 Visibilidad/index \| Visibilidad]] |
| `propiedad` | `@property` | Acceso de atributo respaldado por métodos | [[22 Properties/index \| Properties]] |

El encapsulamiento es la base del **acceso controlado** que luego respeta la [[30 Herencia/index | herencia]]: una subclase hereda la interfaz pública y debe respetar los invariantes que la clase base protege.
