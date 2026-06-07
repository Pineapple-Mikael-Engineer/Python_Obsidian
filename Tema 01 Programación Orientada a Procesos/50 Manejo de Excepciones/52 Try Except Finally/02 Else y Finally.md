---
title: Else y Finally
order: 2
draft: false
tags: [python, teoria, excepciones]
---
# Else y Finally

`else` se ejecuta solo si el `try` terminó **sin excepción**; `finally` se ejecuta **siempre**, haya o no error (e incluso ante un `return`). El orden completo es: `try` → (`except` | `else`) → `finally`.

| Bloque | Cuándo se ejecuta | Uso típico |
|--------|-------------------|------------|
| **try** | Siempre | Código que puede lanzar excepciones |
| **except** | Solo si hay error del tipo especificado | Manejar errores específicos |
| **else** | Solo si NO hay error | Código que depende del éxito del try |
| **finally** | Siempre (haya o no error) | Limpieza de recursos |

## Bloque else: se ejecuta solo si no hay error

Permite separar el código que depende del éxito del `try` del código que puede fallar. Mantiene el `try` pequeño: solo la operación riesgosa va en `try`, el procesamiento posterior en `else`.

```python
def procesar_con_else():
    """Demuestra el uso del bloque else."""
    
    def leer_configuracion(archivo):
        """Lee configuración y procesa con else."""
        try:
            with open(archivo, 'r') as f:
                config = f.read()
        except FileNotFoundError:
            print(f"Archivo {archivo} no encontrado")
            return None
        else:
            # Este bloque solo se ejecuta si NO hubo error
            print("✅ Archivo leído exitosamente")
            print(f"  Contenido: {config}")
            
            # Procesar configuración
            lineas = config.split('\n')
            print(f"  Líneas: {len(lineas)}")
            return lineas
        finally:
            print("  finally: siempre se ejecuta")
    
    # Crear archivo temporal
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.cfg') as f:
        f.write("host=localhost\nport=8080\ndebug=true")
        archivo = f.name
    
    # Probar con archivo existente
    resultado = leer_configuracion(archivo)
    print(f"Resultado: {resultado}\n")
    
    # Probar con archivo inexistente
    resultado = leer_configuracion("no_existe.cfg")
    print(f"Resultado: {resultado}")
    
    # Limpiar
    import os
    os.unlink(archivo)

procesar_con_else()
```

## Bloque finally: siempre se ejecuta

Se usa para liberar recursos (archivos, conexiones, sockets) pase lo que pase. Se ejecuta antes de que un `return` del `try`/`except` devuelva el valor; si `finally` tiene su propio `return`, este sobreescribe al anterior.

```python
def demostrar_finally():
    """Muestra que finally siempre se ejecuta."""
    
    def operacion_con_finally(provocar_error=False):
        """Realiza operación con finally."""
        print("\n" + "="*40)
        print(f"Iniciando operación (error={provocar_error})")
        
        recurso = None
        try:
            print("1. Abriendo recurso...")
            recurso = open("temp.txt", "w")
            recurso.write("datos")
            
            if provocar_error:
                print("2. Provocando error...")
                raise ValueError("Error simulado")
            
            print("3. Operación completada exitosamente")
            return "Éxito"
            
        except ValueError as e:
            print(f"4. Capturado error: {e}")
            return "Error capturado"
            
        finally:
            print("5. FINALLY: Cerrando recurso siempre")
            if recurso:
                recurso.close()
                print("   Recurso cerrado")
    
    # Sin error
    resultado = operacion_con_finally(False)
    print(f"Resultado final: {resultado}")
    
    # Con error capturado
    resultado = operacion_con_finally(True)
    print(f"Resultado final: {resultado}")
    
    # finally con return
    def funcion_con_return():
        try:
            print("try: retornando 1")
            return 1
        finally:
            print("finally: se ejecuta ANTES de retornar")
            # finally puede tener return, pero sobreescribe
            # return 2  # Descomentar para ver que sobreescribe
    
    print("\n" + "="*40)
    print(f"Return en try: {funcion_con_return()}")

demostrar_finally()
```

## Orden completo: try → except/else → finally

```python
def demostrar_orden_completo():
    """Muestra el orden completo de ejecución."""
    
    def probar_escenario(valor, divisor, idx):
        """Prueba diferentes escenarios de error."""
        print(f"\n--- Probando: valor={valor}, divisor={divisor}, idx={idx} ---")
        
        lista = [10, 20, 30]
        
        try:
            print("1. try: Iniciando operaciones")
            
            num = int(valor)
            print(f"   Conversión OK: {num}")
            
            div = num / divisor
            print(f"   División OK: {div}")
            
            elem = lista[idx]
            print(f"   Acceso a lista OK: {elem}")
            
        except ValueError as e:
            print(f"2. except ValueError: {e}")
            return "Error de conversión"
            
        except ZeroDivisionError as e:
            print(f"2. except ZeroDivisionError: {e}")
            return "Error de división"
            
        except IndexError as e:
            print(f"2. except IndexError: {e}")
            return "Error de índice"
            
        else:
            print("3. else: Todo salió bien")
            resultado = div * elem
            print(f"   Calculando resultado: {div} * {elem} = {resultado}")
            return f"Éxito: {resultado}"
            
        finally:
            print("4. finally: Limpiando recursos (siempre)")
    
    # Probar diferentes escenarios
    print(probar_escenario("10", 2, 1))   # Éxito
    print(probar_escenario("hola", 2, 1)) # ValueError
    print(probar_escenario("10", 0, 1))   # ZeroDivisionError
    print(probar_escenario("10", 2, 5))   # IndexError

demostrar_orden_completo()
```

## Casos prácticos: limpieza de recursos

El patrón `recurso = None` → `try` → `finally: if recurso: recurso.close()` garantiza el cierre incluso si la apertura o el uso fallan.

```python
import sqlite3
import time

def ejemplo_conexion_bd():
    """Ejemplo práctico: conexión a BD con finally."""
    
    def consultar_usuario(usuario_id):
        """Consulta usuario asegurando cierre de conexión."""
        conn = None
        try:
            print(f"Conectando a BD para usuario {usuario_id}...")
            conn = sqlite3.connect(':memory:')  # BD en memoria
            
            # Crear tabla de prueba
            conn.execute('CREATE TABLE usuarios (id INTEGER, nombre TEXT)')
            conn.execute('INSERT INTO usuarios VALUES (1, "Ana")')
            conn.execute('INSERT INTO usuarios VALUES (2, "Juan")')
            conn.commit()
            
            # Consultar
            cursor = conn.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,))
            resultado = cursor.fetchone()
            
            if resultado is None:
                raise ValueError(f"Usuario {usuario_id} no encontrado")
            
            return resultado
            
        except sqlite3.Error as e:
            print(f"Error de BD: {e}")
            return None
        except ValueError as e:
            print(f"Error: {e}")
            return None
        finally:
            print("Cerrando conexión a BD...")
            if conn:
                conn.close()
    
    # Probar
    print(consultar_usuario(1))  # OK
    print(consultar_usuario(3))  # No existe
    print(consultar_usuario("x")) # Error de tipo

# ejemplo_conexion_bd()

def ejemplo_conexion_red():
    """Ejemplo práctico: conexión de red con finally."""
    import socket
    
    def verificar_puerto(host, port, timeout=2):
        """Verifica si un puerto está abierto."""
        sock = None
        try:
            print(f"Verificando {host}:{port}...")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            resultado = sock.connect_ex((host, port))
            
            if resultado == 0:
                return f"Puerto {port} abierto"
            else:
                return f"Puerto {port} cerrado o filtrado"
                
        except socket.gaierror as e:
            print(f"Error de resolución DNS: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None
        finally:
            print("Cerrando socket...")
            if sock:
                sock.close()
    
    # Probar
    print(verificar_puerto("localhost", 80))
    print(verificar_puerto("google.com", 443))
    print(verificar_puerto("host_inexistente.xyz", 80))

# ejemplo_conexion_red()
```

> [!tip] Context managers
> Cuando exista, prefiere `with` a un `try/finally` manual: el cierre del recurso se gestiona automáticamente.
>
> ```python
> def buena_practica_context_manager():
>     # En lugar de try/finally manual
>     with open('archivo.txt', 'r') as f:
>         return f.read()
>     # with maneja el cierre automáticamente
> ```

## Buenas prácticas con else y finally

```python
# ✅ Usar else para código que depende del éxito
def buena_practica_else():
    try:
        datos = cargar_datos()
    except FileNotFoundError:
        datos = []
    else:
        # Solo se ejecuta si cargar_datos() funcionó
        datos = procesar_datos(datos)
    finally:
        # Siempre se ejecuta
        guardar_log()
    return datos

# ✅ Usar finally para limpieza
def buena_practica_finally():
    recurso = None
    try:
        recurso = abrir_recurso()
        return usar_recurso(recurso)
    finally:
        if recurso:
            recurso.close()
```
