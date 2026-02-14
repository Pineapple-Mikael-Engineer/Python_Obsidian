---
title: 05 Manejo de Exepciones
draft: false
---



## ¿Qué es una Excepción?

Desde un punto de vista técnico:

> Una **excepción** es un evento que interrumpe el flujo normal de ejecución de un programa cuando ocurre un error en tiempo de ejecución.

A diferencia de los errores de sintaxis (detectados antes de ejecutar el programa), las excepciones ocurren cuando el programa ya está corriendo.

Ejemplos típicos:

- División entre cero
    
- Acceso a una clave inexistente
    
- Conversión inválida de tipos
    
- Archivo no encontrado
    

En esencia:

-  Una excepción es una señal de que algo no salió como se esperaba.

---

# Arquitectura del Manejo de Excepciones

El manejo de excepciones en Python se basa en tres pilares fundamentales:


##  Excepciones Built-in

Python incluye un conjunto de excepciones predefinidas que representan errores comunes.

- [[01 Excepciones Built-in|Excepciones Built-in]]
    

En esta sección se estudiará:

- Jerarquía de excepciones
    
- Excepciones más frecuentes
    
- Diferencia entre `Exception` y `BaseException`
    
- Casos prácticos de cada tipo
    
- Buenas prácticas al capturarlas
    

Aquí se entiende **qué puede fallar**.

---

##  Try / Except / Finally

Es la estructura que permite capturar y manejar excepciones.

- [[02 Try Except Finally|Try Except Finally]]
    

Aquí se estudiará:

- Sintaxis completa
    
- Múltiples bloques `except`
    
- Uso de `else`
    
- Uso de `finally`
    
- Manejo específico vs manejo genérico
    
- Buenas prácticas y anti-patrones
    

Aquí se aprende **cómo reaccionar ante el error**.

---

##  Raise de Excepciones

Permite generar excepciones de manera explícita.

- [[03 Raise de Excepciones|Raise de Excepciones]]
    

Se abordará:

- Uso de `raise`
    
- Re-lanzamiento de excepciones
    
- Creación de errores personalizados
    
- Diseño defensivo
    
- Validaciones explícitas
    

Aquí se aprende **cuándo y por qué provocar un error intencionalmente**.

---

# Filosofía del Manejo de Errores

En Python existe una filosofía importante:

> Es mejor pedir perdón que pedir permiso (EAFP — _Easier to Ask Forgiveness than Permission_).

Esto significa que muchas veces:

- Se intenta ejecutar la acción.
    
- Si falla, se maneja la excepción.
    

En lugar de:

- Verificar todo antes de ejecutar.
    

Comprender esto cambia completamente la manera de escribir código.

---

# Relación con Otros Módulos

El manejo de excepciones se conecta directamente con:

- Variables y Tipos de Datos
    
- Estructuras de Control
    
- Estructuras de Datos
    
- Entrada y salida de datos
    

Porque cualquier operación sobre datos puede generar una excepción.

---

# Enfoque del Módulo

Cada nota desarrollará:

- Fundamento conceptual
    
- Jerarquía formal
    
- Sintaxis detallada
    
- Ejemplos prácticos
    
- Casos reales
    
- Buenas prácticas
    
- Errores comunes
    
- Diseño robusto
    

---

#  Notas del Módulo

- [[01 Excepciones Built-in|Excepciones Built-in]]
    
- [[02 Try Except Finally|Try Except Finally]]
    
- [[03 Raise de Excepciones|Raise de Excepciones]]
    
