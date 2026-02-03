---
title: Valores Truthy y Falsy
draft: false
---


En Python, cualquier valor puede ser evaluado en un contexto booleano (como en una condición  [[01 Condicionales|`if` o `while`]]). Los valores que se evalúan como **`False`** se llaman **falsy**, y los que se evalúan como **`True`** se llaman **truthy**.

# `bool`: Una Subclase de `int`

`bool` (booleano) es una subclase de `int` (entero):
- `True` es equivalente al entero `1`
- `False` es equivalente al entero `0`

```python
# bool como subclase de int
print(isinstance(True, int))  # True
print(isinstance(False, int)) # True

print(int(True))   # 1
print(int(False))  # 0

print(True + True)    # 2
print(True + False)   # 1
print(False + False)  # 0
```

# Valores Falsy (se evalúan como `False`)

```python
falsy_values = [
    False,      # El booleano False
    None,       # El valor nulo
    0,          # Entero cero
    0.0,        # Float cero
    0j,         # Número complejo cero
    "",         # String vacío
    [],         # Lista vacía
    {},         # Diccionario vacío
    (),         # Tupla vacía
    set(),      # Conjunto vacío
    range(0),   # Range vacío
    b'',        # Bytes vacío
    bytearray(b''),  # Bytearray vacío
    memoryview(b''), # Memoryview vacío
]

# Verificación
for value in falsy_values:
    if not value:
        print(f"✓ {repr(value)} es Falsy")
    else:
        print(f"✗ {repr(value)} es Truthy")
```

# Valores Truthy (se evalúan como `True`)

```python
truthy_values = [
    True,        # El booleano True
    1,           # Cualquier número distinto de cero
    -1,          
    0.1,         # Float no cero
    3.14,
    "a",         # String no vacío
    "False",     # El string "False" es truthy
    " ",         # String con espacios
    [1],         # Lista no vacía
    [0],         # Lista con elemento 0 (el 0 es falsy, pero la lista no)
    {1: 2},      # Diccionario no vacío
    (1,),        # Tupla no vacía
    {1},         # Conjunto no vacío
    range(1),    # Range no vacío
    object(),    # Cualquier objeto
]

# Verificación
for value in truthy_values:
    if value:
        print(f"✓ {repr(value)} es Truthy")
    else:
        print(f"✗ {repr(value)} es Falsy")
```

# Ejemplos Prácticos

##  Uso en [[01 Condicionales|Condiciones]]

```python
# Verificar si una lista tiene elementos
lista = []
if lista:
    print("La lista tiene elementos")
else:
    print("La lista está vacía")  # Este se ejecuta

# Verificar si un string no está vacío
nombre = ""
if nombre:
    print(f"Hola, {nombre}")
else:
    print("Nombre no proporcionado")  # Este se ejecuta

# Verificar si un número es distinto de cero
contador = 0
if contador:
    print(f"Contador: {contador}")
else:
    print("Contador es cero")  # Este se ejecuta
```

## Conversiones Explícitas

```python
# Convertir cualquier valor a booleano
print(bool(0))      # False
print(bool(1))      # True
print(bool(""))     # False
print(bool("Hola")) # True
print(bool([]))     # False
print(bool([1,2]))  # True
```

## Casos Especiales Interesantes

```python
# Cuidado con estos casos
print(bool("False"))  # True (string no vacío)
print(bool("0"))      # True (string no vacío)
print(bool(" "))      # True (string con espacio)
print(bool(float('nan')))  # True (NaN es truthy)
print(bool(float('0.0')))  # False

# En estructuras de datos
print(bool([0]))      # True (lista no vacía)
print(bool({0: False})) # True (diccionario no vacío)
```

## Uso con [[Operadores de Variables|Operadores Lógicos]]

```python
# Short-circuit evaluation
def obtener_nombre():
    print("Función llamada")
    return "Juan"

nombre = ""
# Como nombre es falsy, se evalúa obtener_nombre()
resultado = nombre or obtener_nombre()
print("Resultado:", resultado)  # "Juan"

# Valor por defecto
config = {}
puerto = config.get('puerto') or 8080
print("Puerto:", puerto)  # 8080

# Validación múltiple
datos = {"nombre": "Ana", "edad": 25}
if datos.get("nombre") and datos.get("edad"):
    print("Datos completos")
```

# Reglas Importantes

1. **Colecciones vacías** son falsy
2. **Cadenas vacías** son falsy
3. **Número cero** (en cualquier tipo) es falsy
4. **`None`** siempre es falsy
5. **Casi todo lo demás** es truthy

# Consejos de Uso

**Buenas Practicas:**

```python
# En lugar de:
if len(lista) > 0:
    pass

# Usa:
if lista:
    pass

# En lugar de:
if nombre != "":
    pass

# Usa:
if nombre:
    pass

# En lugar de:
if valor is not None and valor != 0:
    pass

# Usa (si 0 no es un valor válido):
if valor:
    pass
```

# Casos de Borde
> [!error] Importante
> Leer esta parte con conocimiento de [[POO|POO]]


**Cuidado con estos casos especiales con [[Clases y Objetos|Clases y Objetos]]**
```python
class MiClase:
    def __len__(self):
        return 0  # Hace que la instancia sea falsy
    
    def __bool__(self):
        return False  # Sobrescribe __len__

obj = MiClase()
print(bool(obj))  # False (por __bool__)

# Sin __bool__, Python usa __len__
class OtraClase:
    def __len__(self):
        return 0

obj2 = OtraClase()
print(bool(obj2))  # False (por __len__)
```

