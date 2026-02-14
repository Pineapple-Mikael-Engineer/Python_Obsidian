---
title: 04 Funciones
draft: false
tags:
  - Index
---


# FUNCIONES EN PYTHON

## 📝 DEFINICIÓN
Una función es un bloque de código reutilizable que realiza una tarea específica. En Python, las funciones son **objetos de primera clase**, lo que significa que pueden ser asignadas a variables, pasadas como argumentos y retornadas desde otras funciones.

## 🎯 PROPÓSITO
- **Reutilización**: Escribir código una vez, usarlo muchas veces
- **Modularidad**: Dividir problemas complejos en partes más pequeñas
- **Abstracción**: Ocultar detalles de implementación
- **Mantenibilidad**: Facilitar cambios y depuración

## 🏗️ ESTRUCTURA GENERAL
```python
def nombre_funcion(parametros):
    """Docstring: explica qué hace la función"""
    # Cuerpo de la función
    return valor_opcional
```

## 📑 CONTENIDO DEL MÓDULO

### [10 Definición y Llamada](./10%20Definicion%20y%20Llamada/index.md)
- Sintaxis básica de definición
- Cómo llamar/invocar funciones
- Parámetros y argumentos
- Valores de retorno

### [20 Clasificación de Funciones](./20%20Clasificacion%20de%20Funciones/index.md)
- Funciones built-in de Python
- Funciones definidas por usuario
- Funciones lambda (anónimas)
- Funciones recursivas

### [30 Ámbito y Espacios de Nombres](./30%20Ambito%20y%20Espacios%20de%20Nombres/index.md)
- Variables locales vs globales
- La regla LEGB
- La palabra clave `global`
- La palabra clave `nonlocal`

### [40 Patrones de Argumentos](./40%20Patrones%20de%20Argumentos/index.md)
- Argumentos posicionales y nominales
- Valores por defecto
- *args y **kwargs
- Parámetros solo posicionales (/)
- Parámetros solo nominales (*)

## 🔗 RELACIONES CON OTROS MÓDULOS

| Módulo | Relación |
|--------|----------|
| Variables y Tipos | Las funciones trabajan con tipos de datos |
| Estructuras de Control | if, for, while DENTRO de funciones |
| Estructuras de Datos | Funciones que reciben/retornan listas, dicts |
| Módulos | Las funciones son la unidad de organización |


