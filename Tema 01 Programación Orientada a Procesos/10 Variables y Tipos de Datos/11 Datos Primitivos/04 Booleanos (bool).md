---
title: 04 Booleanos (bool)
draft: false
tags: [python, teoria, booleanos]
---

# Booleanos-`bool`
El tipo `bool` representa valores de **lógica binaria**. Se utiliza para evaluar si una condición es verdadera o falsa, siendo la base de todas las [[30 Estructuras de Control/index | estructuras de control]] (como los `if` y los `while`). Solo puede tener dos valores:
- **`True`** (Verdadero)
- **`False`** (Falso)

> [!note] Notate
>  En Python, los valores booleanos deben escribirse siempre con la **primera letra en mayúscula**, caso contrario lanzará un error de nombre.
>  ```python
>  a = True   # True con mayusculas, Bien
>  b = true   # true con minusculas, Mal -> NameError: name 'true' is not defined
>  ```

`True` y `False` son las **únicas dos instancias** del tipo `bool`; son singletons, por lo que se comparan con `is` de forma segura. La identidad es estable durante toda la ejecución:

```python
type(True)        # <class 'bool'>
True is True      # True
bool.__instancecheck__  # solo True y False son instancias
```

## True/False como subclase de `int`
Python se diferencia de otros lenguajes: **un booleano es técnicamente un número entero**.

Históricamente, Python no tenía un tipo booleano dedicado y usaba `0` para falso y `1` para verdadero. Cuando se introdujo el tipo `bool` (PEP 285, Python 2.3), se hizo como una **subclase de [[01 Enteros (int) | int]]** para mantener la compatibilidad hacia atrás.

```python
issubclass(bool, int)   # True
isinstance(True, int)   # True
True == 1               # True
False == 0              # True
True == 2               # False
```

**Evidencias de esta relación:**

1. **Valores numéricos:** `True` equivale a `1` y `False` equivale a `0`.
2. **Operaciones aritméticas:** Puedes realizar cálculos matemáticos con booleanos (aunque no es una práctica recomendada por legibilidad).
    - `True + True` → `2`
    - `True * 10` → `10`
    - `False - 5` → `-5`

> [!warning] `True == 1` pero `True is not 1`
> La **igualdad** (`==`) es `True` porque comparan valor numérico. La **identidad** (`is`) es `False` porque son objetos distintos. Como consecuencia, `1` y `True` colisionan como claves de diccionario (mismo hash y mismo `==`):
> ```python
> {1: "a", True: "b"}     # {1: 'b'} -> True sobrescribe la clave 1
> {0: "x", False: "y"}    # {0: 'y'}
> ```

### Suma y conteo de bools
Como `True == 1` y `False == 0`, sumar un iterable de booleanos **cuenta cuántos son verdaderos**. Es el idioma estándar para contar elementos que cumplen una condición:

```python
notas = [12, 8, 15, 4, 18, 9]
aprobados = sum(n >= 11 for n in notas)   # 3  -> cuenta los True
ratio = sum(n >= 11 for n in notas) / len(notas)   # 0.5

# Equivale a, pero más conciso que:
len([n for n in notas if n >= 11])        # 3
```

> [!tip] `int(bool)` y `bool(int)`
> La conversión es directa en ambos sentidos: `int(True)` → `1`, `int(False)` → `0`. A la inversa, `bool(0)` → `False` y `bool(cualquier_otro)` → `True`.

## La función `bool()`

`bool(x)` convierte cualquier objeto a su valor de verdad invocando su protocolo de truthiness (`__bool__` o, en su defecto, `__len__`). Sin argumentos, `bool()` → `False`.

| Entrada            | `bool(...)` | Regla aplicada                          |
| ------------------ | ----------- | --------------------------------------- |
| `bool()`           | `False`     | sin argumento                           |
| `0`, `0.0`, `0j`   | `False`     | cero numérico                           |
| `42`, `-1`, `3.14` | `True`      | número distinto de cero                 |
| `""`               | `False`     | cadena vacía (`__len__ == 0`)           |
| `"False"`, `"0"`   | `True`      | cadena no vacía (¡el contenido da igual!)|
| `[]`, `()`, `{}`, `set()` | `False` | contenedor vacío                      |
| `[0]`, `{"k": None}` | `True`    | contenedor no vacío                     |
| `None`             | `False`     | objeto nulo                             |

```python
bool("False")   # True  -> es una cadena no vacía, NO el booleano False
bool(" ")       # True  -> un espacio cuenta como contenido
bool(0.0)       # False
bool([0])       # True  -> la lista no está vacía aunque contenga un 0
```

> [!warning] Trampa clásica
> `bool("False")` es `True`. Para parsear texto a booleano nunca uses `bool(texto)`; compara explícitamente: `texto.strip().lower() == "true"`.

El detalle completo de qué objetos son verdaderos o falsos se desarrolla en [[Valores Truthy y Falsy | truthiness]].

## Operadores lógicos

Los operadores `and`, `or` y `not` combinan o niegan valores según su truthiness.

| Operador | Función                                    | Ejemplo                   |
| -------- | ------------------------------------------ | ------------------------- |
| `and`    | Verdadero solo si **ambos** lo son.        | `True and False` → `False`|
| `or`     | Verdadero si **al menos uno** lo es.       | `True or False` → `True`  |
| `not`    | Niega (invierte) el valor.                 | `not True` → `False`      |

### Tabla de verdad

| `a`     | `b`     | `a and b` | `a or b` | `not a` |
| ------- | ------- | --------- | -------- | ------- |
| `False` | `False` | `False`   | `False`  | `True`  |
| `False` | `True`  | `False`   | `True`   | `True`  |
| `True`  | `False` | `False`   | `True`   | `False` |
| `True`  | `True`  | `True`    | `True`   | `False` |

### Evaluación en cortocircuito (*short-circuit*)
Python evalúa las expresiones lógicas de **izquierda a derecha** y se detiene en cuanto el resultado queda determinado:

- **`and`:** Si el primer operando es falsy, el resultado ya está decidido; el segundo operando **no se evalúa**.
- **`or`:** Si el primer operando es truthy, el resultado ya está decidido; el segundo operando **no se evalúa**.

El cortocircuito permite usar el segundo operando como **guarda** para evitar errores o trabajo costoso:

```python
# El segundo operando solo se evalúa si el primero no cortocircuita
def caro():
    print("ejecutado")
    return True

False and caro()   # False -> "ejecutado" NO se imprime
True or caro()     # True  -> "ejecutado" NO se imprime

usuario is not None and usuario.activo   # no accede a .activo si es None
datos and procesar(datos)                # no procesa si datos está vacío
```

### `and`/`or` devuelven un operando (no un `bool`)

A diferencia de otros lenguajes, `and` y `or` **no devuelven `True`/`False`**, sino **el operando** que decidió el resultado. El valor conserva su tipo original.

| Expresión | Devuelve | Regla |
| --------- | -------- | ----- |
| `a and b` | `a` si `a` es falsy; si no, `b` | primer falsy, o el último |
| `a or b`  | `a` si `a` es truthy; si no, `b` | primer truthy, o el último |

```python
0 and 5          # 0      -> primer operando es falsy, lo devuelve
3 and 5          # 5      -> primero truthy, devuelve el segundo
0 or 5           # 5      -> primero falsy, devuelve el segundo
3 or 5           # 3      -> primero truthy, lo devuelve
"" or "default"  # 'default'
[] or [0]        # [0]
```

**Patrones idiomáticos:**

```python
nombre = entrada or "Anónimo"        # valor por defecto si entrada es falsy
config = usuario and usuario.config  # encadenamiento seguro: None si usuario es falsy
puerto = puerto_arg or os.environ.get("PORT") or 8080   # primer truthy de la cadena
```

> [!warning] `x or default` falla con falsy válidos
> `x or default` reemplaza **cualquier** valor falsy, no solo `None`. Si `0`, `""` o `[]` son valores legítimos, los pisará. Para distinguir "ausencia" de "falsy", usa una comprobación explícita:
> ```python
> cantidad = 0
> cantidad or 100         # 100  -> ¡pisa el 0 válido!
> cantidad if cantidad is not None else 100   # 0  -> correcto
> ```

## Lógicos (`and`/`or`) vs bit a bit (`&`/`|`/`^`)

Con operandos `bool`, los operadores **bit a bit** producen el mismo resultado de verdad que los lógicos, pero **no cortocircuitan** (evalúan siempre ambos lados) y **devuelven un `bool`**, no un operando. Con `int` operan sobre los bits.

| Aspecto              | `and` / `or` / `not`        | `&` / `|` / `^` / `~`           |
| -------------------- | --------------------------- | ------------------------------- |
| Tipo de operación    | lógica (truthiness)         | bit a bit (sobre enteros)       |
| Cortocircuito        | sí                          | no (evalúa ambos lados)         |
| Valor devuelto       | un operando (tipo original) | `bool` con bools; `int` con ints |
| Precedencia          | baja                        | **alta** (mayor que `==`, `<`)  |
| `^` (XOR)            | no existe lógico nativo     | sí: verdadero si difieren       |

```python
True & False     # False   (bool)
True | False     # True    (bool)
True ^ True      # False   (XOR: iguales -> False)
True ^ False     # True    (difieren -> True)
~True            # -2      (¡bit a bit sobre int! ~1 == -2, NO False)

5 & 3            # 1   -> 0b101 & 0b011 = 0b001
```

> [!warning] Precedencia: paréntesis obligatorios
> `&` y `|` tienen **mayor** precedencia que los comparadores. `a == 1 & b == 2` se parsea como `a == (1 & b) == 2`, casi nunca lo que se quiere. Con condiciones, usa `and`/`or` o **encierra cada comparación**:
> ```python
> # Pandas/NumPy fuerzan & y | (no aceptan and/or sobre arrays):
> df[(df.edad > 18) & (df.activo)]   # paréntesis imprescindibles
> ```

> [!info] Usa `^` para "exactamente uno"
> No existe un `xor` lógico. Para "exactamente uno de dos verdadero" sobre bools, `a ^ b` es el idioma directo. Si los operandos no son bool, normalízalos: `bool(a) ^ bool(b)`.

## `any()` y `all()` sobre iterables

Generalizan `or` y `and` a un iterable completo, aplicando truthiness a cada elemento. Ambos **cortocircuitan** y devuelven un `bool`.

| Función      | Devuelve `True` si...                  | Iterable vacío | Cortocircuita en |
| ------------ | -------------------------------------- | -------------- | ---------------- |
| `any(it)`    | **al menos un** elemento es truthy     | `False`        | primer truthy    |
| `all(it)`    | **todos** los elementos son truthy     | `True`         | primer falsy     |

```python
any([0, "", None, 5])     # True   -> 5 es truthy
all([1, "x", [0]])        # True   -> todos truthy
all([1, 0, 3])            # False  -> el 0 corta
any([])                   # False  -> vacío
all([])                   # True   -> vacuamente verdadero ("vacuous truth")

# Con generadores, evalúan condiciones sin construir la lista:
all(n > 0 for n in [3, 5, 1])      # True
any(c.isdigit() for c in "abc3")   # True   -> corta en el '3'
```

> [!tip] Encontrar el primer elemento, no solo si existe
> `any(...)` solo dice *si* hay un truthy. Para obtener *cuál*, usa `next(filter(None, it), default)` o `next((x for x in it if cond(x)), default)`.

> [!info] `all([])` es `True`
> Sobre un iterable vacío, `all` devuelve `True` (no hay contraejemplo) y `any` devuelve `False` (no hay testigo). Tenlo presente al validar colecciones que podrían venir vacías.

## La lógica de la "Verdad" ([[Valores Truthy y Falsy | Truthiness]])

Dado que los booleanos son números, Python extiende este concepto a otros tipos de datos. Casi cualquier objeto en Python puede evaluarse en un contexto booleano:

- **Valores que equivalen a `False`:**
    - El número `0` (`0`, `0.0`, `0j`).
    - [[20 Estructura de Datos/index | Contenedores vacíos]] (`""`, `[]`, `()`, `{}`).
    - El valor `None`.
- **Valores que equivalen a `True`:**
    - Cualquier número distinto de cero.
    - Cualquier cadena o contenedor que no esté vacío.

> [!note] Nota
> Si se desea entender mejor la logica de "Verdad" de Python, revisar: [[Valores Truthy y Falsy | Valores Truthy y Falsy]]
