---
title: Sintaxis Básica
tags:
  - python
  - teoria
  - funciones
draft: false
aliases:
  - def
  - Definición de funciones
---

# Sintaxis Básica de Funciones

Una **función** es un bloque de código reutilizable identificado por un nombre. Se define con la palabra clave `def`, seguida del nombre, una lista de parámetros entre paréntesis y dos puntos. El cuerpo es un bloque indentado que se ejecuta al **llamar** la función con `nombre()`.

```python
# Estructura más simple
def saludar():
    print("¡Hola, mundo!")

# Función con documentación (docstring)
def despedirse():
    """Esta función imprime una despedida."""
    print("¡Adiós, mundo!")

# Función con cuerpo vacío (útil para esqueletos)
def funcion_futura():
    pass  # Placeholder, no hace nada

# Función con múltiples líneas
def mostrar_info():
    """Muestra información del sistema."""
    print("=== INFORMACIÓN ===")
    print("Versión: 1.0")
    print("Autor: Python Dev")
    print("===================")
```

## Elementos de la Definición

Toda definición consta de cuatro piezas: nombre descriptivo, lista de parámetros, cuerpo indentado obligatorio y, opcionalmente, un docstring. El detalle de cómo se reciben los valores en los parámetros se trata en [[02 Parametros y Argumentos | Parámetros y Argumentos]].

```python
# 1. Nombre de función (debe ser descriptivo)
def calcular_promedio():
    pass

# 2. Parámetros (entre paréntesis)
def saludar_persona(nombre):
    print(f"Hola, {nombre}!")

# 3. Cuerpo indentado (obligatorio)
def operacion_matematica():
    resultado = 10 + 20  # Cuerpo
    print(f"Resultado: {resultado}")

# 4. Docstring (documentación)
def calcular_area_circulo(radio):
    """
    Calcula el área de un círculo dado su radio.
    
    Args:
        radio (float): El radio del círculo
        
    Returns:
        float: El área calculada
    """
    return 3.14159 * radio ** 2

# Ver documentación
help(calcular_area_circulo)
print(calcular_area_circulo.__doc__)
```

> [!info] El cuerpo es obligatorio
> La indentación delimita el bloque de la función; no puede quedar vacío. Cuando aún no hay implementación, `pass` ocupa el lugar y mantiene la definición sintácticamente válida (esqueleto).

## Llamada e Invocación

La función se ejecuta al escribir su nombre seguido de paréntesis. Debe estar **definida antes** de llamarse en el flujo de ejecución; de lo contrario se produce `NameError`.

```python
# Definición
def saludar():
    print("¡Hola!")

# Llamada
saludar()  # ¡Hola!

# Las funciones deben definirse antes de llamarse
# Esto daría error:
# funcion_no_definida()  # NameError

# Pero pueden llamarse dentro de otras funciones
def preparar_cafe():
    print("Preparando café...")

def desayunar():
    preparar_cafe()  # Llamada dentro de otra función
    print("¡A desayunar!")

desayunar()
```

Una llamada es una expresión: su resultado (el valor de retorno, ver [[03 Valor de Retorno | Valor de Retorno]]) puede usarse en cualquier contexto donde se admita un valor.

```python
def suma(a, b):
    return a + b

def multiplica(a, b):
    return a * b

# Llamada directa
resultado = suma(5, 3)
print(f"Resultado directo: {resultado}")

# Llamada en expresión
valor = suma(10, 20) * 2
print(f"En expresión: {valor}")

# Llamada anidada
complejo = suma(multiplica(2, 3), multiplica(4, 5))
print(f"Llamada anidada: {complejo}")  # (2*3) + (4*5) = 6 + 20 = 26

# Llamada como argumento
print(f"Como argumento: {suma(suma(1, 2), suma(3, 4))}")  # (1+2)+(3+4)=10

# Llamada en condicionales
if suma(5, 5) > 5:
    print("La suma es mayor que 5")

# Llamada en listas por comprensión
resultados = [suma(x, x) for x in range(5)]
print(f"En list comprehension: {resultados}")
```

La definición se evalúa una vez; las llamadas pueden repetirse con argumentos distintos, lo que constituye la reutilización característica de las funciones.

```python
def convertir_mayusculas(texto):
    """Convierte texto a mayúsculas y añade formato."""
    return f"**{texto.upper()}**"

# Múltiples llamadas con diferentes argumentos
print(convertir_mayusculas("hola"))
print(convertir_mayusculas("python"))
print(convertir_mayusculas("funciones"))

# Llamada en bucle
nombres = ["ana", "juan", "carlos"]
for nombre in nombres:
    print(convertir_mayusculas(nombre))

# Acumulación de resultados
def cuadrado(x):
    return x ** 2

numeros = [1, 2, 3, 4, 5]
cuadrados = [cuadrado(n) for n in numeros]
print(f"Cuadrados: {cuadrados}")
```

## Docstring

El **docstring** es el primer literal de cadena dentro del cuerpo. Documenta propósito, argumentos, retorno y excepciones; queda accesible en `función.__doc__` y desde `help(función)`. Convención: una línea de resumen, y para funciones complejas las secciones `Args`, `Returns`, `Raises` y `Example`.

```python
def factorial(n):
    """
    Calcula el factorial de un número n.
    
    Args:
        n (int): Número entero no negativo
        
    Returns:
        int: El factorial de n
        
    Raises:
        ValueError: Si n es negativo
        
    Example:
        >>> factorial(5)
        120
    """
    if n < 0:
        raise ValueError("n debe ser no negativo")
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

## Nombrado de Funciones (PEP 8)

Las funciones siguen `snake_case`: minúsculas con guiones bajos. El `CamelCase` se reserva para clases. Un guion bajo inicial (`_funcion_interna`) señala uso interno por convención.

```python
# ✅ Correcto (snake_case)
def calcular_total():
    pass

def obtener_usuario_por_id():
    pass

def es_valido():
    pass

# ❌ Incorrecto (estilos no recomendados)
def CalcularTotal():  # CamelCase para clases, no funciones
    pass

def calcularTotal():   # Mezcla de estilos
    pass

def f():              # Nombre demasiado corto y poco descriptivo
    pass
```

> [!regla] Buenas prácticas de definición
> - Nombres descriptivos que comuniquen la acción (`calcular_edad_promedio`, no `f`).
> - Una función, una tarea: funciones pequeñas y enfocadas.
> - Documentar las funciones complejas con docstring estructurado.
> - Usar *type hints* (Python 3.5+) para anotar tipos de parámetros y retorno:
>   `def procesar_lista(elementos: list[str]) -> dict[str, int]:`.
> - Guion bajo inicial para funciones "privadas" del módulo.
