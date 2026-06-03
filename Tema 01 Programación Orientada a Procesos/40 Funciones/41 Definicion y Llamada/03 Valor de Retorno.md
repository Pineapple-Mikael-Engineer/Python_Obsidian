---
title: Valor de Retorno
tags:
  - python
  - teoria
  - funciones
draft: false
aliases:
  - return
  - None implícito
---

# Valor de Retorno

`return` finaliza la ejecución de la función y entrega un valor a quien la llamó. Una función sin `return` —o que llega al final sin ejecutarlo— retorna `None` de forma implícita. La llamada es una expresión cuyo valor es ese retorno.

```python
# Función que retorna un valor
def suma(a, b):
    resultado = a + b
    return resultado

# El valor retornado puede asignarse
total = suma(5, 3)
print(f"Total: {total}")

# Return inmediato
def es_par(numero):
    return numero % 2 == 0

print(es_par(4))  # True
print(es_par(5))  # False

# Return condicional
def clasificar_edad(edad):
    if edad < 0:
        return "Edad inválida"
    if edad < 18:
        return "Menor de edad"
    if edad < 65:
        return "Adulto"
    return "Jubilado"

print(clasificar_edad(15))   # Menor de edad
print(clasificar_edad(30))   # Adulto
print(clasificar_edad(70))   # Jubilado
```

## Return Múltiple (Tuplas Implícitas)

`return a, b, c` no devuelve "varios valores": construye una **tupla** con ellos. En el destino, la **asignación múltiple** la desempaqueta en variables individuales, o puede recibirse como tupla completa.

```python
# Retornar múltiples valores (como tupla)
def operaciones_basicas(a, b):
    suma = a + b
    resta = a - b
    multiplicacion = a * b
    division = a / b if b != 0 else None
    return suma, resta, multiplicacion, division

# Asignación múltiple
s, r, m, d = operaciones_basicas(10, 3)
print(f"Suma: {s}, Resta: {r}, Mult: {m}, Div: {d}")

# También se puede recibir como tupla
resultados = operaciones_basicas(10, 3)
print(f"Tupla: {resultados}")
print(f"Suma: {resultados[0]}")

# Otro ejemplo común
def dividir_con_resto(dividendo, divisor):
    cociente = dividendo // divisor
    resto = dividendo % divisor
    return cociente, resto

coc, res = dividir_con_resto(17, 5)
print(f"17 ÷ 5 = {coc} (resto {res})")
```

## `None` como Retorno Implícito

Sin `return` explícito, o con un `return` sin valor, la función entrega `None` (tipo `NoneType`). La comprobación correcta usa `is None` / `is not None`, no `==`.

```python
# Función sin return explícito → retorna None
def mostrar_mensaje(mensaje):
    print(mensaje)
    # No hay return

resultado = mostrar_mensaje("Hola")
print(f"Resultado: {resultado}")  # None
print(f"Tipo: {type(resultado)}")  # <class 'NoneType'>

# Return explícito de None
def validar_positivo(numero):
    if numero > 0:
        return True
    # Equivalente a: return None
    # También explícito: return None

# Verificar None
def procesar_si_valido(valor):
    if valor is not None:  # Comparación correcta con None
        print(f"Procesando: {valor}")
    else:
        print("Valor no válido")

procesar_si_valido(validar_positivo(5))   # Procesando: True
procesar_si_valido(validar_positivo(-3))  # Valor no válido
```

## Return Temprano (Early Return)

Validar condiciones y retornar al inicio evita anidamiento profundo y aclara el flujo. Un patrón frecuente devuelve un par `(resultado, error)` donde `None` en una posición señala ausencia.

```python
def procesar_usuario(usuario):
    """Ejemplo de early returns para claridad."""
    
    # Validaciones tempranas
    if not usuario:
        return None, "Usuario vacío"
    
    if not usuario.get("nombre"):
        return None, "Nombre requerido"
    
    if usuario.get("edad", 0) < 18:
        return None, "Debe ser mayor de edad"
    
    # Procesamiento principal
    resultado = f"Usuario {usuario['nombre']} procesado"
    return resultado, None  # None indica sin error

# Uso
usuarios = [
    {},
    {"nombre": "Ana"},
    {"nombre": "Juan", "edad": 15},
    {"nombre": "Carlos", "edad": 25}
]

for usuario in usuarios:
    resultado, error = procesar_usuario(usuario)
    if error:
        print(f"Error: {error}")
    else:
        print(f"Éxito: {resultado}")
```

## Return de Funciones (Closures)

El valor de retorno puede ser otra función. Una función definida dentro de otra captura las variables del entorno donde fue creada (**closure**), lo que permite fabricar funciones especializadas.

```python
# Función que retorna otra función
def crear_multiplicador(factor):
    """Retorna una función que multiplica por factor."""
    def multiplicador(x):
        return x * factor
    return multiplicador

# Crear funciones específicas
duplicar = crear_multiplicador(2)
triplicar = crear_multiplicador(3)

print(duplicar(5))   # 10
print(triplicar(5))  # 15

# Función que retorna múltiples funciones
def crear_operaciones():
    def suma(a, b):
        return a + b
    
    def resta(a, b):
        return a - b
    
    return suma, resta  # Retorna las funciones

suma_func, resta_func = crear_operaciones()
print(suma_func(10, 5))   # 15
print(resta_func(10, 5))  # 5
```

> [!info] Tipos de retorno
> El tipo del valor retornado depende de los datos en `[[02 Parametros y Argumentos | parámetros]]` que recibe. Para documentar el tipo de salida se usan *type hints*: `def dividir_con_resto(d: int, v: int) -> tuple[int, int]:`.
