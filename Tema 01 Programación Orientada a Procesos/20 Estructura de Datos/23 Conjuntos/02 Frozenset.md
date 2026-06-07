---
title: Frozenset
order: 2
draft: false
tags:
  - python
  - teoria
  - conjuntos
---
# Frozenset

El `frozenset` es la **variante inmutable** del `set`: una colección **no ordenada y sin duplicados** de elementos hashables que, al carecer de métodos de mutación (`add`, `remove`, `update`…), es ella misma **hashable**. Esa propiedad lo habilita como **clave de diccionario** o como **elemento de otro set**, usos imposibles para un `set` normal. Soporta todas las operaciones de conjunto que no modifican (`|`, `&`, `-`, `^`, comparaciones), que devuelven nuevos `frozenset`.

```python
fs = frozenset([1, 2, 3])           # versión inmutable y hashable
hash(fs)                            # válido: frozenset es hashable
```

## set vs frozenset

| Característica            | `set`                          | `frozenset`                       |
| ------------------------ | ------------------------------ | --------------------------------- |
| Mutable                  | Sí                             | No                                |
| Hashable                 | No                             | Sí                                |
| Clave de `dict`          | No (`TypeError`)               | Sí                                |
| Elemento de otro `set`   | No (`TypeError`)               | Sí                                |
| Literal de sintaxis      | `{1, 2}`                       | No tiene; solo `frozenset(...)`   |
| `add` / `remove` / `pop` | Sí                             | No (`AttributeError`)             |
| `update` / `\|=` / `&=`  | Sí                             | No                                |
| `\|`, `&`, `-`, `^`      | Devuelven `set`                | Devuelven `frozenset`             |
| Comparaciones (`<=`, …)  | Sí                             | Sí                                |
| Orden interno            | No ordenado                    | No ordenado                       |

> [!info] Regla de hashabilidad
> Un objeto es hashable si su `hash()` no cambia durante su vida. Como `frozenset` no admite mutación, su hash es estable y se puede indexar. El hash de un `frozenset` se deriva de los hashes de sus elementos, por lo que `frozenset([1, 2]) == frozenset([2, 1])` y comparten hash (el orden de inserción es irrelevante).

```python
a = frozenset([3, 1, 2])
b = frozenset([1, 2, 3])
print(a == b)               # True  -> no ordenado, mismos elementos
print(hash(a) == hash(b))   # True  -> hash estable e independiente del orden
print(a is b)               # False -> objetos distintos, valor igual
```

## Creación y propiedades

El constructor `frozenset(iterable)` consume cualquier iterable y descarta duplicados. Sin argumento produce el frozenset vacío. No existe literal: `{}` es un `dict` vacío, no un frozenset.

```python
# Creación de frozenset
fs1 = frozenset([1, 2, 3, 4])
fs2 = frozenset({3, 4, 5, 6})
fs3 = frozenset("hola")

print(f"Frozenset desde lista: {fs1}")
print(f"Frozenset desde set: {fs2}")
print(f"Frozenset desde string: {fs3}")
print(f"Tipo: {type(fs1)}")

# Frozenset vacío
fs_vacio = frozenset()
print(f"Frozenset vacío: {fs_vacio}")    # frozenset()

# Inmutabilidad
try:
    fs1.add(5)  # Error
except AttributeError as e:
    print(f"Error al intentar modificar: {e}")

try:
    fs1.remove(1)  # Error
except AttributeError as e:
    print(f"Error al intentar eliminar: {e}")
```

> [!warning] Solo elementos hashables
> Igual que el `set`, un `frozenset` no puede contener objetos mutables. `frozenset([[1, 2]])` lanza `TypeError: unhashable type: 'list'`. Para anidar conjuntos, los elementos internos deben ser a su vez `frozenset`.

### Métodos que SÍ existen vs los que NO

`frozenset` expone toda la API de **consulta** y de **operación que devuelve un nuevo conjunto**, pero ninguno de los métodos mutantes del `set`.

| Disponibles (`frozenset`)                          | Ausentes (solo en `set`)                    |
| -------------------------------------------------- | ------------------------------------------- |
| `union`, `intersection`, `difference`              | `add`, `remove`, `discard`, `pop`, `clear`  |
| `symmetric_difference`                             | `update`, `intersection_update`             |
| `issubset`, `issuperset`, `isdisjoint`             | `difference_update`                         |
| `copy`, `len()`, `in`, iteración                   | `symmetric_difference_update`               |

```python
fs = frozenset([1, 2, 3])
print(set(dir(fs)) & {"add", "remove", "update"})   # set()  -> ninguno existe
print(fs.copy() is fs)   # True (opcional) -> copy() de un frozenset devuelve el mismo objeto
```

## Frozenset como clave de diccionario

El uso canónico: indexar por **el contenido de un conjunto**, ignorando el orden. Un `set` normal no sirve porque no es hashable.

```python
# Frozenset puede ser clave (set normal no puede)
diccionario_con_sets = {}

# Intentar con set normal
try:
    diccionario_con_sets[{1, 2}] = "valor"  # Error
except TypeError as e:
    print(f"Error con set como clave: {e}")  # unhashable type: 'set'

# Con frozenset funciona
diccionario_con_frozenset = {
    frozenset([1, 2]): "conjunto A",
    frozenset([3, 4]): "conjunto B",
    frozenset([5, 6]): "conjunto C"
}

print("Diccionario con frozenset como claves:")
for conjunto, valor in diccionario_con_frozenset.items():
    print(f"  {conjunto} -> {valor}")

# Acceso: el orden de la clave no importa
clave_busqueda = frozenset([4, 3])          # mismo valor que frozenset([3, 4])
print(f"Valor para {clave_busqueda}: {diccionario_con_frozenset[clave_busqueda]}")
# -> "conjunto B"
```

## Frozenset como elemento de set

Permite construir un **conjunto de conjuntos** (set de sets). El `set` interno debe ser `frozenset`; los duplicados por valor se colapsan automáticamente.

```python
# Set de frozensets (set normal no puede contener sets)
conjunto_de_conjuntos = set()

# Intentar añadir set normal
try:
    conjunto_de_conjuntos.add({1, 2})  # Error
except TypeError as e:
    print(f"Error al añadir set a set: {e}")  # unhashable type: 'set'

# Con frozenset funciona
conjunto_de_conjuntos.add(frozenset([1, 2]))
conjunto_de_conjuntos.add(frozenset([3, 4]))
conjunto_de_conjuntos.add(frozenset([2, 1]))  # Duplicado por valor, no se añade

print(f"Set de frozensets ({len(conjunto_de_conjuntos)} elementos):")
for elemento in conjunto_de_conjuntos:
    print(f"  {elemento}")

# Útil para conjuntos de conjuntos
poderes = {
    frozenset(["volar", "invisibilidad"]),
    frozenset(["super fuerza", "rayos láser"]),
    frozenset(["volar", "super velocidad"]),
}

print("\nCombinaciones de poderes:")
for poderes_combinados in poderes:
    print(f"  {poderes_combinados}")
```

## Operaciones de conjunto

Todos los operadores de teoría de conjuntos están disponibles y son **cerrados sobre `frozenset`**: aplicados a frozensets devuelven un nuevo `frozenset`, sin mutar los operandos.

```python
fs1 = frozenset([1, 2, 3, 4])
fs2 = frozenset([3, 4, 5, 6])

# Las operaciones devuelven nuevos frozensets
union = fs1 | fs2
interseccion = fs1 & fs2
diferencia = fs1 - fs2
diff_sim = fs1 ^ fs2

print(f"fs1: {fs1}")
print(f"fs2: {fs2}")
print(f"Unión: {union}")                    # frozenset({1, 2, 3, 4, 5, 6})
print(f"Intersección: {interseccion}")      # frozenset({3, 4})
print(f"Diferencia: {diferencia}")          # frozenset({1, 2})
print(f"Diferencia simétrica: {diff_sim}")  # frozenset({1, 2, 5, 6})

# Comparaciones
print(f"¿fs1 es subconjunto de fs1? {fs1 <= fs1}")      # True
print(f"¿fs1 es subconjunto de union? {fs1 <= union}")  # True
print(f"¿fs1 y fs2 son disjuntos? {fs1.isdisjoint(fs2)}")  # False

# Equivalencia operador / método
nuevo = fs1.union(fs2)
print(f"fs1.union(fs2): {nuevo}")           # frozenset({1, 2, 3, 4, 5, 6})
```

> [!info] Tipo del resultado según los operandos
> El tipo devuelto lo fija el operando **izquierdo** en la forma de método, o el primer operando en la forma de operador. `frozenset | set` devuelve `frozenset`; `set | frozenset` devuelve `set`. Para garantizar un resultado inmutable, parte de un `frozenset` o envuelve con `frozenset(...)`.

```python
fs = frozenset([1, 2])
s  = {2, 3}
print(type(fs | s))   # <class 'frozenset'>
print(type(s | fs))   # <class 'set'>
```

## Casos de uso

### Caché de conjuntos como clave

> [!tip] Cachear conjuntos como claves
> Convierte un `set` en `frozenset` cuando necesites usarlo como clave de un caché o como elemento de otro set: `frozenset(conjunto)` produce un objeto hashable equivalente.

```python
cache = {}
def procesar_conjunto(conjunto):
    conjunto_hashable = frozenset(conjunto)  # Para usar como clave
    if conjunto_hashable in cache:
        return cache[conjunto_hashable]      # hit: evita recálculo
    resultado = sum(conjunto)                # cómputo costoso simulado
    cache[conjunto_hashable] = resultado
    return resultado

print(procesar_conjunto({1, 2, 3}))   # 6  (miss -> calcula y guarda)
print(procesar_conjunto({3, 2, 1}))   # 6  (hit -> mismo frozenset)
```

### Conjuntos constantes

Un `frozenset` a nivel de módulo expresa una constante que no debe modificarse por accidente, con la misma búsqueda O(1) que un `set`.

```python
VOCALES = frozenset("aeiou")
PALABRAS_RESERVADAS = frozenset({"if", "else", "for", "while", "def"})

def es_vocal(c):
    return c in VOCALES          # pertenencia O(1), inmune a mutación externa

print(es_vocal("a"))             # True
print("def" in PALABRAS_RESERVADAS)  # True
```

### Aristas y pares no ordenados

`frozenset({u, v})` modela una arista no dirigida: la clave es la misma para `{u, v}` y `{v, u}`.

```python
visitadas = set()
def visitar_arista(u, v):
    arista = frozenset({u, v})
    if arista in visitadas:
        return "ya recorrida"
    visitadas.add(arista)
    return "nueva"

print(visitar_arista("A", "B"))   # nueva
print(visitar_arista("B", "A"))   # ya recorrida  -> orden irrelevante
```

---

Las operaciones de teoría de conjuntos, *comprehensions* y métodos de mutación del `set` mutable se tratan en [[01 Sets|set]].
