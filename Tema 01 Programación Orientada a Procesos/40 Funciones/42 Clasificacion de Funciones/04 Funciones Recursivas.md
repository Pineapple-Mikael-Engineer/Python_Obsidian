---
title: 04 Funciones Recursivas
draft: false
tags:
  - python
  - teoria
  - funciones
---
# Funciones Recursivas

Una **función recursiva** se llama a sí misma durante su ejecución. Requiere siempre dos partes: un **caso base** que detiene la recursión y un **caso recursivo** que progresa hacia él. Python impone un límite de profundidad de pila (~1000 por defecto).

## Estructura básica

```python
# Toda función recursiva necesita:
# 1. Caso base (condición de parada)
# 2. Caso recursivo (llamada a sí misma)

def cuenta_regresiva(n):
    """Ejemplo simple de recursión."""
    # Caso base
    if n <= 0:
        print("¡Despegue!")
        return

    # Caso recursivo
    print(n)
    cuenta_regresiva(n - 1)

cuenta_regresiva(5)
# 5
# 4
# 3
# 2
# 1
# ¡Despegue!
```

## Factorial

```python
def factorial(n):
    """
    Calcula el factorial de n (n!)

    Caso base: factorial(0) = 1
    Caso recursivo: factorial(n) = n * factorial(n-1)
    """
    # Caso base
    if n <= 1:
        return 1

    # Caso recursivo
    return n * factorial(n - 1)

# Pruebas
print(factorial(5))   # 120 (5*4*3*2*1)
print(factorial(0))   # 1
print(factorial(1))   # 1

# Visualización del proceso
def factorial_detallado(n, nivel=0):
    """Versión con traza."""
    indent = "  " * nivel
    print(f"{indent}factorial({n}) - Inicio")

    if n <= 1:
        print(f"{indent}  Caso base: retorna 1")
        return 1

    print(f"{indent}  Llamando a factorial({n-1})")
    resultado_parcial = factorial_detallado(n - 1, nivel + 1)
    resultado = n * resultado_parcial

    print(f"{indent}  {n} * {resultado_parcial} = {resultado}")
    print(f"{indent}factorial({n}) - Retorna {resultado}")
    return resultado

factorial_detallado(4)
```

## Fibonacci y memoización

La versión ingenua de Fibonacci recalcula subproblemas y crece de forma exponencial. La **memoización** cachea resultados ya computados, reduciendo el coste a lineal.

```python
def fibonacci(n):
    """
    Calcula el n-ésimo número de Fibonacci.

    Fibonacci: 0, 1, 1, 2, 3, 5, 8, 13, ...
    Casos base: fib(0) = 0, fib(1) = 1
    Caso recursivo: fib(n) = fib(n-1) + fib(n-2)
    """
    # Casos base
    if n == 0:
        return 0
    if n == 1:
        return 1

    # Caso recursivo
    return fibonacci(n - 1) + fibonacci(n - 2)

# Pruebas
for i in range(10):
    print(f"fib({i}) = {fibonacci(i)}")

# Versión ineficiente (exponencial)
import time

inicio = time.time()
fibonacci(35)
print(f"fib(35) tomó: {time.time() - inicio:.4f}s")

# Versión optimizada con memoización
def fibonacci_memo(n, memo={}):
    """
    Fibonacci con memoización (guardar resultados).
    """
    if n in memo:
        return memo[n]

    if n == 0:
        return 0
    if n == 1:
        return 1

    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]

inicio = time.time()
fibonacci_memo(35)
print(f"fib_memo(35) tomó: {time.time() - inicio:.4f}s")
```

## Recursión en estructuras de datos

La recursión es la forma natural de recorrer estructuras autosimilares (listas anidadas, árboles).

```python
# Suma de elementos en lista anidada
def suma_anidada(lista):
    """Suma todos los números en una lista que puede contener sublistas."""
    total = 0
    for elemento in lista:
        if isinstance(elemento, list):
            total += suma_anidada(elemento)
        else:
            total += elemento
    return total

lista_anidada = [1, 2, [3, 4, [5, 6], 7], 8, [9, 10]]
print(f"Suma anidada: {suma_anidada(lista_anidada)}")  # 55

# Profundidad máxima de anidamiento
def profundidad_maxima(lista, nivel=1):
    """Calcula la máxima profundidad de anidamiento."""
    if not any(isinstance(e, list) for e in lista):
        return nivel

    profundidades = []
    for elemento in lista:
        if isinstance(elemento, list):
            profundidades.append(profundidad_maxima(elemento, nivel + 1))

    return max(profundidades) if profundidades else nivel

print(f"Profundidad máxima: {profundidad_maxima(lista_anidada)}")  # 3

# Aplanar lista anidada
def aplanar(lista):
    """Convierte lista anidada en lista plana."""
    resultado = []
    for elemento in lista:
        if isinstance(elemento, list):
            resultado.extend(aplanar(elemento))
        else:
            resultado.append(elemento)
    return resultado

plana = aplanar(lista_anidada)
print(f"Lista aplanada: {plana}")  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

## Recursión en árboles

```python
# Representación de un árbol binario
class Nodo:
    def __init__(self, valor, izquierdo=None, derecho=None):
        self.valor = valor
        self.izquierdo = izquierdo
        self.derecho = derecho

    def __repr__(self):
        return f"Nodo({self.valor})"

# Crear árbol de ejemplo
arbol = Nodo(10,
    Nodo(5,
        Nodo(3),
        Nodo(7)
    ),
    Nodo(15,
        Nodo(12),
        Nodo(18)
    )
)

# Recorrido in-order (izquierdo, raíz, derecho)
def in_order(nodo):
    """Recorrido in-order del árbol."""
    if nodo is None:
        return []

    resultado = []
    resultado.extend(in_order(nodo.izquierdo))
    resultado.append(nodo.valor)
    resultado.extend(in_order(nodo.derecho))

    return resultado

print(f"In-order: {in_order(arbol)}")  # [3, 5, 7, 10, 12, 15, 18]

# Recorrido pre-order (raíz, izquierdo, derecho)
def pre_order(nodo):
    if nodo is None:
        return []

    resultado = [nodo.valor]
    resultado.extend(pre_order(nodo.izquierdo))
    resultado.extend(pre_order(nodo.derecho))

    return resultado

print(f"Pre-order: {pre_order(arbol)}")  # [10, 5, 3, 7, 15, 12, 18]

# Recorrido post-order (izquierdo, derecho, raíz)
def post_order(nodo):
    if nodo is None:
        return []

    resultado = []
    resultado.extend(post_order(nodo.izquierdo))
    resultado.extend(post_order(nodo.derecho))
    resultado.append(nodo.valor)

    return resultado

print(f"Post-order: {post_order(arbol)}")  # [3, 7, 5, 12, 18, 15, 10]

# Altura del árbol
def altura(nodo):
    """Calcula la altura del árbol."""
    if nodo is None:
        return 0

    return 1 + max(altura(nodo.izquierdo), altura(nodo.derecho))

print(f"Altura: {altura(arbol)}")  # 3

# Buscar valor
def buscar(nodo, valor):
    """Busca un valor en el árbol."""
    if nodo is None:
        return False

    if nodo.valor == valor:
        return True

    return buscar(nodo.izquierdo, valor) or buscar(nodo.derecho, valor)

print(f"¿Existe 7? {buscar(arbol, 7)}")   # True
print(f"¿Existe 20? {buscar(arbol, 20)}") # False
```

## Recursión vs iteración

La recursión es elegante pero más costosa (marcos de pila, riesgo de `RecursionError`). La iteración es más eficiente para secuencias simples.

```python
import time

# Comparación: factorial recursivo vs iterativo
def factorial_recursivo(n):
    if n <= 1:
        return 1
    return n * factorial_recursivo(n - 1)

def factorial_iterativo(n):
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado

# Comparación de rendimiento
n = 500

# Python tiene límite de recursión (~1000)
try:
    inicio = time.time()
    factorial_recursivo(n)
    tiempo_rec = time.time() - inicio
    print(f"Recursivo: {tiempo_rec:.6f}s")
except RecursionError:
    print(f"Recursivo: Error - límite de recursión excedido para {n}")

inicio = time.time()
factorial_iterativo(n)
tiempo_it = time.time() - inicio
print(f"Iterativo: {tiempo_it:.6f}s")

# Comparación: Fibonacci
def fib_recursivo(n):
    if n <= 1:
        return n
    return fib_recursivo(n - 1) + fib_recursivo(n - 2)

def fib_iterativo(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Fibonacci 35
n_fib = 35

inicio = time.time()
fib_recursivo(n_fib)
tiempo_rec = time.time() - inicio

inicio = time.time()
fib_iterativo(n_fib)
tiempo_it = time.time() - inicio

print(f"Fibonacci recursivo ({n_fib}): {tiempo_rec:.4f}s")
print(f"Fibonacci iterativo ({n_fib}): {tiempo_it:.4f}s")

# Conclusión: recursión es más elegante pero menos eficiente
# Usar recursión cuando:
# - La solución recursiva es más natural y clara
# - La profundidad es limitada
# - El problema tiene estructura recursiva (árboles, etc.)
```

## Recursión de cola (tail recursion)

Ocurre cuando la llamada recursiva es la **última operación** de la función. Python **no** optimiza tail calls (no elimina el marco de pila), pero el patrón con acumulador es ampliamente usado en otros lenguajes.

```python
# La recursión de cola ocurre cuando la llamada recursiva es la última operación
# Python NO optimiza la recursión de cola, pero es un concepto importante

# Factorial sin recursión de cola
def factorial_normal(n):
    if n <= 1:
        return 1
    return n * factorial_normal(n - 1)  # No es tail: multiplica después de llamar

# Factorial con recursión de cola
def factorial_cola(n, acumulador=1):
    if n <= 1:
        return acumulador
    return factorial_cola(n - 1, n * acumulador)  # Tail: llamada es última operación

print(factorial_normal(5))   # 120
print(factorial_cola(5))     # 120

# Suma de lista con recursión de cola
def suma_lista_cola(lista, acumulador=0):
    if not lista:
        return acumulador
    return suma_lista_cola(lista[1:], acumulador + lista[0])

print(suma_lista_cola([1, 2, 3, 4, 5]))  # 15
```

## Problemas comunes y límites

```python
# 1. Límite de recursión
def recursión_infinita():
    return recursión_infinita()  # ❌ Eventualmente RecursionError

# 2. Olvidar caso base
def factorial_sin_base(n):
    # Faltó el caso base
    return n * factorial_sin_base(n - 1)  # ❌ Recursión infinita

# 3. No progresar hacia el caso base
def recursión_estancada(n):
    if n <= 0:
        return 0
    # No modifica n adecuadamente
    return n + recursión_estancada(n)  # ❌ Nunca llega al caso base

# 4. Solución: siempre verificar
def factorial_seguro(n):
    """Factorial con validación."""
    if not isinstance(n, int) or n < 0:
        raise ValueError("n debe ser entero no negativo")

    if n <= 1:
        return 1

    return n * factorial_seguro(n - 1)

# 5. Usar sys.setrecursionlimit para aumentar límite
import sys
print(f"Límite actual: {sys.getrecursionlimit()}")
sys.setrecursionlimit(5000)  # Aumentar límite (con cuidado)
print(f"Nuevo límite: {sys.getrecursionlimit()}")
```

## Buenas prácticas

```python
# ✅ Siempre tener caso base claro
def contar_hasta(n):
    if n <= 0:  # Caso base
        return
    print(n)
    contar_hasta(n - 1)  # Progresión hacia caso base

# ✅ Considerar iteración para problemas profundos
# Recursión para árboles
def recorrer_arbol(nodo):
    if nodo is None:
        return
    print(nodo.valor)
    recorrer_arbol(nodo.izquierdo)
    recorrer_arbol(nodo.derecho)

# Iteración para secuencias simples
def factorial(n):
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado
```
