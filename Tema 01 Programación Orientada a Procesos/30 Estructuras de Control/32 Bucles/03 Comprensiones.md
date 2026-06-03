---
title: 03 Comprensiones
draft: false
tags: [python, teoria, bucles]
---

# Comprensiones (Comprehensions)

Una comprensión condensa un bucle `for` que construye una colección en una única expresión. Equivale a un bucle que parte de una colección vacía y acumula con `append`, pero se evalúa como una sola expresión y resulta más rápida al estar optimizada en C.

## Sintaxis General

Las cuatro variantes comparten la misma gramática; cambian solo los delimitadores y la forma de la expresión de cabecera.

| Tipo | Sintaxis | Delimitador | Resultado |
| --- | --- | --- | --- |
| List | `[expr for x in it]` | `[ ]` | `list` |
| Set | `{expr for x in it}` | `{ }` | `set` (sin duplicados) |
| Dict | `{k: v for x in it}` | `{ }` + `:` | `dict` |
| Generator | `(expr for x in it)` | `( )` | `generator` (perezoso) |

La estructura completa, en orden de lectura, es:

```text
[ expr   for x1 in it1   if c1   for x2 in it2   if c2   ... ]
  ▲       └── cláusula 1 ──┘      └── cláusula 2 ──┘
  expresión de salida (1 obligatoria)   (cláusulas for/if: ≥1 for, 0+ if)
```

- La **expresión de salida** se evalúa una vez por combinación que sobreviva a los filtros.
- Cada `for` abre un nivel de bucle; cada `if` (tras un `for`) filtra ese nivel.
- El **scope** de la variable de iteración está aislado: desde Python 3 no se filtra al ámbito exterior (en Py2 sí contaminaba). Internamente la comprensión se compila como una función anónima propia.

```python
x = "intacto"
_ = [x for x in range(3)]
print(x)  # 'intacto'  -> la x del bucle no pisa la externa
```

## List Comprehension

```python
# Sintaxis: [expresión for elemento in iterable]
cuadrados = [x ** 2 for x in range(5)]
# [0, 1, 4, 9, 16]

# Equivalente con for explícito
cuadrados = []
for x in range(5):
    cuadrados.append(x ** 2)
```

### Con Filtro

La cláusula `if` al final descarta los elementos que no satisfacen la condición.

```python
# Sintaxis: [expresión for elemento in iterable if condición]
pares = [x for x in range(10) if x % 2 == 0]
# [0, 2, 4, 6, 8]

# Múltiples filtros encadenados (AND implícito)
filtrados = [x for x in range(30) if x % 2 == 0 if x % 3 == 0]
# [0, 6, 12, 18, 24]
```

### Con `if`/`else` en la Expresión

Cuando el `if`/`else` aparece **antes** del `for`, no filtra: es un operador ternario que decide el valor de cada elemento.

```python
# Sintaxis: [valor_si else valor_no for elemento in iterable]
etiquetas = ["par" if x % 2 == 0 else "impar" for x in range(5)]
# ['par', 'impar', 'par', 'impar', 'par']
```

> [!warning] Posición del `if`
> El `if` **al final** (tras el `for`) filtra elementos; el `if`/`else` **antes** del `for` transforma valores. No se pueden confundir: `[x if cond for x in it]` es un error de sintaxis, porque un filtro no admite `else`.

## Comprensiones Anidadas

### Orden de los `for` = Orden de Anidamiento

Los `for` se escriben en el **mismo orden** en que se escribirían los bucles anidados equivalentes: el primer `for` es el bucle externo, el último el más interno. Cada `for` puede referirse a las variables de los `for` anteriores (pero no al revés).

```python
# [expr  for a in A  for b in B]  ≡  bucle externo a, interno b
combos = [(a, b) for a in [1, 2] for b in ["x", "y"]]
# [(1, 'x'), (1, 'y'), (2, 'x'), (2, 'y')]
#   b varía rápido (interno), a varía lento (externo)

# El for interno depende del externo (triángulo)
pares = [(i, j) for i in range(4) for j in range(i)]
# [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2)]
```

> [!warning] Aplanar invierte la intuición del lector novato
> En `[x for fila in matriz for x in fila]` el `for fila` (externo) va **primero** aunque la expresión de salida `x` provenga del `for` interno. Se lee igual que el bucle anidado, no al contrario.

### Aplanar una Matriz

```python
matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Aplanar: [expr for sub in matriz for x in sub]
plano = [x for fila in matriz for x in fila]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Equivalente con for explícito
plano = []
for fila in matriz:
    for x in fila:
        plano.append(x)
```

### Construir una Matriz

Una comprensión interna como expresión genera cada sublista.

```python
# Matriz [[expr for ...] for ...]
tabla = [[i * j for j in range(1, 4)] for i in range(1, 4)]
# [[1, 2, 3], [2, 4, 6], [3, 6, 9]]

# Transponer una matriz
transpuesta = [[fila[i] for fila in matriz] for i in range(len(matriz[0]))]
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```

## Dict y Set Comprehension

La misma sintaxis se extiende a [[01 Diccionarios | diccionarios]] y [[01 Sets | conjuntos]] usando llaves `{}`.

```python
# Dict comprehension: {clave: valor for ...}
cuadrados = {x: x ** 2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Invertir un diccionario
original = {"a": 1, "b": 2}
invertido = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b'}

# Set comprehension: {expr for ...} (elimina duplicados)
unicos = {x % 3 for x in range(10)}
# {0, 1, 2}
```

## Generator Expression

Sustituir los corchetes por paréntesis `(expr for x in it)` produce un **generador**: no construye la colección, sino un iterador que produce cada valor bajo demanda (evaluación perezosa). No reserva memoria proporcional al tamaño del resultado; solo guarda el estado del bucle.

```python
gen = (x ** 2 for x in range(1_000_000))
# <generator object> -> 0 elementos materializados, memoria O(1)

next(gen)  # 0
next(gen)  # 1   -> produce valores uno a uno

# Se consume UNA sola vez: tras agotarlo queda vacío
list(gen)        # [4, 9, ..., 999998^2]
list(gen)        # []  -> ya estaba agotado
```

| Aspecto | List comp `[...]` | Generator exp `(...)` |
| --- | --- | --- |
| Memoria | O(n) — materializa todo | O(1) — un valor a la vez |
| Reutilizable | Sí (es una lista) | No — se agota al iterar |
| Indexable / `len()` | Sí | No |
| Evaluación | Inmediata (eager) | Perezosa (lazy) |
| Cortocircuito | No | Sí — para al primer match |

```python
# Paréntesis redundantes si es el único argumento de la función
total = sum(x ** 2 for x in range(1000))      # sin () extra
any(n < 0 for n in datos)                     # para en el primer negativo
```

> [!tip] Cortocircuito con `any`/`all`
> `any(cond for x in enorme)` deja de iterar en cuanto encuentra un `True`; la versión con lista `any([cond for x in enorme])` construye toda la lista antes. Para búsquedas sobre secuencias grandes, el generador evita trabajo y memoria.

> [!warning] No reutilizar un generador agotado
> Un generador es un iterador de un solo uso. Si necesitas recorrerlo dos veces (`max` y luego `sum`, por ejemplo), usa una lista o crea dos generadores distintos.

## Walrus `:=` en Comprensiones

El operador de asignación-expresión (Python 3.8+) permite **calcular un valor una sola vez** y reutilizarlo en la expresión de salida y/o en el filtro, evitando recalcularlo.

```python
import math

# Sin walrus: f(x) se calcula DOS veces (filtro + salida)
res = [f(x) for x in datos if f(x) > 0]

# Con walrus: se calcula UNA vez por elemento
res = [y for x in datos if (y := f(x)) > 0]
# y queda asignado por cada x que pasa el filtro y se usa como salida
```

```python
# Mantener estado entre iteraciones (acumulado)
valores = [1, 2, 3, 4]
total = 0
acumulados = [total := total + v for v in valores]
# [1, 3, 6, 10]   -> total = 10 al final
```

> [!info] Fuga deliberada del walrus
> A diferencia de la variable del `for`, el nombre asignado con `:=` **sí escapa** al ámbito que envuelve la comprensión. En el último ejemplo, `total` vale `10` después. Es un efecto buscado, pero conviene no abusar por legibilidad.

## Rendimiento vs `for`, `map` y `filter`

```python
# Estos tres producen el mismo resultado
comp   = [x ** 2 for x in range(10)]
mapped = list(map(lambda x: x ** 2, range(10)))
loop   = []
for x in range(10):
    loop.append(x ** 2)
```

| Forma | Velocidad típica | Notas |
| --- | --- | --- |
| List comprehension | Más rápida | Bucle e inserción optimizados en C; sin `append` resuelto por nombre en cada vuelta |
| `for` + `append` | Más lenta | Cada `append` es una búsqueda de atributo + llamada Python |
| `map(func, it)` | Comparable a comp **si `func` ya existe** | Devuelve iterador perezoso; gana al envolver un built-in (`map(str, xs)`) |
| `map(lambda ...)` | Más lenta que comp | El `lambda` añade una llamada Python por elemento, sin la ventaja del C |
| `filter(func, it)` | Similar a `map` | Idem: built-in eficiente, `lambda` penaliza |

Equivalencias `map`/`filter` ↔ comprensión:

```python
# map(f, it)            ≡  [f(x) for x in it]
# filter(p, it)         ≡  [x for x in it if p(x)]
# map(f, filter(p, it)) ≡  [f(x) for x in it if p(x)]

nombres = list(map(str.upper, palabras))    # map con built-in: idiomático y rápido
nombres = [s.upper() for s in palabras]     # comp: igual de claro, sin list()
```

> [!tip] Cuándo gana `map`
> `map` solo aventaja a la comprensión cuando la función ya existe como built-in o referencia (`map(int, tokens)`, `map(str.strip, lineas)`). Si necesitarías un `lambda`, la comprensión es más rápida y más legible.

## Cuándo NO Usar una Comprensión

```python
# MAL: efecto secundario, valor de retorno descartado
[print(x) for x in datos]     # crea una lista de None inútil
# BIEN
for x in datos:
    print(x)

# MAL: sobre-anidamiento ilegible
res = [f(x, y, z) for x in a for y in b for z in c if g(x, y) if h(z)]
# BIEN: bucle explícito por niveles, con nombres y posibilidad de break/continue

# MAL: try/except no cabe en una comprensión
# parsed = [int(t) for t in tokens]   # revienta ante el primer token inválido
# BIEN
parsed = []
for t in tokens:
    try:
        parsed.append(int(t))
    except ValueError:
        continue
```

| Antipatrón | Síntoma | Alternativa |
| --- | --- | --- |
| Efectos colaterales (`print`, I/O, mutación) | Lista de `None` que se tira | `for` explícito |
| Más de 2 `for`/`if` | No se lee de un vistazo | `for` anidado con nombres |
| `try`/`except`, `break`, `continue` | No existen en la sintaxis | `for` explícito |
| Expresión multilínea o con muchos ternarios | Cabe pero ilegible | Extraer función + `map` o `for` |
| Reutilizar el resultado varias veces siendo generador | Se agota tras el primer uso | Materializar a lista |

## Cuándo Usar una Comprensión

| Situación | Recomendación |
| --- | --- |
| Transformar o filtrar produciendo una nueva colección | Comprensión |
| Una sola operación por elemento, expresión corta | Comprensión |
| Más de dos `for`/`if` anidados | `for` explícito |
| El cuerpo tiene efectos secundarios (`print`, escritura en archivo) | `for` explícito |
| Se necesita `break`, `continue` o `try`/`except` | `for` explícito |
| La lógica por elemento no cabe legible en una línea | `for` explícito |

> [!tip] Legibilidad sobre concisión
> Una comprensión mejora la lectura cuando expresa **qué** colección se construye de un vistazo. Si requiere más de dos cláusulas anidadas o la expresión deja de leerse en voz alta como una frase, un `for` explícito comunica mejor la intención. Las comprensiones no se usan por su valor de retorno cuando el objetivo es solo el efecto secundario; en ese caso, un bucle ordinario.
