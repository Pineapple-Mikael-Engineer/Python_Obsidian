---
title: Sintaxis Try Except
draft: false
tags: [python, teoria, excepciones]
---
# Sintaxis Try Except

El bloque `try` envuelve el código que puede lanzar excepciones; cada `except` captura un tipo concreto y desvía el flujo cuando ocurre. Si el error no coincide con ningún `except`, se propaga hacia arriba.

```python
# Sintaxis fundamental de try/except
def division_segura(a, b):
    """Divide dos números de manera segura."""
    try:
        resultado = a / b
        print(f"Resultado: {resultado}")
        return resultado
    except ZeroDivisionError:
        print("Error: No se puede dividir por cero")
        return None

# Pruebas
print(division_segura(10, 2))   # Resultado: 5.0 → 5.0
print(division_segura(10, 0))   # Error: No se puede dividir por cero → None
print(division_segura("10", 2)) # Esto daría TypeError (no capturado)
```

## Múltiples Except y captura específica

Se encadenan varios `except` para tratar cada tipo de error de forma distinta. Python evalúa los bloques en orden y ejecuta el primero que coincide.

```python
def procesar_entrada_usuario(entrada):
    """Procesa entrada de usuario con manejo específico de errores."""
    try:
        # Intentar convertir a entero
        numero = int(entrada)
        
        # Realizar operación
        resultado = 100 / numero
        
        # Acceder a índice
        lista = [1, 2, 3]
        valor_lista = lista[numero]
        
        print(f"Todo OK: {resultado}, {valor_lista}")
        return resultado
        
    except ValueError:
        print("Error: No se puede convertir a número")
        print("  Causa: La entrada no es un número válido")
        
    except ZeroDivisionError:
        print("Error: División por cero")
        print("  Causa: El número no puede ser 0")
        
    except IndexError:
        print("Error: Índice fuera de rango")
        print("  Causa: El número debe ser 0, 1 o 2")
        
    except Exception as e:
        print(f"Error inesperado: {e}")
        print(f"  Tipo: {type(e).__name__}")

# Pruebas
procesar_entrada_usuario("10")   # Índice 10 fuera de rango
procesar_entrada_usuario("0")    # División por cero
procesar_entrada_usuario("hola") # ValueError
procesar_entrada_usuario("2")    # Todo OK
```

### Capturar múltiples excepciones en un solo except

Una tupla de tipos en un único `except` agrupa errores que comparten tratamiento. El detalle de la captura por tupla y `as e` se desarrolla en [[03 Captura de Excepciones | Captura de excepciones]].

```python
def procesar_archivo_datos(nombre_archivo):
    """Procesa archivo con captura múltiple en un except."""
    try:
        with open(nombre_archivo, 'r') as f:
            datos = f.read()
        
        numeros = [int(x) for x in datos.split(',')]
        promedio = sum(numeros) / len(numeros)
        
        return promedio
        
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error de archivo: {e}")
        return None
        
    except (ValueError, ZeroDivisionError) as e:
        print(f"Error de datos: {e}")
        print("  Archivo contiene datos inválidos o está vacío")
        return None
        
    except Exception as e:
        print(f"Error inesperado: {type(e).__name__}: {e}")
        return None

# Simular archivos
import tempfile
import os

# Crear archivo temporal para prueba
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
    f.write("10,20,30,40,50")
    archivo_valido = f.name

# Probar diferentes escenarios
print("Archivo válido:", procesar_archivo_datos(archivo_valido))
print("Archivo inexistente:", procesar_archivo_datos("no_existe.txt"))
os.unlink(archivo_valido)  # Limpiar
```

### Except genérico (`except Exception:`)

`except Exception` captura los errores de programa pero deja pasar `SystemExit` y `KeyboardInterrupt`, a diferencia de un `except:` desnudo. Se coloca al final, después de los específicos.

```python
def buena_practica_exception():
    try:
        x = 10 / 0
    except Exception:  # Captura errores de programa, no SystemExit, KeyboardInterrupt
        pass
```

> [!warning] except desnudo
> Un `except:` sin tipo captura **todo**, incluido `KeyboardInterrupt`. Es peligroso y dificulta detener el programa; usa `except Exception:` como red de seguridad.
>
> ```python
> def mala_practica_general():
>     try:
>         x = 10 / 0
>     except:  # Captura TODO (incluyendo KeyboardInterrupt)
>         pass  # Esto es peligroso
> ```

## Orden de los bloques except

El orden importa: los `except` específicos van **antes** que los generales. Si un tipo general aparece primero, captura todo y los específicos posteriores se vuelven código muerto.

```python
def demostrar_orden_except():
    """Muestra la importancia del orden en los bloques except."""
    
    print("✅ ORDEN CORRECTO: Específicos primero, general después")
    
    class ErrorPersonalizado(Exception):
        pass
    
    try:
        # raise ErrorPersonalizado("Mi error")
        raise ValueError("Mi valor")
    except ErrorPersonalizado as e:
        print(f"Error personalizado: {e}")
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"Exception general: {e}")
    
    print("\n❌ ORDEN INCORRECTO: General antes que específico")
    
    try:
        raise ValueError("Mi valor")
    except Exception as e:  # Este captura TODO
        print(f"Exception general: {e}")
    except ValueError as e:  # Este NUNCA se ejecuta
        print("ValueError - No se ejecutará")
    
    print("\n⚠️ El segundo except nunca se alcanza (código muerto)")

demostrar_orden_except()
```

## Flujo de ejecución con try/except

Tres escenarios: sin error (el `try` se completa), error capturado (salta al `except` correspondiente) y error no capturado (la excepción se propaga e interrumpe el resto).

```python
def demostrar_flujo_try_except():
    """Muestra cómo cambia el flujo con try/except."""
    
    print("1. Sin error:")
    try:
        print("   Inicio del bloque try")
        x = 10 / 2
        print(f"   Operación exitosa: {x}")
        print("   Fin del bloque try")
    except ZeroDivisionError:
        print("   Bloque except - NO se ejecuta")
    print("   Continuación después del bloque\n")
    
    print("2. Con error capturado:")
    try:
        print("   Inicio del bloque try")
        x = 10 / 0
        print("   Esto NO se ejecuta (error antes)")
    except ZeroDivisionError:
        print("   Bloque except - SE ejecuta")
    print("   Continuación después del bloque\n")
    
    print("3. Con error NO capturado:")
    try:
        print("   Inicio del bloque try")
        x = 10 / "0"  # TypeError
        print("   Esto NO se ejecuta")
    except ZeroDivisionError:
        print("   Esto NO se ejecuta (error diferente)")
    print("   Esto NO se ejecuta (el error propaga)")

# demostrar_flujo_try_except()  # Descomentar para ver el error no capturado
```

## Buenas prácticas de captura

```python
# 1. ✅ Capturar excepciones específicas
def buena_practica_especifica():
    try:
        with open('archivo.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Archivo no encontrado"
    except PermissionError:
        return "Sin permisos"
    # No capturar Exception a menos que sea necesario

# 2. ❌ No usar except vacío
def mala_practica_vacio():
    try:
        x = 10 / 0
    except:  # Mal
        pass

# 3. ✅ Mantener el try lo más pequeño posible
def buena_practica_try_pequeno():
    # Mal: try demasiado grande
    try:
        archivo = open('datos.txt', 'r')
        datos = archivo.read()
        numeros = [int(x) for x in datos.split(',')]
        promedio = sum(numeros) / len(numeros)
        archivo.close()
    except Exception:
        pass
    
    # Bien: try enfocado
    try:
        archivo = open('datos.txt', 'r')
    except FileNotFoundError:
        return []
    
    try:
        datos = archivo.read()
    except Exception as e:
        archivo.close()
        raise e
    
    try:
        numeros = [int(x) for x in datos.split(',')]
    except ValueError:
        archivo.close()
        return []
    
    promedio = sum(numeros) / len(numeros)
    archivo.close()
    return promedio
```

La división robusta combina conversión previa, captura específica de `ZeroDivisionError`, una tupla `(TypeError, ValueError)` y un `except Exception` final:

```python
def division_mas_segura(a, b):
    """Divide con captura de múltiples errores."""
    try:
        # Intentar convertir si son strings
        if isinstance(a, str):
            a = float(a)
        if isinstance(b, str):
            b = float(b)
        
        resultado = a / b
        return resultado
    except ZeroDivisionError:
        print("Error: División por cero")
        return None
    except (TypeError, ValueError) as e:
        print(f"Error de tipo/valor: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None

print(division_mas_segura("10", 2))   # 5.0
print(division_mas_segura(10, "0"))   # Error: División por cero → None
print(division_mas_segura("hola", 2)) # Error de tipo/valor → None
```
