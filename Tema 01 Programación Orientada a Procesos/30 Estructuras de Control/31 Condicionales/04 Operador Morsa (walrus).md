---
title: Operador Morsa (walrus)
order: 4
draft: false
tags:
  - python
  - teoria
  - condicionales
aliases:
  - Operador Morsa
  - Walrus Operator
  - Assignment Expression
---
# Operador Morsa (Walrus `:=`)

Python 3.8+ ([PEP 572](https://peps.python.org/pep-0572/)) introduce el operador morsa, que permite **asignar y evaluar** en la misma expresión, evitando duplicar el cálculo o la lectura previa. A diferencia de `=` (sentencia de asignación), `:=` es un **operador de expresión** (*assignment expression*): produce el valor asignado **y** lo deja ligado a un nombre, por lo que puede aparecer donde se espera una expresión (condiciones de `if`/`while`, comprehensions, argumentos), no como sentencia independiente.

| | `=` (sentencia) | `:=` (expresión) |
|---|---|---|
| Categoría | Statement | Operador / expresión |
| Devuelve valor | No (no usable en `if x = 5`) | Sí (el valor asignado) |
| Dónde puede ir | Solo a nivel de sentencia | Dentro de cualquier expresión |
| Destino (target) | Nombres, `obj.attr`, `lista[i]`, tuplas, *unpacking* | **Solo nombres simples** |
| Asignación múltiple | `a = b = 0` | No: `(a := b := 0)` es error |
| Aumentada | `x += 1` | No existe `x :+= 1` |

## Sintaxis

```python
(nombre := expresión)
```

La expresión se evalúa, su resultado se asigna a `nombre` y ese mismo resultado queda disponible para la expresión contenedora. El *target* a la izquierda debe ser un **identificador simple**: no se permite *unpacking* ni asignar a atributos o índices.

> [!warning] Los paréntesis casi siempre son obligatorios
> `:=` tiene precedencia muy baja (menor que `,` en muchos contextos). Sin paréntesis, Python interpreta la sentencia como otra cosa o la rechaza. Regla práctica: **envuelve siempre `(nombre := expr)` en paréntesis** salvo en la cabecera desnuda de un `if`/`while` donde no haya operadores alrededor.

```python
if n := len(datos) > 3:      # n = (len(datos) > 3) -> n es bool, NO el largo
if (n := len(datos)) > 3:    # n = len(datos); se compara con 3  (correcto)
```

## Uso en `if`

```python
# Tradicional
entrada = input("Ingresa un número: ")
if entrada.isdigit():
    numero = int(entrada)
    print(f"Número ingresado: {numero}")

# Con morsa: asigna y comprueba en una línea; 'entrada' sobrevive al if
if (entrada := input("Ingresa un número: ")).isdigit():
    print(f"Número ingresado: {int(entrada)}")

lista = [1, 2, 3, 4, 5]
if (n := len(lista)) > 3:
    print(f"La lista tiene {n} elementos, más de 3")   # La lista tiene 5 elementos, más de 3
```

### `if` con match de regex

Caso canónico: `re.match`/`re.search` devuelve un objeto `Match` o `None`. La morsa captura el match para reutilizar sus grupos sin llamar dos veces.

```python
import re

texto = "edad: 42"

# Tradicional: dos llamadas o una variable previa fuera del if
m = re.search(r"(\d+)", texto)
if m:
    print(m.group(1))

# Con morsa: una sola llamada, 'm' disponible dentro del bloque
if (m := re.search(r"(\d+)", texto)):
    print(m.group(1))    # 42

# Encadenado en elif sin anidar
if (m := re.match(r"GET (\S+)", linea)):
    handle_get(m.group(1))
elif (m := re.match(r"POST (\S+)", linea)):
    handle_post(m.group(1))
```

## Uso en `while`

Permite leer-y-comprobar en la propia cabecera del bucle, eliminando la lectura previa duplicada antes y dentro del `while` (patrón *read-ahead*).

```python
# Tradicional: la lectura se repite arriba y al final del cuerpo
linea = archivo.readline()
while linea:
    procesar(linea)
    linea = archivo.readline()

# Con morsa: una sola línea de lectura
while (linea := archivo.readline()):
    procesar(linea)
```

```python
# Consumir un stream / bloques de tamaño fijo
while (bloque := f.read(8192)):
    sha.update(bloque)

# Bucle de entrada con centinela
while (cmd := input("> ")) != "salir":
    ejecutar(cmd)
```

> [!tip] Sustituye a `iter(callable, sentinela)`
> `while (b := f.read(4096)):` es equivalente a `for b in iter(lambda: f.read(4096), b''):` pero más directo cuando el centinela no es un valor fijo único.

## Uso en comprehensions

Reutiliza el resultado de un cálculo dentro de una comprensión sin repetir la llamada en el filtro y en la salida.

```python
# Sin morsa: f(x) se calcula DOS veces por elemento que pasa el filtro
resultados = [f(x) for x in datos if f(x) > 0]

# Con morsa: f(x) se calcula UNA sola vez por elemento
resultados = [y for x in datos if (y := f(x)) > 0]
```

```python
# Filtrar y transformar a la vez reusando un valor intermedio
nombres = ["  ana ", "", "  LEO "]
limpios = [s for n in nombres if (s := n.strip())]   # ['ana', 'LEO']  (descarta '' y "   ")

# Reutilizar en map dentro del cuerpo de la comprensión
distancias = [d for p in puntos if (d := dist(p, origen)) < radio]
```

> [!warning] Fuga de scope en comprehensions
> El nombre asignado con `:=` dentro de una comprensión **no** se confina al ámbito implícito de la comprensión (como sí ocurre con la variable de bucle `x`): se filtra al **scope contenedor**. Tras la línea anterior, `y`, `s` o `d` quedan vivos con el **último** valor evaluado.
> ```python
> resultados = [y for x in range(5) if (y := x * 2) > 4]
> print(resultados)  # [6, 8]
> print(y)           # 8   <- y existe fuera; x NO (NameError)
> ```

## Scope: vive en el bloque contenedor

El nombre ligado por `:=` pertenece al **scope que contiene la expresión**, no a un ámbito propio. En un `if`/`while`/comprehension dentro de una función, el nombre es **local a la función**; a nivel de módulo, es global.

```python
def f():
    if (total := sum(range(10))) > 40:
        ...
    return total          # 45  -> 'total' sigue accesible tras el if

[v for v in range(3) if (w := v + 1)]
# 'w' existe en el scope de f(), aunque la comprensión sí confine 'v'
```

Excepción: dentro de una comprensión usada en el cuerpo de **clase**, asignar con `:=` está **prohibido** (no hay un scope contenedor accesible donde ligar el nombre) y produce `SyntaxError`.

## Prohibiciones y errores comunes

| Caso | Válido | Motivo |
|---|---|---|
| `x := 5` como sentencia suelta | No | Debe ir en una expresión: `(x := 5)` |
| `(x := 5)` como única expresión-sentencia | Sí (pero inútil) | Equivale a `x = 5`; usa `=` |
| `obj.attr := v` | No | Target debe ser nombre simple, no atributo |
| `lista[i] := v` | No | Target debe ser nombre simple, no índice |
| `(a, b := 1, 2)` *unpacking* | No | No admite *tuple targets* |
| `a := b := 0` encadenado | No | Solo un target por `:=` |
| `x :+= 1` | No | No hay forma aumentada |
| `f(x := g())` argumento | Sí | Liga `x` en el scope que llama |
| `def f(x := 0)` valor por defecto | No | Ahí `=` es sintaxis de parámetro, no asignación |
| `:=` en comprensión de cuerpo de clase | No | `SyntaxError`: sin scope contenedor válido |

```python
# Errores típicos
x := 5            # SyntaxError: invalid syntax
total.count := 0  # SyntaxError: cannot use assignment expressions with attribute
a, b := 1, 2      # SyntaxError: cannot use assignment expressions with tuple
```

## Legibilidad: cuándo usarlo y cuándo no

> [!note] Heurística
> Usa `:=` **solo** cuando elimina una **duplicación real** (una lectura, un cálculo costoso o una comprobación repetida) y mantiene la línea legible. Si la expresión crece o el lector debe detenerse a localizar dónde se asignó el nombre, prefiere la asignación previa con `=`.

```python
# Buen uso: elimina llamada duplicada y mantiene foco
if (resp := api.fetch(url)) is not None:
    cache[url] = resp

# Mal uso: anida varias morsas, ilegible
print(total := sum(xs := [g(k) for k in keys]))   # evitar
```

- Aporta cuando: *read-ahead* en `while`, capturar `Match` de regex en `if`, reusar cálculo en una comprehension, evitar una variable temporal de una sola línea.
- Estorba cuando: se anidan dos o más `:=`, se usa solo por ahorrar una línea, o se mezcla con efectos secundarios poco evidentes.

## Relación con otras estructuras

- [[01 If-Elif-Else | If-Elif-Else]]: caso de uso principal junto con regex y validación de entrada.
- [[01 While | While]]: patrón *read-ahead* en la cabecera del bucle.
- [[03 Comprensiones | Comprensiones]]: reuso de cálculo y la fuga de scope asociada.
- [[02 Operador Ternario | Operador Ternario]] y [[03 Match Case | Match Case]]: alternativas/complemento en condicionales compactos.

> [!info] Disponibilidad
> Requiere **Python 3.8+**. En versiones anteriores cualquier `:=` es `SyntaxError`. El acrónimo "morsa" viene de que `:=` recuerda los ojos y colmillos de una morsa vistos de lado.
