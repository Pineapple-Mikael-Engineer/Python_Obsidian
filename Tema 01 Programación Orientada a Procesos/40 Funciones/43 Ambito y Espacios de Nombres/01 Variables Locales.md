---
title: Variables Locales
order: 1
tags:
  - python
  - teoria
  - ambito
draft: false
aliases:
  - Local variables
  - Variables de función
---

# Variables Locales

> [!definicion]
> Una **variable local** es aquella que se crea dentro de una función mediante una asignación. Solo existe mientras la función se ejecuta y solo es accesible dentro de ella. Su tiempo de vida está acotado por la llamada: nace en la primera asignación y se destruye al retornar la función.

> [!info]
> El intérprete decide en *tiempo de compilación* del cuerpo de la función qué nombres son locales: cualquier nombre que reciba una asignación en cualquier punto del cuerpo se trata como local en toda la función (salvo declaración `global` o `nonlocal`).

---

## Definición y alcance acotado

```python
def procesar_datos():
    # Variables locales
    nombre_local = "Carlos"
    edad_local = 30
    resultado = nombre_local + " tiene " + str(edad_local) + " años"
    return resultado

print(procesar_datos())  # Carlos tiene 30 años

# Intentar acceder a variable local fuera de la función
try:
    print(nombre_local)  # ❌ NameError
except NameError as e:
    print(f"Error: {e}")
```

El nombre `nombre_local` no existe fuera del cuerpo de `procesar_datos`; el acceso externo lanza `NameError`.

---

## Tiempo de vida: recreación en cada llamada

Las variables locales se reinician en cada invocación. No conservan estado entre llamadas.

```python
# Las variables locales se crean en cada llamada
def contador():
    cuenta = 0  # Se reinicia en cada llamada
    cuenta += 1
    print(f"Cuenta: {cuenta}")

contador()  # Cuenta: 1
contador()  # Cuenta: 1 (otra vez 1, no 2)
contador()  # Cuenta: 1
```

```python
def ciclo_vida():
    # Variable local: nace aquí
    temp = [1, 2, 3]
    print(f"Dentro: {temp}")
    # Variable local: muere al salir

ciclo_vida()
# temp ya no existe
```

Cada llamada construye y descarta sus propios objetos locales:

```python
# Las variables locales se crean y destruyen
def crear_lista():
    lista_local = [x for x in range(1000)]
    return len(lista_local)

for i in range(5):
    print(f"Llamada {i}: {crear_lista()} elementos")
    # Cada llamada crea y destruye una lista nueva
```

> [!info]
> Persistir estado entre llamadas sin recurrir a variables de módulo se logra con closures sobre el ámbito *enclosing* (ver [[04 Nonlocal | nonlocal]] y [[08 Closures | closures]]).

---

## Ocultamiento de globales (shadowing)

Una variable local con el mismo nombre que una global **oculta** a la global dentro de la función. Son objetos distintos; la asignación local no afecta a la global.

```python
# Variable global
mensaje = "Hola desde global"

def funcion_ambito():
    # Variable local con el mismo nombre
    mensaje = "Hola desde local"
    print("Dentro de función:", mensaje)

print("Fuera:", mensaje)    # Fuera: Hola desde global
funcion_ambito()            # Dentro: Hola desde local
print("Fuera:", mensaje)    # Fuera: Hola desde global (sin cambios)
```

La diferencia se confirma comparando identidades: el nombre local y el global referencian objetos diferentes.

```python
# Demostración de que son variables diferentes
def demostrar_id():
    x = 10
    print(f"ID local x: {id(x)}")

x = 5
print(f"ID global x: {id(x)}")
demostrar_id()  # ID diferente
```

---

## UnboundLocalError: asignación tras lectura

> [!warning]
> Si un nombre recibe una asignación en cualquier punto del cuerpo, Python lo trata como local en *toda* la función. Leerlo antes de esa asignación lanza `UnboundLocalError`, aunque exista una global con el mismo nombre.

```python
contador = 0

def problema():
    # Python ve una asignación, asume que contador es local
    contador += 1  # ❌ UnboundLocalError
    return contador

def solucion1():
    global contador
    contador += 1
    return contador

def solucion2(contador):
    contador += 1
    return contador

try:
    problema()
except UnboundLocalError as e:
    print(f"Error: {e}")

print(f"Solución1: {solucion1()}")  # 1
print(f"Solución2: {solucion2(5)}")  # 6 (no modifica global)
```

La asignación `contador += 1` equivale a `contador = contador + 1`: la parte derecha lee un `contador` que el intérprete ya clasificó como local pero que aún no fue asignado. Las soluciones son declarar [[02 Variables Globales | global]] o recibir el valor por parámetro.

---

## Relación con otras notas

- El nombre que oculta una local se resuelve por la [[03 Regla LEGB | regla LEGB]], donde *Local* es el primer nivel consultado.
- Promover una local a global para modificarla se trata en [[02 Variables Globales | Variables Globales]].
- Capturar y modificar variables del ámbito contenedor (no global) se trata en [[04 Nonlocal | Nonlocal]].
