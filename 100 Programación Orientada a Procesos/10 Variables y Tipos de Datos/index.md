---
title: Variables y Tipos de Datos
draft: false
weight: 0
description: Descripcion de Variables y Datos Python
---

En el desarrollo de software, entender la diferencia entre el **contenedor** y el **contenido** es el primer paso para escribir código sólido.

# Conceptos Fundamentales

- **Variable:** Es un nombre (identificador) que apunta a un lugar en la memoria de la computadora donde se almacena un valor. En Python, son dinámicas: una misma variable puede apuntar a diferentes tipos de datos a lo largo del programa.    
- **Dato:** Es la unidad mínima de información que el programa manipula. Cada dato tiene un **tipo**, que determina qué operaciones se pueden realizar con él y cuánta memoria ocupa.
    
# Contenido del Módulo

## [[01 Datos Primitivos|Datos Primitivos]]

Exploración de los ladrillos básicos del lenguaje.

- **Numéricos:** `int` (enteros de precisión infinita), `float` (punto flotante y sus problemas de precisión) y `complex`.
- **Lógica:** `bool` como subclase de entero.
- **Cadenas:** `str` y el estándar Unicode/UTF-8.    
- **Vacío:** `NoneType` para representar la ausencia de valor.

## [[02 Mutabilidad y Inmutabilidad|Mutabilidad y Inmutabilidad]]

El concepto más crítico para la gestión de memoria y evitar efectos secundarios.

- **Inmutables:** Objetos que no cambian (Números, Cadenas, Tuplas). Son seguros y _hashables_.
- **Mutables:** Objetos modificables (Listas, Diccionarios). Requieren cuidado con las referencias y copias.
- **Implicaciones:** Diferencia entre asignar una nueva etiqueta y modificar el contenido interno.
    

## [[03 Transformación de Tipos|Transformación de Tipos]]

Cómo mover datos entre diferentes categorías de forma segura.

- **Implícita:** Coerción automática realizada por el intérprete.
- **Explícita:** Uso de constructores como `int()`, `str()` o `list()`.
- **Validación:** Herramientas para asegurar la integridad de los datos (`isinstance()`) y el uso de _Type Hints_.    
