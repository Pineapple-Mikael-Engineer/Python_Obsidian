---
title: Excepciones por Tipo
draft: false
tags:
  - python
  - teoria
  - excepciones
aliases:
  - Excepciones por Tipo
  - Categorías de Errores
---
# Excepciones por Tipo

Agrupación de las excepciones built-in por **categoría de origen**, frente al catálogo individual de [[02 Excepciones Comunes | Excepciones Comunes]]. Cada categoría comparte una clase base común en el árbol de [[01 Jerarquia de Excepciones | Jerarquía de Excepciones]], lo que permite capturar toda la familia con un único `except` sobre la raíz.

| Categoría | Clase base | Miembros típicos | Capturable con `try/except` |
|-----------|-----------|------------------|------------------------------|
| Tipo / valor | `Exception` | `TypeError`, `ValueError` | Sí |
| Índice / acceso | `LookupError` | `IndexError`, `KeyError` | Sí |
| Atributo / nombre | `Exception` | `AttributeError`, `NameError`, `UnboundLocalError` | Sí |
| E/S y sistema | `OSError` | `FileNotFoundError`, `PermissionError`, `IsADirectoryError`, `FileExistsError`, `ConnectionError`, `TimeoutError` | Sí |
| Importación | `ImportError` | `ModuleNotFoundError` | Sí |
| Sintaxis | `SyntaxError` | `IndentationError` | **No** (ocurre en parseo) |
| Ejecución | `RuntimeError` | `RecursionError`, `MemoryError`, `NotImplementedError` | Sí |
| Lógicos | — | (no lanzan excepción) | **No** (resultado incorrecto) |

## Errores de tipo y valor

`TypeError` (operación entre tipos incompatibles) y `ValueError` (tipo correcto, valor inaceptable) son las dos caras del mismo problema de datos de entrada. Cuelgan directamente de `Exception`. El desarrollo y los ejemplos disparadores de cada una están en [[02 Excepciones Comunes | Excepciones Comunes]].

## Errores de índice y acceso (`LookupError`)

`IndexError` (secuencias) y `KeyError` (diccionarios) comparten la base `LookupError`, lo que permite capturar ambos accesos fallidos de una vez:

```python
try:
    valor = coleccion[clave]
except LookupError:          # captura IndexError y KeyError
    valor = None
```

## Errores de atributo y nombre

`AttributeError` (atributo/método ausente en un objeto) y `NameError`/`UnboundLocalError` (identificador no resuelto en ningún ámbito) cubren los fallos de **resolución de nombres**: el primero sobre miembros de un objeto, los segundos sobre variables y funciones del espacio de nombres.

## Errores de E/S y sistema (`OSError`)

Todos los errores del sistema operativo y de entrada/salida heredan de `OSError`, por lo que un `except OSError` captura la familia completa:

```python
def demostrar_errores_sistema():
    """Errores relacionados con el sistema operativo y E/S."""
    
    print("1. PermissionError - Sin permisos:")
    import os
    try:
        if os.name == 'posix':  # Unix/Linux/Mac
            with open("/etc/shadow", "r") as f:
                pass
        else:  # Windows
            with open("C:\\Windows\\System32\\config\\SAM", "r") as f:
                pass
    except PermissionError as e:
        print(f"   Error: {e}")
    except FileNotFoundError:
        print("   Archivo no encontrado (depende del sistema)")
    
    print("\n2. IsADirectoryError - Es un directorio:")
    try:
        with open("/", "r") as f:  # Intentar abrir directorio como archivo
            pass
    except IsADirectoryError as e:
        print(f"   Error: {e}")
    
    print("\n3. FileExistsError - Archivo ya existe:")
    try:
        os.mkdir("nuevo_directorio")
        os.mkdir("nuevo_directorio")  # Intentar crear directorio existente
    except FileExistsError as e:
        print(f"   Error: {e}")
    except Exception as e:
        print(f"   Otro error: {e}")
    finally:
        # Limpiar
        if os.path.exists("nuevo_directorio"):
            os.rmdir("nuevo_directorio")
    
    print("\n4. ConnectionError - Errores de conexión:")
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 9999))  # Puerto probablemente no abierto
    except ConnectionRefusedError as e:
        print(f"   ConnectionRefusedError: {e}")
    except Exception as e:
        print(f"   Otro error: {e}")
    finally:
        sock.close()
    
    print("\n5. TimeoutError - Tiempo de espera agotado:")
    try:
        import time
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("Operación timeout")
        
        # Configurar alarma (solo Unix)
        if os.name == 'posix':
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(1)  # Alarma en 1 segundo
            
            try:
                time.sleep(3)  # Esperar más que la alarma
            except TimeoutError as e:
                print(f"   Error: {e}")
            finally:
                signal.alarm(0)  # Cancelar alarma
        else:
            print("   Timeout con señal solo en Unix")
    
    except Exception as e:
        print(f"   Error: {e}")

# demostrar_errores_sistema()  # Requiere permisos especiales, comentado por seguridad
```

`FileNotFoundError` —la más frecuente de esta familia— se detalla en [[02 Excepciones Comunes | Excepciones Comunes]].

## Errores de importación (`ImportError`)

Se lanzan al fallar un `import`. `ModuleNotFoundError` (subclase de `ImportError`) indica que el módulo no existe; un `ImportError` directo indica que el módulo existe pero el nombre solicitado **dentro** de él no.

```python
def demostrar_import_error():
    """ImportError ocurre al importar módulos inexistentes."""
    
    print("1. ModuleNotFoundError - Módulo inexistente:")
    try:
        import modulo_inexistente
    except ModuleNotFoundError as e:
        print(f"   Error: {e}")
    
    print("\n2. ImportError - Atributo inexistente en módulo:")
    try:
        from math import seno  # math tiene sin, no seno
    except ImportError as e:
        print(f"   Error: {e}")
    
    print("\n3. ModuleNotFoundError vs ImportError:")
    try:
        # Esto lanza ModuleNotFoundError
        import modulo_inexistente
    except ModuleNotFoundError as e:
        print(f"   ModuleNotFoundError: {type(e).__name__}")
    
    try:
        # Esto lanza ImportError (no ModuleNotFoundError)
        from math import seno
    except ImportError as e:
        print(f"   ImportError: {type(e).__name__}")
    
    print("\n4. Herencia:")
    print(f"   ¿ModuleNotFoundError es subclase de ImportError? "
          f"{issubclass(ModuleNotFoundError, ImportError)}")
    
    print("\n5. Captura general de ImportError:")
    try:
        import sys
        if sys.version_info[0] < 3:
            from urlparse import urlparse  # Python 2
        else:
            from urllib.parse import urlparse  # Python 3
        print("   Importación exitosa")
    except ImportError as e:
        print(f"   Error de importación: {e}")

demostrar_import_error()
```

## Errores de sintaxis (`SyntaxError`)

Ocurren durante el **parseo**, antes de que el código se ejecute, por lo que no son capturables con `try/except` en el mismo bloque que los contiene (solo si el código se compila dinámicamente con `eval`/`exec`/`compile`).

```python
def demostrar_errores_sintaxis():
    """Los SyntaxError ocurren antes de la ejecución."""
    
    print("⚠️ Los SyntaxError no se pueden capturar con try/except")
    print("   porque ocurren durante el parseo, no en ejecución.\n")
    
    ejemplos_sintaxis = [
        "if x == 5  # Faltan dos puntos",
        "    print('Hola')  # Indentación incorrecta",
        "def funcion()  # Faltan dos puntos",
        "print('Hola'  # Falta paréntesis de cierre",
        "a = 5 = b  # Asignación invertida",
        "return x  # return fuera de función",
        "break  # break fuera de bucle",
        "from math import *  # Aunque válido, a veces no recomendado"
    ]
    
    print("Ejemplos que causarían SyntaxError:")
    for i, ejemplo in enumerate(ejemplos_sintaxis, 1):
        print(f"  {i}. {ejemplo}")
    
    print("\nPara ver un SyntaxError real, descomenta la siguiente línea:")
    print("# eval('if True print(\"hola\")')")  # Esto lanzaría SyntaxError

demostrar_errores_sintaxis()
```

## Errores en tiempo de ejecución (`RuntimeError`)

Surgen durante la ejecución por condiciones del propio entorno o flujo del programa: recursión sin caso base (`RecursionError`), agotamiento de memoria (`MemoryError`), método abstracto sin implementar (`NotImplementedError`) o un `RuntimeError` genérico lanzado a mano.

```python
def demostrar_errores_runtime():
    """Errores que ocurren durante la ejecución del programa."""
    
    print("1. RecursionError - Demasiada recursión:")
    def recursivo():
        return recursivo()
    
    try:
        recursivo()
    except RecursionError as e:
        print(f"   Error: {e}")
    
    print("\n2. MemoryError - Memoria insuficiente:")
    try:
        # Intentar crear lista enorme
        lista_gigante = [0] * (10**10)
    except MemoryError as e:
        print(f"   Error: {e}")
    
    print("\n3. SystemError - Error interno del intérprete:")
    # Raro en código normal, más común en extensiones C
    
    print("\n4. RuntimeError - Error general de ejecución:")
    try:
        # raise RuntimeError("Error personalizado")
        pass
    except RuntimeError as e:
        print(f"   Error: {e}")
    
    print("\n5. NotImplementedError - Método no implementado:")
    class ClaseBase:
        def metodo_abstracto(self):
            raise NotImplementedError("Debe implementarse en subclase")
    
    try:
        obj = ClaseBase()
        obj.metodo_abstracto()
    except NotImplementedError as e:
        print(f"   Error: {e}")

demostrar_errores_runtime()
```

## Errores lógicos (semánticos)

No generan excepción: el programa se ejecuta sin fallar pero produce un resultado incorrecto. Por ello **no son detectables** por el mecanismo de excepciones; se descubren con pruebas y revisión.

```python
def demostrar_errores_logicos():
    """Errores lógicos: el código funciona pero hace algo incorrecto."""
    
    print("⚠️ Los errores lógicos NO lanzan excepciones")
    print("   pero producen resultados incorrectos.\n")
    
    ejemplos_logicos = [
        "1. Usar = en lugar de == en condicionales",
        "2. Off-by-one errors en bucles",
        "3. Confundir and/or en condiciones",
        "4. No considerar todos los casos en condicionales",
        "5. Errores de precisión con floats"
    ]
    
    for ejemplo in ejemplos_logicos:
        print(f"  {ejemplo}")
    
    print("\nEjemplo concreto:")
    
    # Error off-by-one
    def suma_hasta_n_mal(n):
        """Intenta sumar números de 1 a n, pero tiene error."""
        suma = 0
        for i in range(n):  # range(n) va de 0 a n-1
            suma += i
        return suma
    
    def suma_hasta_n_bien(n):
        """Suma correctamente números de 1 a n."""
        return sum(range(1, n + 1))
    
    print(f"  suma_hasta_n_mal(5) = {suma_hasta_n_mal(5)} (incorrecto, debería ser 15)")
    print(f"  suma_hasta_n_bien(5) = {suma_hasta_n_bien(5)} (correcto)")
    
    # Error de precisión con floats
    print("\n  Error de precisión con floats:")
    print(f"  0.1 + 0.2 = {0.1 + 0.2} (no es exactamente 0.3)")

demostrar_errores_logicos()
```

> [!warning] Sintaxis y lógica no se capturan
> `SyntaxError` se detecta antes de ejecutar (parseo) y los errores lógicos nunca elevan excepción. El mecanismo `try/except` solo intercepta errores **en tiempo de ejecución** descendientes de `Exception`. Las dos primeras categorías se previenen con linters, pruebas y revisión de código, no con manejo de excepciones.
