---
title: Conversión Explícita
order: 2
draft: false
tags:
  - python
  - teoria
  - transformacion-tipos
aliases:
  - Casting
  - Type Casting
  - Funciones Constructoras
---
# Conversión Explícita (Casting)

La **conversión explícita** transforma un valor de un tipo a otro mediante funciones constructoras (`int()`, `float()`, `str()`, `bool()`, `list()`, …). A diferencia de la [[01 Conversion Implicita | coerción]], el programador decide el tipo destino y asume el riesgo de pérdida de información (truncamiento) o de fallo en tiempo de ejecución (`ValueError`, `TypeError`).

## Constructores fundamentales

### `int()` — conversión a entero

Trunca hacia cero (no redondea). Sobre `str`, admite una base como segundo argumento.

```python
print(int(3.9))           # 3 (trunca, NO redondea)
print(int(-2.7))          # -2 (trunca hacia cero)
print(int("100"))         # 100
print(int("101", 2))      # 5 (convierte binario "101" a decimal)
print(int("FF", 16))      # 255 (hexadecimal a decimal)
```

### `float()` — conversión a punto flotante

```python
print(float("10.5"))      # 10.5
print(float(7))           # 7.0
print(float("inf"))       # inf (infinito positivo)
print(float("-inf"))      # -inf (infinito negativo)
print(float("nan"))       # nan (Not a Number)
```

### `str()` — representación textual

```python
print(str(42))            # "42"
print(str([1, 2, 3]))     # "[1, 2, 3]"
print(str(3.14159))       # "3.14159"
```

### `bool()` — evaluación de truthiness

Aplica las reglas de [[Valores Truthy y Falsy | truthiness]]: vacíos, cero y `None` son `False`.

```python
print(bool(0))            # False
print(bool(1))            # True
print(bool(""))           # False (string vacío)
print(bool("Hola"))       # True
print(bool([]))           # False (lista vacía)
print(bool([1, 2]))       # True
print(bool(None))         # False
```

## Constructores de colecciones

Construyen una colección a partir de cualquier iterable.

```python
# list() - lista desde iterable
print(list("Python"))           # ['P', 'y', 't', 'h', 'o', 'n']
print(list((1, 2, 3)))          # [1, 2, 3]
print(list({1, 2, 3}))          # [1, 2, 3] (orden puede variar)
print(list(range(5)))           # [0, 1, 2, 3, 4]

# tuple() - tupla desde iterable
print(tuple([1, 2, 3]))         # (1, 2, 3)
print(tuple("abc"))             # ('a', 'b', 'c')

# set() - conjunto (elimina duplicados)
print(set([1, 2, 2, 3, 3]))     # {1, 2, 3}
print(set("banana"))            # {'b', 'a', 'n'}

# dict() - diccionario desde pares o kwargs
print(dict([('a', 1), ('b', 2)]))    # {'a': 1, 'b': 2}
print(dict(a=1, b=2))                # {'a': 1, 'b': 2}
print(dict(zip(['x', 'y'], [5, 6]))) # {'x': 5, 'y': 6}
```

El destino de cada constructor se desarrolla en su nota propia: [[02 Listas | lista]], [[03 Tuplas | tupla]], [[01 Sets | conjunto]] y [[01 Diccionarios | diccionario]].

## Caracteres y sistemas numéricos

`chr()` y `ord()` son inversas entre código Unicode y carácter. `bin()`, `hex()` y `oct()` devuelven **strings** con el prefijo de base; `int()` con base revierte la conversión.

```python
# chr() - entero a carácter Unicode
print(chr(65))            # 'A'
print(chr(8364))          # '€' (símbolo del euro)
print(chr(128512))        # '😀' (emoji)

# ord() - carácter a código Unicode
print(ord('A'))           # 65
print(ord('€'))           # 8364
print(ord('😀'))          # 128512

# Sistemas numéricos (devuelven strings)
print(bin(10))            # '0b1010'
print(hex(255))           # '0xff'
print(oct(64))            # '0o100'

# Convertir de nuevo a entero
print(int('0b1010', 2))   # 10
print(int('0xff', 16))    # 255
print(int('0o100', 8))    # 64
```

## Tabla de referencia rápida

| Conversión | Función | Ejemplo | Resultado |
|------------|---------|---------|-----------|
| **A Entero** | `int()` | `int("100")` | `100` |
| **A Float** | `float()` | `float(7)` | `7.0` |
| **A String** | `str()` | `str([1,2])` | `"[1, 2]"` |
| **A Bool** | `bool()` | `bool("")` | `False` |
| **A Lista** | `list()` | `list("abc")` | `['a','b','c']` |
| **A Tupla** | `tuple()` | `tuple([1,2])` | `(1, 2)` |
| **A Conjunto** | `set()` | `set([1,1,2])` | `{1, 2}` |
| **A Binario** | `bin()` | `bin(10)` | `'0b1010'` |
| **Carácter** | `chr()` | `chr(65)` | `'A'` |
| **Código** | `ord()` | `ord('A')` | `65` |

## Conversiones seguras y manejo de errores

`int()` y `float()` lanzan `ValueError` cuando el `str` no representa un número válido, y `TypeError` cuando el argumento es de un tipo no admitido (p. ej. `None`). El patrón robusto envuelve la conversión en `try-except`.

```python
def convertir_a_entero_seguro(valor):
    """Intenta convertir a entero, devuelve None si falla."""
    try:
        return int(valor)
    except (ValueError, TypeError):
        return None

# Pruebas
print(convertir_a_entero_seguro("123"))     # 123
print(convertir_a_entero_seguro("12.3"))    # None (float string)
print(convertir_a_entero_seguro("abc"))     # None
print(convertir_a_entero_seguro(None))      # None

def convertir_cadena_numerica(valor: str) -> Union[int, float, None]:
    """Convierte string a número manteniendo tipo."""
    try:
        if '.' in valor or 'e' in valor.lower():
            return float(valor)
        else:
            return int(valor)
    except ValueError:
        return None
```

En procesamiento de datos crudos conviene validar el formato antes de elegir el constructor, evitando así excepciones predecibles:

```python
def normalizar_datos(fila: list) -> list:
    """Normaliza tipos en una fila de datos."""
    normalizada = []
    
    for elemento in fila:
        if isinstance(elemento, str):
            # Intenta convertir strings numéricos
            elemento = elemento.strip()
            if elemento.replace('.', '', 1).isdigit():
                normalizada.append(float(elemento))
            elif elemento.isdigit():
                normalizada.append(int(elemento))
            else:
                normalizada.append(elemento)
        else:
            normalizada.append(elemento)
    
    return normalizada

# Ejemplo
datos_crudos = ["123", "45.67", "texto", "  89  ", "0.5e-2"]
print(normalizar_datos(datos_crudos))
# [123, 45.67, 'texto', 89, 0.005]
```

> [!warning] Errores comunes
> ```python
> # MAL: Asumir que float() siempre funciona
> # valor = float(input_usuario)  # Puede lanzar ValueError
>
> # BIEN: Validar antes
> entrada = input_usuario
> if entrada.replace('.', '', 1).isdigit():
>     valor = float(entrada)
> else:
>     # Manejar error
>     ...
>
> # MAL: Conversiones implícitas arriesgadas
> # resultado = "10" * 2  # "1010" (repetición, no multiplicación)
>
> # BIEN: Conversión explícita
> resultado = int("10") * 2  # 20
> ```

## Buenas prácticas

1. Usar `try-except` para conversiones que pueden fallar (`int()`, `float()` sobre entrada externa).
2. Validar el formato de la entrada **temprano**, antes de convertir, para evitar errores posteriores.
3. Recordar que `int()` trunca: si se requiere redondeo, usar `round()` antes de convertir.
4. Considerar el contexto antes de convertir; la coerción ya resuelve muchos casos aritméticos sin casting manual.
