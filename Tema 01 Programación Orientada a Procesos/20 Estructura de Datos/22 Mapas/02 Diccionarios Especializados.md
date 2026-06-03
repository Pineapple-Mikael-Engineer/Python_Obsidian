---
title: 02 Diccionarios Especializados
draft: false
tags: [python, teoria, diccionarios]
---

# Diccionarios Especializados

Variantes de `dict` provistas por el módulo [[Modulo y Paquetes|collections]] que extienden el comportamiento base con valores por defecto automáticos, reordenamiento explícito, conteo de frecuencias, encadenamiento de contextos y subclasificación segura. Para el `dict` base, sus métodos, comprensiones y la fusión con `|`, ver [[01 Diccionarios|Diccionarios]].

## Resumen comparativo

| Tipo | Hereda de | Caso de uso | Aporte clave sobre `dict` |
|------|-----------|-------------|---------------------------|
| `defaultdict` | `dict` | Agrupar, contar, evitar `KeyError` | Crea el valor faltante con un factory al acceder |
| `Counter` | `dict` | Frecuencias, multiconjuntos | `most_common`, aritmética `+ - & \|`, `elements` |
| `OrderedDict` | `dict` | Reordenamiento explícito, LRU, igualdad por orden | `move_to_end`, `popitem(last=)`, `==` sensible al orden |
| `ChainMap` | `MutableMapping` | Capas de scopes/defaults sin copiar | Vista encadenada de varios mapas; `new_child`, `maps` |
| `UserDict` | `MutableMapping` | Subclasear un dict de forma fiable | Datos reales en `.data`; intercepta todos los accesos |

> [!info] `defaultdict`, `Counter` y `OrderedDict` heredan de `dict` (son `isinstance(x, dict)`). `ChainMap` y `UserDict` **no**: son mapeos que envuelven o agregan `dict`s.

## 1. `collections.defaultdict`

Subclase de `dict` que recibe un `default_factory` (un callable sin argumentos). Al acceder a una clave inexistente con `d[k]`, invoca `default_factory()`, **inserta** el resultado bajo `k` y lo devuelve. Si `default_factory` es `None`, se comporta como `dict` y lanza `KeyError`.

```python
from collections import defaultdict

# defaultdict con tipo por defecto
conteo = defaultdict(int)  # int() devuelve 0
palabras = ["manzana", "banana", "manzana", "naranja", "banana", "manzana"]

for palabra in palabras:
    conteo[palabra] += 1

print(f"Conteo palabras: {dict(conteo)}")  # {'manzana': 3, 'banana': 2, 'naranja': 1}

# defaultdict con lista
grupos = defaultdict(list)
datos = [("A", 1), ("B", 2), ("A", 3), ("C", 4), ("B", 5)]

for clave, valor in datos:
    grupos[clave].append(valor)

print(f"Grupos: {dict(grupos)}")  # {'A': [1, 3], 'B': [2, 5], 'C': [4]}

# defaultdict con función personalizada
def valor_por_defecto():
    return "desconocido"

dic_personalizado = defaultdict(valor_por_defecto)
dic_personalizado["a"] = "conocido"
print(f"Personalizado: {dic_personalizado['a']}")      # conocido
print(f"Personalizado: {dic_personalizado['b']}")      # desconocido
```

### Factories habituales y patrones

| Factory | `d[clave_nueva]` produce | Patrón |
|---------|--------------------------|--------|
| `int` | `0` | Contar / acumular sumas |
| `list` | `[]` | Agrupar elementos en listas |
| `set` | `set()` | Agrupar sin duplicados |
| `dict` | `{}` | Mapas anidados / matrices dispersas |
| `lambda: valor` | `valor` | Constante por defecto |
| `lambda: defaultdict(int)` | `defaultdict(int)` | Anidamiento de profundidad fija |

```python
from collections import defaultdict

# Agrupar sin duplicados con set
adyacencia = defaultdict(set)
aristas = [("A", "B"), ("A", "B"), ("A", "C"), ("B", "C")]
for u, v in aristas:
    adyacencia[u].add(v)
print(dict(adyacencia))  # {'A': {'B', 'C'}, 'B': {'C'}}

# Diccionario anidado de 2 niveles (matriz dispersa)
matriz = defaultdict(lambda: defaultdict(int))
matriz[0][3] = 7
print(matriz[0][3])  # 7
print(matriz[9][9])  # 0  (filas/columnas creadas al vuelo)
```

> [!warning] El acceso por lectura **muta** el diccionario: `d[clave_ausente]` inserta la clave. Si solo quieres consultar sin crear, usa `d.get(clave)` o el operador `in`. Tras un bucle de agrupación es común que existan claves "vacías" creadas por lecturas accidentales.

> [!tip] `default_factory` es un atributo reasignable. Asignarlo a `None` desactiva la creación automática y restaura el `KeyError` del `dict` base:
> ```python
> grupos.default_factory = None
> grupos["X"]  # KeyError: 'X'
> ```
> Para crear con argumentos que dependan de la clave, `defaultdict` no sirve: sobrescribe `__missing__` en una subclase de `dict`.

## 2. `collections.Counter`

Subclase de `dict` para conteo de objetos hashables (un multiconjunto). Las claves son los elementos; los valores, sus cuentas (enteros, que pueden ser cero o negativos). El acceso a una clave ausente devuelve `0` **sin** insertarla ni lanzar `KeyError`.

```python
from collections import Counter

# Contar elementos de una secuencia
texto = "abracadabra"
contador = Counter(texto)
print(f"Contador texto: {contador}")
print(f"Letra más común: {contador.most_common(1)}")  # [('a', 5)]
print(f"Las 3 más comunes: {contador.most_common(3)}")

# Operaciones con Counter
c1 = Counter("abracadabra")
c2 = Counter("alacazam")

print(f"\nc1: {c1}")
print(f"c2: {c2}")
print(f"c1 + c2: {c1 + c2}")    # Suma
print(f"c1 - c2: {c1 - c2}")    # Resta (solo positivos)
print(f"c1 & c2: {c1 & c2}")    # Intersección (mínimos)
print(f"c1 | c2: {c1 | c2}")    # Unión (máximos)

# Actualizar Counter
c = Counter()
c.update("abc")
c.update("bcd")
print(f"\nActualizado: {c}")  # Counter({'b': 2, 'c': 2, 'a': 1, 'd': 1})

# Contar palabras en texto
texto_largo = "el gato caza ratones y el perro ladra al gato"
palabras = texto_largo.split()
contador_palabras = Counter(palabras)
print(f"\nPalabras más comunes: {contador_palabras.most_common(3)}")
```

### Construcción e introspección

```python
from collections import Counter

# 4 formas de construir
Counter("aab")               # Counter({'a': 2, 'b': 1})  desde iterable
Counter(["x", "x", "y"])     # Counter({'x': 2, 'y': 1})
Counter({"a": 3, "b": 1})    # Counter({'a': 3, 'b': 1})  desde mapeo
Counter(a=3, b=1)            # Counter({'a': 3, 'b': 1})  desde kwargs

c = Counter(a=4, b=2, c=0, d=-2)

# elements(): reexpande cada elemento según su cuenta (ignora cuentas <= 0)
print(sorted(c.elements()))  # ['a', 'a', 'a', 'a', 'b', 'b']

# total(): suma de todas las cuentas (3.10+)
print(c.total())             # 4

# most_common sin argumento: todos, ordenados de mayor a menor
print(c.most_common())       # [('a', 4), ('b', 2), ('c', 0), ('d', -2)]
print(c.most_common()[-2:])  # los 2 menos comunes
```

### Aritmética de contadores

| Operación | Significado | Conserva |
|-----------|-------------|----------|
| `c1 + c2` | Suma de cuentas | Resultados `> 0` |
| `c1 - c2` | Resta de cuentas | Resultados `> 0` |
| `c1 & c2` | Mínimo por clave (intersección) | Resultados `> 0` |
| `c1 \| c2` | Máximo por clave (unión) | Resultados `> 0` |
| `+c` (unario) | Descarta cuentas `<= 0` | Resultados `> 0` |
| `-c` (unario) | Niega y descarta `<= 0` | Resultados `> 0` |

```python
from collections import Counter

c = Counter(a=3, b=-1, c=0)
print(+c)  # Counter({'a': 3})   filtra cuentas no positivas

# Operadores binarios filtran ceros/negativos; los in-place NO
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=1)
print(c1 - c2)        # Counter({'a': 2})  'b':0 se descarta
c1.subtract(c2)       # in-place: permite cuentas negativas/cero
print(c1)             # Counter({'a': 2, 'b': 0})
```

> [!warning] Distinción clave entre métodos y operadores:
> - `update()` / `subtract()` modifican **in-place** y **permiten** cuentas cero o negativas.
> - `+`, `-`, `&`, `|` crean un **nuevo** `Counter` y **descartan** toda cuenta `<= 0`.
> Para deduplicar y obtener un set de elementos presentes con cuenta positiva: `set(+c)`.

## 3. `collections.OrderedDict`

Subclase de `dict` que recuerda el orden de inserción. Desde Python 3.7 `dict` también lo garantiza, pero `OrderedDict` aporta reordenamiento explícito (`move_to_end`), `popitem` por ambos extremos e igualdad **sensible al orden**, útil para colas, caches LRU y comparaciones donde el orden es semántico.

```python
from collections import OrderedDict

# En Python 3.7+, dict mantiene orden, pero OrderedDict tiene métodos adicionales
od = OrderedDict()
od["z"] = 1
od["a"] = 2
od["m"] = 3

print(f"OrderedDict: {od}")
print(f"Claves en orden: {list(od.keys())}")

# Mover elementos al final
od.move_to_end("z")
print(f"Después move_to_end('z'): {list(od.keys())}")

# Mover al principio
od.move_to_end("a", last=False)
print(f"Después move_to_end('a', last=False): {list(od.keys())}")

# Último elemento
ultimo_clave, ultimo_valor = od.popitem()
print(f"popitem(): ({ultimo_clave}, {ultimo_valor})")

# Primer elemento
primer_clave, primer_valor = od.popitem(last=False)
print(f"popitem(last=False): ({primer_clave}, {primer_valor})")

# Comparación de orden
od1 = OrderedDict([("a", 1), ("b", 2)])
od2 = OrderedDict([("b", 2), ("a", 1)])
print(f"¿Mismo orden?: {od1 == od2}")  # False (orden diferente)
```

### `OrderedDict` vs `dict` (3.7+)

| Característica | `dict` | `OrderedDict` |
|---------------|--------|---------------|
| Mantiene orden de inserción | Sí (3.7+) | Sí |
| `move_to_end(k, last=)` | No | Sí |
| `popitem(last=)` por ambos extremos | Solo último (LIFO) | Sí, ambos |
| `od1 == od2` sensible al orden | No (compara contenido) | Sí, frente a otro `OrderedDict` |
| Reasignar valor mueve la clave | No | No |
| Coste de memoria | Menor | Mayor |

```python
from collections import OrderedDict

# Igualdad asimétrica: OrderedDict vs dict ignora orden
od = OrderedDict([("a", 1), ("b", 2)])
print(od == {"b": 2, "a": 1})  # True   (frente a dict normal: solo contenido)

od_otro = OrderedDict([("b", 2), ("a", 1)])
print(od == od_otro)           # False  (frente a OrderedDict: también orden)

# Cache LRU mínima con move_to_end + popitem(last=False)
class LRU(OrderedDict):
    def __init__(self, cap):
        super().__init__()
        self.cap = cap
    def get(self, k):
        if k not in self:
            return None
        self.move_to_end(k)          # marca como recién usado
        return self[k]
    def put(self, k, v):
        if k in self:
            self.move_to_end(k)
        self[k] = v
        if len(self) > self.cap:
            self.popitem(last=False)  # expulsa el menos usado

cache = LRU(2)
cache.put("a", 1); cache.put("b", 2)
cache.get("a")        # 'a' pasa a recién usado
cache.put("c", 3)     # expulsa 'b' (el más antiguo sin uso)
print(list(cache))    # ['a', 'c']
```

> [!note] Para una cache LRU lista para producción usa `functools.lru_cache`. `OrderedDict` es la base cuando necesitas control manual del reordenamiento o políticas distintas de expulsión.

## 4. `collections.ChainMap`

Agrupa varios mapeos en una **vista** única y actualizable, sin copiarlos. Las búsquedas recorren los mapas en orden (el primero gana); las escrituras, borrados y `popitem` afectan **solo al primer mapa**. Ideal para capas de configuración: línea de comandos → entorno → defaults.

```python
from collections import ChainMap, UserDict

# ChainMap - múltiples diccionarios como uno solo
defaults = {"tema": "claro", "idioma": "es"}
personalizado = {"tema": "oscuro"}

config = ChainMap(personalizado, defaults)
print(f"ChainMap tema: {config['tema']}")      # oscuro (de personalizado)
print(f"ChainMap idioma: {config['idioma']}")  # es (de defaults)

# Añadir nuevo contexto
config = config.new_child({"tema": "auto"})
print(f"Nuevo tema: {config['tema']}")
```

### Capas, escrituras y `parents`

```python
from collections import ChainMap

cli      = {"verbose": True}
entorno  = {"verbose": False, "host": "localhost"}
defaults = {"verbose": False, "host": "0.0.0.0", "puerto": 8000}

cfg = ChainMap(cli, entorno, defaults)
print(cfg["host"])     # localhost  (entorno gana sobre defaults)
print(cfg["puerto"])   # 8000       (solo en defaults)
print(list(cfg.maps))  # [cli, entorno, defaults]

# Las escrituras van SIEMPRE al primer mapa (cli), nunca a las capas inferiores
cfg["host"] = "remoto"
print(cli)             # {'verbose': True, 'host': 'remoto'}
print(entorno)         # {'verbose': False, 'host': 'localhost'}  intacto

# new_child añade una capa al frente; parents la quita
hijo = cfg.new_child({"verbose": False})
print(hijo["verbose"])           # False
print(hijo.parents["verbose"])   # True   (vista sin el primer mapa)

# Simular scopes (global/local) con valores únicos
combinado = dict(cfg)            # aplana resolviendo prioridades
print("puerto" in combinado)     # True
```

> [!warning] `del cfg[k]` y `cfg.pop(k)` solo operan sobre `maps[0]`. Si la clave existe únicamente en una capa inferior, lanzan `KeyError` aunque `k in cfg` sea `True`. `ChainMap` no copia los mapas: mutarlos por fuera se refleja en la vista.

## 5. `collections.UserDict`

Envoltorio en Python puro alrededor de un `dict` real expuesto como atributo `.data`. Pensado para **subclasear**: a diferencia de heredar de `dict`, garantiza que sobrescribir `__getitem__`/`__setitem__`/`__delitem__` afecte a todos los accesos (incluidos `update`, `get`, el constructor y `|`), porque los métodos del mapeo delegan en esos tres.

```python
from collections import UserDict

# UserDict - para crear diccionarios personalizados
class DiccionarioSiemprePositivo(UserDict):
    """Diccionario que convierte valores negativos a positivos."""

    def __setitem__(self, key, value):
        if isinstance(value, (int, float)) and value < 0:
            value = abs(value)
        super().__setitem__(key, value)

dp = DiccionarioSiemprePositivo()
dp["a"] = -5
dp["b"] = 10
dp["c"] = -3.14
print(f"\nDiccionario positivo: {dp}")  # {'a': 5, 'b': 10, 'c': 3.14}
```

### Por qué `UserDict` y no heredar de `dict`

Heredar de `dict` es frágil: sus métodos en C **no** se enrutan por tus overrides. Si redefines `__setitem__`, el `update()` o el constructor de `dict` siguen escribiendo sin pasar por él.

```python
from collections import UserDict

# Heredar de dict: __setitem__ se SALTA en update/constructor
class DictRoto(dict):
    def __setitem__(self, k, v):
        super().__setitem__(k, v.upper())

d = DictRoto()
d["a"] = "hola"
print(d["a"])               # HOLA   (funciona el acceso directo)
d.update({"b": "mundo"})
print(d["b"])               # mundo  (¡no se transformó!)

# UserDict: todos los caminos pasan por __setitem__
class DictBien(UserDict):
    def __setitem__(self, k, v):
        super().__setitem__(k, v.upper())

u = DictBien({"a": "hola"})  # el constructor también enruta
u.update({"b": "mundo"})
print(u["a"], u["b"])        # HOLA MUNDO
print(u.data)                # {'a': 'HOLA', 'b': 'MUNDO'}  dict real subyacente
```

| Base | Métodos enrutados por overrides | Datos en | Velocidad | Cuándo |
|------|--------------------------------|----------|-----------|--------|
| `dict` | Solo accesos directos `d[k]` | el objeto | Máxima (C) | Sin override de acceso, o solo añadir métodos |
| `UserDict` | Todos (delegan en los dunder) | `.data` | Menor (puro Python) | Interceptar/validar todos los accesos de forma fiable |

> [!tip] Si solo quieres **añadir** métodos sin alterar el almacenamiento, heredar de `dict` es válido y más rápido. Usa `UserDict` cuando necesites que validaciones o transformaciones se apliquen en **cualquier** ruta de escritura/lectura. Alternativa estándar: heredar de `collections.abc.MutableMapping` e implementar los métodos abstractos.
