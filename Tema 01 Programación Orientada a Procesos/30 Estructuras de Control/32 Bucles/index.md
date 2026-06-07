---
title: Bucles
order: 32
draft: false
tags: [python, teoria, bucles]
---

# Bucles

Un bucle (o ciclo) es una estructura de control que ejecuta un bloque de código repetidamente mientras se cumple una condición o para cada elemento de una secuencia. Son la base para automatizar tareas repetitivas y procesar colecciones de datos. Python ofrece dos construcciones según la naturaleza de la iteración:

- **Bucles definidos** ([[02 For | for]]): el número de repeticiones queda determinado por el iterable que se recorre. Se usan cuando se conocen los elementos a procesar.
- **Bucles indefinidos** ([[01 While | while]]): repiten mientras una condición sea verdadera, sin saber de antemano cuántas vueltas harán falta. La salida depende de un estado cambiante.

## Iterables e Iteradores

Un **iterable** es cualquier objeto sobre el que se puede recorrer con `for` (listas, tuplas, cadenas, diccionarios, conjuntos, `range`). Internamente, `for` obtiene un **iterador** del iterable y le pide elementos uno a uno hasta agotarlo; al consumir el último, el bucle termina sin necesidad de gestionar índices ni condiciones a mano. El `while`, en cambio, no recorre un iterable: evalúa una condición booleana antes de cada vuelta.

## Delegación

- [[01 While | while]] — iteración indefinida controlada por condición: sintaxis, bucles infinitos y cómo evitarlos, inicialización/actualización y `while-else`.
- [[02 For | for]] — iteración definida sobre iterables: `range()`, `enumerate()`, `zip()`, recorrido de diccionarios y `for-else`.
- [[03 Comprensiones | comprensiones]] — construcción de colecciones en una sola expresión: list/dict/set comprehension, filtros, `if`/`else`, comprensiones anidadas, generadores y cuándo conviene frente a un `for` explícito.

## Resumen

| Aspecto | [[01 While \| while]] | [[02 For \| for]] | [[03 Comprensiones \| comprensiones]] |
| --- | --- | --- | --- |
| Tipo de iteración | Indefinida (por condición) | Definida (por iterable) | Definida, en una sola expresión |
| Control de parada | Condición booleana | Agotamiento del iterable | Agotamiento del iterable |
| Cuándo usarlo | No se sabe cuántas vueltas; estado cambiante | Recorrer elementos de una colección | Construir una colección transformando/filtrando |
| Riesgo típico | Bucle infinito (olvidar actualizar) | — | Ilegibilidad si hay demasiados `for`/`if` |
| Cláusula `else` | Se ejecuta si la condición pasa a `False` sin `break` | Se ejecuta si se agota el iterable sin `break` | No aplica |
| Herramientas asociadas | `break`, condición controlada | `range()`, `enumerate()`, `zip()` | list/dict/set, generadores, filtros |

## ¿`for` o `while`?

```python
# USAR FOR CUANDO:
# 1. Sabes cuántas iteraciones necesitas
for i in range(10):
    print(i)

# 2. Estás iterando sobre elementos de una colección
for elemento in lista:
    procesar(elemento)

# 3. Necesitas procesar cada elemento una vez
for char in "Python":
    print(char)

# USAR WHILE CUANDO:
# 1. No sabes cuántas iteraciones necesitas
respuesta = ""
while respuesta != "salir":
    respuesta = input("Comando: ")

# 2. La condición depende de un estado cambiante
segundos = 10
while segundos > 0:
    print(f"Tiempo restante: {segundos}s")
    segundos -= 1
    time.sleep(1)

# 3. Necesitas un bucle infinito controlado
while True:
    evento = obtener_evento()
    if evento == "terminar":
        break
    procesar(evento)
```

## Ejemplo Completo Integrado

```python
def procesar_inventario(inventario):
    """
    Procesa un inventario usando diferentes tipos de bucles
    """
    print("=== PROCESANDO INVENTARIO ===")
    
    # for con enumerate para mostrar posición
    for idx, (producto, cantidad) in enumerate(inventario.items(), 1):
        print(f"{idx}. {producto}: {cantidad} unidades")
    
    print("\n=== PRODUCTOS BAJOS EN STOCK ===")
    # for-else para buscar productos con stock bajo
    for producto, cantidad in inventario.items():
        if cantidad < 5:
            print(f"ALERTA: {producto} tiene solo {cantidad} unidades")
            break
    else:
        print("Todos los productos tienen stock suficiente")
    
    print("\n=== ACTUALIZANDO STOCK ===")
    # while para reponer stock
    productos_a_reponer = ["manzanas", "naranjas"]
    
    for producto in productos_a_reponer:
        if producto in inventario:
            stock_actual = inventario[producto]
            objetivo = 20
            
            print(f"\nReponiendo {producto}...")
            while stock_actual < objetivo:
                print(f"  Stock actual: {stock_actual}, agregando 5...")
                stock_actual += 5
                inventario[producto] = stock_actual
            
            print(f"  {producto} repuesto a {stock_actual} unidades")
    
    return inventario

# Inventario inicial
inventario = {
    "manzanas": 15,
    "bananas": 8,
    "naranjas": 3,
    "peras": 10
}

# Procesar
inventario_actualizado = procesar_inventario(inventario)

print("\n=== INVENTARIO FINAL ===")
for producto, cantidad in inventario_actualizado.items():
    print(f"{producto}: {cantidad} unidades")
```

## Mejores Prácticas

1. **Usa `for` para iterar sobre elementos conocidos**
2. **Usa `while` para condiciones dinámicas o desconocidas**
3. **Siempre inicializa y actualiza variables en `while`**
4. **Utiliza `enumerate()` para obtener índice y valor**
5. **Usa `zip()` para iterar múltiples secuencias**
6. **Aprovecha `for-else`/`while-else` para casos de "no encontrado"**
7. **Evita bucles infinitos asegurando condiciones de salida**
8. **Prefiere `range()` con `len()` en lugar de índices manuales**
9. **Documenta bucles complejos**
10. **Considera comprensiones de listas para transformaciones simples**
