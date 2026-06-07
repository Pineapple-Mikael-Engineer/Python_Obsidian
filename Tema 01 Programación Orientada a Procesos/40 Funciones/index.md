---
title: Funciones
draft: false
description: Abstracción y reutilización mediante funciones en Python
tags:
  - Index
  - Tema
aliases:
  - Funciones
---
# Funciones

Una **función** es un bloque de código con nombre que encapsula una tarea y se ejecuta al ser invocado, opcionalmente recibiendo argumentos y devolviendo un valor. Es la unidad de **abstracción** y **reutilización** del paradigma procedimental: convierte una secuencia de instrucciones en una operación reutilizable y nombrada.

En Python las funciones son **objetos de primera clase**: se asignan a variables, se pasan como argumentos y se retornan desde otras funciones —propiedad sobre la que se construyen [[08 Closures | closures]], [[07 Funciones de Orden Superior | funciones de orden superior]] y [[06 Decoradores | decoradores]].

```python
def area_rectangulo(base, altura):
    """Devuelve el área de un rectángulo."""
    return base * altura

area_rectangulo(5, 3)   # 15
```

## Subtemas

- [[41 Definicion y Llamada/index | Definición y Llamada]] — sintaxis `def`, parámetros frente a argumentos, paso por asignación y valor de retorno.
- [[42 Clasificacion de Funciones/index | Clasificación de Funciones]] — built-in, de usuario, lambda, recursivas, generadoras, de orden superior, closures y decoradores.
- [[43 Ambito y Espacios de Nombres/index | Ámbito y Espacios de Nombres]] — regla **LEGB**, palabras clave `global` y `nonlocal`, tiempo de vida de los nombres.
- [[44 Patrones de Argumentos/index | Patrones de Argumentos]] — posicionales y nominales, valores por defecto, `*args`/`**kwargs`, parámetros solo-posicionales (`/`) y solo-nominales (`*`).

## Estructura general

```python
def nombre(parametros):     # firma: nombre + parámetros
    """docstring"""         # documentación opcional
    cuerpo                  # bloque indentado
    return valor            # retorno opcional (None implícito si se omite)
```

| Concepto | Define | Subtema |
| -------- | ------ | ------- |
| Firma | Nombre y parámetros | [[41 Definicion y Llamada/index \| Definición]] |
| Tipos de función | Origen y comportamiento | [[42 Clasificacion de Funciones/index \| Clasificación]] |
| Ámbito | Dónde es visible cada nombre | [[43 Ambito y Espacios de Nombres/index \| Ámbito]] |
| Argumentos | Cómo se pasan los valores | [[44 Patrones de Argumentos/index \| Patrones de Argumentos]] |

Las funciones contienen [[30 Estructuras de Control/index | estructuras de control]], operan sobre [[20 Estructura de Datos/index | colecciones]] y, al fallar, propagan [[50 Manejo de Excepciones/index | excepciones]] a quien las llamó.
