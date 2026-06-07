---
title: Captura de Excepciones
draft: false
tags: [python, teoria, excepciones]
---
# Captura de Excepciones

La cláusula `as e` vincula la instancia de la excepción a una variable, permitiendo inspeccionar mensaje, `args`, tipo y atributos específicos. Una tupla de tipos en un solo `except` captura varias excepciones que comparten tratamiento.

```python
# Acceso a la instancia con 'as'
try:
    x = 10 / 0
except ZeroDivisionError as e:
    print(f"Tipo: {type(e)}")
    print(f"Nombre: {type(e).__name__}")
    print(f"Mensaje: {e}")
    print(f"Args: {e.args}")
    print(f"str(e): {str(e)}")
    print(f"repr(e): {repr(e)}")

# Capturar múltiples tipos en un solo except (tupla)
try:
    procesar()
except (FileNotFoundError, PermissionError) as e:
    print(f"Error de archivo: {e}")
```

## Inspeccionar la instancia de la excepción

`type(e).__name__` da el nombre del tipo, `e` o `str(e)` el mensaje, `e.args` la tupla de argumentos con los que se construyó. Varias excepciones exponen atributos propios (`e.name` en `ModuleNotFoundError`).

```python
def demostrar_acceso_excepcion():
    """Muestra cómo acceder a la información de la excepción."""
    
    try:
        x = 10 / 0
    except ZeroDivisionError as e:
        print(f"Tipo: {type(e)}")
        print(f"Nombre: {type(e).__name__}")
        print(f"Mensaje: {e}")
        print(f"Args: {e.args}")
        print(f"str(e): {str(e)}")
        print(f"repr(e): {repr(e)}")
    
    try:
        lista = [1, 2, 3]
        print(lista[10])
    except IndexError as e:
        print(f"\nIndexError:")
        print(f"  Mensaje: {e}")
        print(f"  Args: {e.args}")
    
    try:
        int("hola")
    except ValueError as e:
        print(f"\nValueError:")
        print(f"  Mensaje: {e}")
        print(f"  Args: {e.args}")
    
    try:
        import modulo_inexistente
    except ModuleNotFoundError as e:
        print(f"\nModuleNotFoundError:")
        print(f"  Mensaje: {e}")
        print(f"  Args: {e.args}")
        print(f"  Nombre: {e.name}")  # Atributo específico

demostrar_acceso_excepcion()
```

## Atributos específicos de excepciones

Muchas excepciones del estándar añaden atributos útiles para diagnosticar: `OSError` expone `errno`/`strerror`/`filename`; `UnicodeEncodeError` el `encoding`, `start`, `end`; `SyntaxError` el `lineno` y `offset`.

```python
def demostrar_atributos_especificos():
    """Muestra atributos específicos de diferentes excepciones."""
    
    # OSError y subclases
    try:
        with open("/archivo/inexistente", "r") as f:
            pass
    except OSError as e:
        print("OSError:")
        print(f"  errno: {e.errno}")
        print(f"  strerror: {e.strerror}")
        print(f"  filename: {e.filename}")
        print(f"  filename2: {e.filename2}")
    
    # UnicodeError
    try:
        texto = "áéíóú".encode("ascii")
    except UnicodeEncodeError as e:
        print("\nUnicodeEncodeError:")
        print(f"  encoding: {e.encoding}")
        print(f"  reason: {e.reason}")
        print(f"  object: {e.object}")
        print(f"  start: {e.start}")
        print(f"  end: {e.end}")
    
    # SyntaxError
    try:
        compile('if True print("hola")', '<string>', 'exec')
    except SyntaxError as e:
        print("\nSyntaxError:")
        print(f"  msg: {e.msg}")
        print(f"  lineno: {e.lineno}")
        print(f"  offset: {e.offset}")
        print(f"  text: {e.text}")

demostrar_atributos_especificos()
```

## Traceback y pila de llamadas

El traceback contiene la cadena de frames desde donde se lanzó el error. `traceback.format_exc()` lo da como string, `sys.exc_info()` devuelve la tupla `(tipo, valor, traceback)`, y se puede recorrer manualmente con `tb.tb_next`.

```python
import traceback
import sys

def demostrar_traceback():
    """Muestra cómo obtener y usar el traceback."""
    
    def funcion_nivel3():
        raise ValueError("Error en nivel 3")
    
    def funcion_nivel2():
        funcion_nivel3()
    
    def funcion_nivel1():
        funcion_nivel2()
    
    try:
        funcion_nivel1()
    except ValueError as e:
        print("=" * 50)
        print("1. Información básica:")
        print(f"Error: {e}")
        
        print("\n2. Traceback como string:")
        tb_string = traceback.format_exc()
        print(tb_string)
        
        print("\n3. Traceback como lista:")
        tb_list = traceback.format_exception(*sys.exc_info())
        for linea in tb_list:
            print(linea, end='')
        
        print("\n4. Información detallada:")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(f"Tipo: {exc_type.__name__}")
        print(f"Valor: {exc_value}")
        
        # Recorrer frames del traceback
        print("\n5. Frames de la pila:")
        tb = exc_traceback
        while tb:
            print(f"  Archivo: {tb.tb_frame.f_code.co_filename}")
            print(f"  Línea: {tb.tb_lineno}")
            print(f"  Función: {tb.tb_frame.f_code.co_name}")
            print("  ---")
            tb = tb.tb_next

demostrar_traceback()
```

## Encadenamiento de excepciones

`raise NuevoError(...) from e` establece `__cause__` (causa explícita). Sin `from`, el error original queda en `__context__` (contexto implícito). `from None` suprime el contexto.

```python
def demostrar_encadenamiento():
    """Muestra el encadenamiento de excepciones con 'from'."""
    
    def convertir_a_entero(valor):
        """Convierte valor a entero, encadenando excepciones."""
        try:
            return int(valor)
        except ValueError as e:
            # Encadenar explícitamente
            raise TypeError(f"No se pudo convertir '{valor}' a entero") from e
    
    def procesar_sin_encadenar(valor):
        """Procesa sin encadenamiento explícito."""
        try:
            return int(valor)
        except ValueError:
            # Sin 'from', contexto implícito
            raise TypeError(f"No se pudo convertir '{valor}' a entero")
    
    print("Con encadenamiento explícito (from):")
    try:
        convertir_a_entero("hola")
    except TypeError as e:
        print(f"Error: {e}")
        print(f"Causa original: {e.__cause__}")
    
    print("\nSin encadenamiento explícito:")
    try:
        procesar_sin_encadenar("hola")
    except TypeError as e:
        print(f"Error: {e}")
        print(f"Contexto: {e.__context__}")
        print(f"Causa: {e.__cause__}")
    
    # Suprimir contexto
    def suprimir_contexto(valor):
        try:
            return int(valor)
        except ValueError as e:
            # Suprimir el contexto automático
            raise TypeError(f"No se pudo convertir '{valor}'") from None
    
    print("\nContexto suprimido (from None):")
    try:
        suprimir_contexto("hola")
    except TypeError as e:
        print(f"Error: {e}")
        print(f"Causa: {e.__cause__}")

demostrar_encadenamiento()
```

## Logging de excepciones

`logging.error(..., exc_info=True)` y `logging.exception(...)` registran el traceback completo junto al mensaje. `logging.exception` se usa dentro de un `except` y equivale a `error(..., exc_info=True)`.

```python
import logging

def demostrar_logging_excepciones():
    """Muestra cómo registrar excepciones con logging."""
    
    # Configurar logging básico
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    def procesar_archivo_log(nombre_archivo):
        """Procesa archivo con logging de errores."""
        try:
            with open(nombre_archivo, 'r') as f:
                datos = f.read()
            
            # Procesar datos
            numeros = [int(x) for x in datos.split(',')]
            promedio = sum(numeros) / len(numeros)
            
            logging.info(f"Procesado {nombre_archivo}: promedio={promedio}")
            return promedio
            
        except FileNotFoundError as e:
            logging.error(f"Archivo no encontrado: {nombre_archivo}", exc_info=True)
            return None
        except ValueError as e:
            logging.error(f"Datos inválidos en {nombre_archivo}", exc_info=True)
            return None
        except Exception as e:
            logging.exception(f"Error inesperado procesando {nombre_archivo}")
            return None
    
    # Probar con diferentes archivos
    print(procesar_archivo_log("archivo_inexistente.txt"))
    
    import tempfile
    import os
    
    # Archivo con datos válidos
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("10,20,30,40,50")
        nombre = f.name
    
    print(procesar_archivo_log(nombre))
    os.unlink(nombre)
    
    # Archivo con datos inválidos
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("10,hola,30")
        nombre = f.name
    
    print(procesar_archivo_log(nombre))
    os.unlink(nombre)

# demostrar_logging_excepciones()
```

## Buenas prácticas

```python
# ✅ Acceder a información del error cuando sea útil
def buena_practica_info_error():
    try:
        conversion = int("hola")
    except ValueError as e:
        print(f"Error: {e}")  # Muestra mensaje útil
        # Mejor que print("Error de conversión") genérico

# ✅ Encadenar excepciones apropiadamente
def buena_practica_encadenamiento():
    try:
        return int("hola")
    except ValueError as e:
        raise TypeError("Error de tipo") from e
```
