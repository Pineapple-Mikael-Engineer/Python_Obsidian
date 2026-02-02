---
title: " Condicionales (if, elif, else)"
draft: false
weight: 1
---

Las condicionales en Python no son solo bifurcaciones; son expresiones de la lógica de evaluación del intérprete.

# La Lógica Fundamental: Operadores y Verdad

## A. Operadores Lógicos y Evaluación Cortocircuitada (Short-circuit)

Python optimiza la evaluación lógica de izquierda a derecha.

- **`and` (Conjunción):** Si el primer operando es _Falsy_, Python **no evalúa** el segundo, porque el resultado final será falso de todos modos.
    
- **`or` (Disyunción):** Si el primer operando es _Truthy_, el segundo no se evalúa; el resultado ya es verdadero.

## B. Precedencia de Operadores

En expresiones complejas, Python sigue este orden (de mayor a menor importancia):

1. **Comparaciones** (`<`, `>`, `==`, `!=`, `is`, `in`)    
2. **`not`** (Negación)
3. **`and`** (Conjunción)
4. **`or`** (Disyunción)

## C. El Protocolo de Verdad: Truthy y Falsy

Python no solo mira booleanos; invoca internamente al método `__bool__()` (o `__len__()` si el primero no existe) del objeto.

- **Falsy:**
    - `None`, `False`.   
    - Ceros: `0`, `0.0`, `0j`, `Decimal(0)`, `Fraction(0, 1)`.
    - Vacíos: `''`, `()`, `[]`, `{}`, `set()`, `range(0)`.
- **Truthy:** Cualquier objeto que no esté en la lista anterior.
    


# Bloques Condicionales: `if`, `elif`, `else`

## A. Definiciones Específicas

- **`if`**: Evalúa una expresión de prueba. Si el resultado es _Truthy_, el bloque indentado se ejecuta. Abre un nuevo ámbito de ejecución pero **no** un nuevo _scope_ de variables (las variables definidas dentro de un `if` son visibles fuera).
    
- **`elif`**: Permite verificar múltiples condiciones mutuamente excluyentes. Evita el "Efecto Escalera" de los `if` anidados, mejorando la complejidad ciclomática del código.
    
- **`else`**: Bloque de escape. En una cadena de `if/elif`, el `else` garantiza que al menos una acción se realice.
    

## B. Sintaxis Anidada y Legibilidad

Aunque puedes anidar, el **Zen de Python** dicta: _"Flat is better than nested"_ (Plano es mejor que anidado).

- **Mala práctica:** Un `if` dentro de otro `if` dentro de otro `if`.
    
- **Solución:** Uso de **cláusulas de guarda** (guard clauses) para retornar o saltar errores temprano, manteniendo el flujo principal en el nivel de indentación más bajo.
    

---

# 3. Funcionalidades Avanzadas de Python

## A. Encadenamiento de Comparaciones (Comparison Chaining)

Python traduce internamente `a < b < c` como `(a < b) and (b < c)`.

- **Detalle técnico:** A diferencia de la versión expandida con `and`, en el encadenamiento `b` se evalúa **una sola vez**. Esto es crucial si `b` es una función con efectos secundarios, como `a < funcion_costosa() < c`.
    

## B. El Operador Ternario (Expresión Condicional)

No es una estructura de control tradicional, sino una **expresión**. Esto significa que devuelve un valor y puede ser parte de otra instrucción.

- **Sintaxis:** `[valor_si_true] if [condicion] else [valor_si_false]`
    
- **Limitación:** No admite `elif`. Para múltiples condiciones, se pueden anidar ternarios (aunque se vuelve ilegible rápidamente): `x if c1 else y if c2 else z`.
    

---

# 4. Patrones de Comparación Especiales

## `is` vs `==` (Identidad vs Igualdad)

Es un error común en condicionales:

- **`==`**: Llama a `__eq__()`. Compara si los **valores** son iguales.
    
- **`is`**: Compara si los objetos son la **misma instancia** en memoria (sus IDs son iguales).
    
    - _Uso correcto:_ `if x is None:`.
        

## Membresía (`in`)

Muy potente en condicionales para limpiar código:

- `if color == "rojo" or color == "azul" or color == "verde":` ❌
    
- `if color in {"rojo", "azul", "verde"}:` ✅ (Mucho más rápido si usas un set).
    

---

## Notas para tu Obsidian

> [!ABSTRACT]
> 
> **Resumen técnico:**
> 
> 1. Las condicionales usan el protocolo de verdad (`__bool__`).
>     
> 2. `and` y `or` son perezosos (lazy evaluation).
>     
> 3. El encadenamiento de comparaciones es más eficiente que usar `and` explícito.
>     
> 4. Prefiere `is` para comparar con `None` y `in` para múltiples opciones.
>     

¿Qué te parece esta profundidad? Si estás satisfecho, el siguiente paso natural en estructuras de control es el **Match-Case (Pattern Matching)**, introducido en Python 3.10, que es como un "if-elif" con esteroides. ¿Lo añadimos?