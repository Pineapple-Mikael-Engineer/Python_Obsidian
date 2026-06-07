---
title: Excepciones Comunes
order: 2
draft: false
tags:
  - python
  - teoria
  - excepciones
aliases:
  - Excepciones Comunes
  - Common Exceptions
---
# Excepciones Comunes

Catálogo de las excepciones built-in que más se encuentran en código cotidiano, con la **causa** que las dispara y ejemplos mínimos de cada disparador. Su posición en el árbol y la captura por ancestro se trata en [[01 Jerarquia de Excepciones | Jerarquía de Excepciones]]; su agrupación por categoría en [[03 Excepciones por Tipo | Excepciones por Tipo]].

| Excepción | Causa | Ejemplo |
|-----------|-------|---------|
| `NameError` | Nombre no definido en el ámbito | `print(x)` sin `x` |
| `TypeError` | Operación entre tipos incompatibles | `"hola" + 5` |
| `ValueError` | Tipo correcto, valor inapropiado | `int("hola")` |
| `IndexError` | Índice fuera de rango en secuencia | `[1,2][5]` |
| `KeyError` | Clave inexistente en diccionario | `{"a":1}["b"]` |
| `AttributeError` | Atributo/método inexistente | `[1,2].añadir()` |
| `ZeroDivisionError` | División por cero | `10 / 0` |
| `FileNotFoundError` | Archivo o ruta inexistente | `open("x.txt")` |

## NameError — Nombre no definido

Se lanza al usar un identificador (variable o función) que no existe en ningún ámbito accesible. Su subtipo `UnboundLocalError` ocurre cuando una variable **local** se lee antes de asignarse (Python la marca local por existir una asignación posterior en la misma función).

```python
def demostrar_name_error():
    """NameError ocurre cuando se usa un nombre no definido."""
    
    print("1. NameError - Variable no definida:")
    try:
        print(variable_inexistente)
    except NameError as e:
        print(f"   Error: {e}")
    
    print("\n2. NameError - Función no definida:")
    try:
        funcion_inexistente()
    except NameError as e:
        print(f"   Error: {e}")
    
    print("\n3. NameError vs UnboundLocalError:")
    x = 10
    try:
        print(x)
        x = x + 1  # Esto funciona
    except NameError:
        print("   Esto no ocurrirá")
    
    def problema():
        print(y)  # y no está definida
        y = 5
    
    try:
        problema()
    except UnboundLocalError as e:  # Subtipo de NameError
        print(f"   UnboundLocalError: {e}")

demostrar_name_error()
```

## TypeError — Tipo incorrecto

Se lanza cuando una operación o función se aplica a un objeto de tipo inadecuado: concatenar tipos distintos, invocar algo no llamable, iterar sobre un no-iterable, indexar con un tipo equivocado o pasar un número erróneo de argumentos.

```python
def demostrar_type_error():
    """TypeError ocurre cuando se opera con tipos incompatibles."""
    
    print("1. TypeError - Sumar string y número:")
    try:
        resultado = "hola" + 5
    except TypeError as e:
        print(f"   Error: {e}")
    
    print("\n2. TypeError - Llamar a no-función:")
    try:
        numero = 42
        numero()
    except TypeError as e:
        print(f"   Error: {e}")
    
    print("\n3. TypeError - Iterar sobre no-iterable:")
    try:
        for x in 42:
            pass
    except TypeError as e:
        print(f"   Error: {e}")
    
    print("\n4. TypeError - Índice con tipo incorrecto:")
    lista = [1, 2, 3]
    try:
        print(lista["0"])
    except TypeError as e:
        print(f"   Error: {e}")
    
    print("\n5. TypeError - Argumentos incorrectos:")
    try:
        print(len(1, 2, 3))  # len espera un solo argumento
    except TypeError as e:
        print(f"   Error: {e}")

demostrar_type_error()
```

## ValueError — Valor incorrecto

El **tipo** del argumento es correcto, pero su **valor** no es aceptable: convertir una cadena no numérica con `int()`, `list.index()`/`list.remove()` con un elemento ausente, `math.sqrt()` de un negativo o `range()` con paso cero.

```python
def demostrar_value_error():
    """ValueError ocurre cuando el valor es inapropiado aunque el tipo sea correcto."""
    
    print("1. ValueError - Conversión inválida:")
    try:
        numero = int("hola")
    except ValueError as e:
        print(f"   Error: {e}")
    
    print("\n2. ValueError - Índice fuera de rango en métodos:")
    lista = [1, 2, 3]
    try:
        lista.index(10)  # ValueError, no IndexError
    except ValueError as e:
        print(f"   Error: {e}")
    
    print("\n3. ValueError - Raíz de número negativo (sin cmath):")
    import math
    try:
        math.sqrt(-1)
    except ValueError as e:
        print(f"   Error: {e}")
    
    print("\n4. ValueError - remove() con elemento inexistente:")
    try:
        lista.remove(10)
    except ValueError as e:
        print(f"   Error: {e}")
    
    print("\n5. ValueError - range() con step cero:")
    try:
        list(range(0, 10, 0))
    except ValueError as e:
        print(f"   Error: {e}")

demostrar_value_error()
```

> [!info] `index()`/`remove()` lanzan `ValueError`, no `IndexError`
> Buscar un elemento ausente en una lista (`lista.index(10)`, `lista.remove(10)`) es un problema de **valor**, no de índice: el elemento no está, así que la excepción es `ValueError`. `IndexError` solo surge al acceder por posición (`lista[5]`).

## IndexError — Índice fuera de rango

Se lanza al acceder por posición a una secuencia (lista, tupla, `str`) con un índice inexistente, sea positivo o negativo. En diccionarios el acceso por clave inexistente no es `IndexError` sino `KeyError`.

```python
def demostrar_index_error():
    """IndexError ocurre al acceder a un índice inexistente."""
    
    print("1. IndexError - Índice positivo fuera de rango:")
    lista = [1, 2, 3]
    try:
        print(lista[5])
    except IndexError as e:
        print(f"   Error: {e}")
    
    print("\n2. IndexError - Índice negativo fuera de rango:")
    try:
        print(lista[-10])
    except IndexError as e:
        print(f"   Error: {e}")
    
    print("\n3. IndexError - En strings:")
    texto = "Python"
    try:
        print(texto[10])
    except IndexError as e:
        print(f"   Error: {e}")
    
    print("\n4. IndexError - En tuplas:")
    tupla = (1, 2, 3)
    try:
        print(tupla[5])
    except IndexError as e:
        print(f"   Error: {e}")
    
    print("\n5. IndexError no ocurre en diccionarios (KeyError):")
    diccionario = {"a": 1}
    try:
        print(diccionario[5])  # Esto es KeyError, no IndexError
    except KeyError as e:
        print(f"   Es KeyError: {e}")

demostrar_index_error()
```

## KeyError — Clave no encontrada

Se lanza al acceder a una clave inexistente en un diccionario con `d[clave]` o al usar `pop()`/`del` sobre una clave ausente. Los métodos `get()` y `pop(clave, default)` evitan la excepción devolviendo un valor por defecto.

```python
def demostrar_key_error():
    """KeyError ocurre al acceder a una clave inexistente en diccionario."""
    
    print("1. KeyError - Clave inexistente:")
    diccionario = {"nombre": "Ana", "edad": 25}
    try:
        print(diccionario["direccion"])
    except KeyError as e:
        print(f"   Error: {e}")
    
    print("\n2. KeyError - Diferencia con get():")
    # get() no lanza excepción
    valor = diccionario.get("direccion", "No especificada")
    print(f"   Usando get(): {valor}")
    
    try:
        valor = diccionario["direccion"]
    except KeyError as e:
        print(f"   Usando []: KeyError: {e}")
    
    print("\n3. KeyError en diccionarios anidados:")
    datos = {
        "usuario": {
            "nombre": "Juan",
            "contacto": {
                "email": "juan@mail.com"
            }
        }
    }
    
    try:
        print(datos["usuario"]["contacto"]["telefono"])
    except KeyError as e:
        print(f"   Error: clave '{e}' no encontrada")
    
    print("\n4. KeyError en pop() con clave inexistente:")
    try:
        diccionario.pop("direccion")
    except KeyError as e:
        print(f"   Error: {e}")
    
    # pop() con default no lanza error
    valor = diccionario.pop("direccion", None)
    print(f"   pop() con default: {valor}")

demostrar_key_error()
```

## AttributeError — Atributo no existe

Se lanza al acceder con notación de punto a un atributo o método que el objeto no posee: un método mal escrito, un atributo no inicializado, una función inexistente en un módulo, o llamar un método sobre `None`. El acceso con punto a un diccionario busca **atributo** (`AttributeError`), no clave (`KeyError`).

```python
def demostrar_attribute_error():
    """AttributeError ocurre al acceder a un atributo inexistente."""
    
    print("1. AttributeError - Método inexistente:")
    lista = [1, 2, 3]
    try:
        lista.añadir(4)  # append, no añadir
    except AttributeError as e:
        print(f"   Error: {e}")
    
    print("\n2. AttributeError - Atributo inexistente:")
    class Persona:
        def __init__(self, nombre):
            self.nombre = nombre
    
    p = Persona("Ana")
    try:
        print(p.edad)
    except AttributeError as e:
        print(f"   Error: {e}")
    
    print("\n3. AttributeError - En módulos:")
    import math
    try:
        math.seno(30)  # math.sin, no math.seno
    except AttributeError as e:
        print(f"   Error: {e}")
    
    print("\n4. AttributeError - En NoneType:")
    valor = None
    try:
        valor.append(5)
    except AttributeError as e:
        print(f"   Error: {e}")
    
    print("\n5. AttributeError vs KeyError:")
    # En diccionarios, acceso con punto es AttributeError
    d = {"nombre": "Ana"}
    try:
        d.nombre  # Esto busca atributo, no clave
    except AttributeError as e:
        print(f"   Acceso con punto: {e}")
    
    # Acceso con corchetes es KeyError
    try:
        d["nombre"]  # Esto funciona
        d["edad"]    # Esto da KeyError
    except KeyError as e:
        print(f"   Acceso con []: KeyError: {e}")

demostrar_attribute_error()
```

## ZeroDivisionError — División por cero

Se lanza con cualquier operador de división cuyo divisor sea cero: `/`, `//` y `%`, tanto con enteros como con flotantes.

```python
def demostrar_zero_division():
    """ZeroDivisionError ocurre al dividir por cero."""
    
    print("1. ZeroDivisionError - División entera:")
    try:
        resultado = 10 / 0
    except ZeroDivisionError as e:
        print(f"   Error: {e}")
    
    print("\n2. ZeroDivisionError - División flotante:")
    try:
        resultado = 10.5 / 0.0
    except ZeroDivisionError as e:
        print(f"   Error: {e}")
    
    print("\n3. ZeroDivisionError - División entera (//):")
    try:
        resultado = 10 // 0
    except ZeroDivisionError as e:
        print(f"   Error: {e}")
    
    print("\n4. ZeroDivisionError - Módulo (%):")
    try:
        resultado = 10 % 0
    except ZeroDivisionError as e:
        print(f"   Error: {e}")
    
    print("\n5. ZeroDivisionError no ocurre con 0.0 en algunos contextos:")
    # En contextos matemáticos avanzados, 0.0 puede dar infinito
    import math
    try:
        print(f"   math.atanh(1.0) = {math.atanh(1.0)}")  # infinito
    except ValueError as e:  # No ZeroDivisionError
        print(f"   Error: {e}")

demostrar_zero_division()
```

## FileNotFoundError — Archivo no encontrado

Subclase de `OSError`. Se lanza al abrir, borrar (`os.remove`) o renombrar (`os.rename`) un archivo cuya ruta no existe. Errores de E/S afines (`PermissionError`, `IsADirectoryError`) son hermanos bajo `OSError`, no `FileNotFoundError`.

```python
def demostrar_file_not_found():
    """FileNotFoundError ocurre al intentar abrir archivo inexistente."""
    
    print("1. FileNotFoundError - Abrir archivo:")
    try:
        with open("archivo_inexistente.txt", "r") as f:
            contenido = f.read()
    except FileNotFoundError as e:
        print(f"   Error: {e}")
    
    print("\n2. FileNotFoundError - Diferente de PermissionError:")
    try:
        # Intentar abrir directorio como archivo
        with open("/", "r") as f:  # En Unix
            pass
    except FileNotFoundError:
        print("   No es FileNotFoundError en este caso")
    except IsADirectoryError as e:  # Subtipo de OSError
        print(f"   Error: {e}")
    except PermissionError as e:
        print(f"   Error: {e}")
    except OSError as e:
        print(f"   Error OSError: {e}")
    
    print("\n3. FileNotFoundError en os.remove():")
    import os
    try:
        os.remove("archivo_inexistente.txt")
    except FileNotFoundError as e:
        print(f"   Error: {e}")
    
    print("\n4. FileNotFoundError en os.rename():")
    try:
        os.rename("origen_inexistente.txt", "destino.txt")
    except FileNotFoundError as e:
        print(f"   Error: {e}")
    
    print("\n5. FileNotFoundError es subclase de OSError:")
    print(f"   issubclass(FileNotFoundError, OSError): {issubclass(FileNotFoundError, OSError)}")

demostrar_file_not_found()
```

Las familias de E/S (`OSError`), importación (`ImportError`) y acceso (`LookupError`) se agrupan y contrastan en [[03 Excepciones por Tipo | Excepciones por Tipo]].
