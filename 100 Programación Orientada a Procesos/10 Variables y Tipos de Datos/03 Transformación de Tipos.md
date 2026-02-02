---
title: Transformación de Tipos
draft:
weight: 3
---
# Conversión Implícita (Coerción)

Ocurre automáticamente cuando Python decide que, para realizar una operación, debe transformar un dato a un tipo más "amplio" o compatible para evitar la pérdida de información.

- **`int` + `float` a `float`**: Si sumas un entero y un decimal, Python promociona el entero a flotante.
    - `5 + 2.0` resulta en `7.0`.
- **Booleanos en aritmética**: Los `bool` son subclase de `int`.
    - `True + 5` resulta en `6`.
    - `False * 10` resulta en `0`.

# Conversión Explícita
Es cuando se obliga a algún dato a transformarse con el uso de [[Constructores|funciones constructoras]]

## A. Constructores Fundamentales

- **`int()`**: Convierte a entero (trunca decimales, no redondea). `int(3.9)` a `3`.
- **`float()`**: Convierte a punto flotante. `float("10.5")` a `10.5`.
- **`str()`**: Convierte cualquier objeto en su representación de texto.
- **`bool()`**: Evalúa la verdad (_truthiness_) de un objeto.
### B. Constructores de Colecciones

Permiten transformar una estructura en otra:
- **`list()`**, **`tuple()`**, **`set()`**: Útiles para quitar duplicados (usando `set`) o hacer que una lista sea inmutable (usando `tuple`).
- **`dict()`**: Requiere una secuencia de pares (ej. una lista de tuplas `[(llave, valor)]`).

### C. Caracteres y Sistemas Numéricos

- **`chr(n)`**: Devuelve el carácter Unicode del número `n`. `chr(65)` a `'A'`.
- **`ord(c)`**: Devuelve el número Unicode del carácter `c`. `ord('A')` a `65`.
- **`bin()`, `hex()`, `oct()`**: Convierten un entero a una **cadena** que representa su valor en binario (`0b`), hexadecimal (`0x`) u octal (`0o`).

# Validación de Tipos

Antes de convertir, a veces necesitas saber qué tienes tipo de datos estas usando.

### `isinstance()` vs `type()`

Es una de las dudas más comunes en Python:

- **`type(obj)`**: Te dice exactamente qué es el objeto. Se usa para comparaciones estrictas: `type(x) == int`.
    
- **`isinstance(obj, clase)`**: Es más flexible y **recomendado**. Verifica si un objeto es de un tipo _o de una subclase de este_.
    
    - `isinstance(True, int)` devuelve `True` (porque bool es hijo de int). `type(True) == int` devuelve `False`.
        

## Type Hints Básicos (Sugerencias de tipo)

A partir de Python 3.5, puedes indicar qué tipo de dato esperas. No obliga a Python a cumplirlo (es informativo), pero ayuda mucho a los editores de código y a otros programadores.

```python
# Sintaxis: variable: tipo = valor
edad: int = 25
nombre: str = "Luis"

def saludar(nombre: str) -> str:
    return "Hola " + nombre
```

# Ejemplos

| Función       | Entrada (ejemplo) | Salida                    |
| ------------- | ----------------- | ------------------------- |
| `int("10")`   | Cadena            | `10` (Entero)             |
| `float(5)`    | Entero            | `5.0` (Flotante)          |
| `bin(10)`     | Entero            | `'0b1010'` (Cadena)       |
| `list("abc")` | Cadena            | `['a', 'b', 'c']` (Lista) |
