---
title: Re-raise y Encadenamiento
tags:
  - python
  - teoria
  - excepciones
draft: false
aliases:
  - raise from
  - Exception chaining
  - Re-lanzar excepciones
---

# Re-raise y Encadenamiento

> [!definicion]
> Re-lanzar es propagar la excepción capturada hacia arriba; encadenar es lanzar una excepción nueva preservando (o suprimiendo) la original. Python registra la relación en dos atributos: `__cause__` (causa explícita, fijada con `from`) y `__context__` (contexto implícito, fijado automáticamente al lanzar dentro de un `except`).

## Sintaxis

| Forma | Sintaxis | Efecto |
|-------|----------|--------|
| **Re-lanzar** | `raise` | Propaga la excepción actual sin alterarla; conserva el traceback original |
| **Encadenar** | `raise Nueva(...) from e` | Lanza `Nueva` fijando `__cause__ = e` ("la causa directa fue…") |
| **Suprimir contexto** | `raise Nueva(...) from None` | Lanza `Nueva` ocultando la original (`__cause__` y `__context__` quedan a `None`) |
| **Implícito** | `raise Nueva(...)` dentro de `except` | Fija `__context__` automáticamente ("durante el manejo ocurrió…") |

## Re-lanzar con `raise` sin argumentos

`raise` desnudo dentro de un `except` vuelve a lanzar la **misma** excepción con su traceback intacto. Útil para registrar (log) el error en un nivel intermedio y dejar que el manejo definitivo ocurra más arriba.

```python
def demostrar_relanzar():
    """Muestra cómo relanzar excepciones."""
    
    def funcion_nivel1():
        print("  Nivel 1: intentando...")
        raise ValueError("Error original en nivel 1")
    
    def funcion_nivel2():
        print("  Nivel 2: llamando a nivel 1...")
        try:
            funcion_nivel1()
        except ValueError:
            print("  Nivel 2: error capturado, relanzando...")
            raise  # Relanza la misma excepción
    
    def funcion_nivel3():
        print(" Nivel 3: llamando a nivel 2...")
        try:
            funcion_nivel2()
        except ValueError as e:
            print(f" Nivel 3: error final capturado: {e}")
            # Procesar y no relanzar
    
    print("Iniciando cadena:")
    funcion_nivel3()
    
    print("\n" + "="*50)
    print("Con logging en cada nivel:")
    
    def nivel_con_log(nivel):
        try:
            if nivel == 1:
                raise RuntimeError(f"Error en nivel {nivel}")
            else:
                nivel_con_log(nivel - 1)
        except Exception as e:
            print(f"  Nivel {nivel}: capturado {type(e).__name__}")
            if nivel > 1:
                print(f"  Nivel {nivel}: relanzando...")
                raise
            else:
                print(f"  Nivel {nivel}: manejando definitivamente")
    
    try:
        nivel_con_log(3)
    except Exception as e:
        print(f"  Final: {e}")

demostrar_relanzar()
```

## Encadenamiento con `raise ... from`

`raise Nueva from e` traduce un error de bajo nivel a uno del dominio actual manteniendo la traza completa. El traceback muestra: *"The above exception was the direct cause of the following exception"*.

> [!info]
> Sin `from`, lanzar dentro de un `except` igualmente preserva la original en `__context__` (cadena implícita, mensaje *"During handling of the above exception…"*). La diferencia: `from` fija `__cause__` y declara la relación de forma explícita e intencional.

```python
def demostrar_encadenamiento_from():
    """Muestra encadenamiento explícito con 'from'."""
    
    def operacion_bd():
        """Simula error de base de datos."""
        raise ConnectionError("Timeout conectando a BD")
    
    def procesar_usuario(usuario_id):
        try:
            print(f"Procesando usuario {usuario_id}...")
            operacion_bd()
        except ConnectionError as e:
            # Encadenar explícitamente
            raise ValueError(f"Error procesando usuario {usuario_id}") from e
    
    def procesar_sin_encadenar(usuario_id):
        try:
            print(f"Procesando usuario {usuario_id}...")
            operacion_bd()
        except ConnectionError:
            # Sin encadenamiento explícito
            raise ValueError(f"Error procesando usuario {usuario_id}")
    
    print("CON ENCADENAMIENTO EXPLÍCITO (from):")
    try:
        procesar_usuario(123)
    except ValueError as e:
        print(f"Error: {e}")
        print(f"Causa original: {e.__cause__}")
        print(f"Es instancia de ConnectionError: {isinstance(e.__cause__, ConnectionError)}")
    
    print("\n" + "="*50)
    print("SIN ENCADENAMIENTO EXPLÍCITO:")
    try:
        procesar_sin_encadenar(456)
    except ValueError as e:
        print(f"Error: {e}")
        print(f"Causa original: {e.__cause__}")  # None
        print(f"Contexto: {e.__context__}")  # ConnectionError implícito
        print(f"Es instancia de ConnectionError: {isinstance(e.__context__, ConnectionError)}")

demostrar_encadenamiento_from()
```

## Suprimir contexto con `from None`

`from None` corta la cadena: oculta el error original en el traceback. Se usa para no filtrar detalles internos (rutas de archivo, errores de driver) al exponer un mensaje limpio al usuario.

```python
def demostrar_from_none():
    """Muestra cómo suprimir el contexto con 'from None'."""
    
    def leer_configuracion(archivo):
        try:
            with open(archivo, 'r') as f:
                return f.read()
        except FileNotFoundError:
            # No queremos exponer detalles del sistema de archivos
            raise RuntimeError(f"Archivo de configuración '{archivo}' no encontrado") from None
    
    def leer_sin_suprimir(archivo):
        try:
            with open(archivo, 'r') as f:
                return f.read()
        except FileNotFoundError as e:
            # Mantiene el contexto
            raise RuntimeError(f"Error leyendo configuración") from e
    
    print("CON SUPRESIÓN (from None):")
    try:
        leer_configuracion("no_existe.conf")
    except RuntimeError as e:
        print(f"Error: {e}")
        print(f"Causa: {e.__cause__}")  # None
        print(f"Contexto: {e.__context__}")  # None
    
    print("\n" + "="*50)
    print("SIN SUPRESIÓN:")
    try:
        leer_sin_suprimir("no_existe.conf")
    except RuntimeError as e:
        print(f"Error: {e}")
        print(f"Causa: {e.__cause__}")
        print(f"Contexto: {e.__context__}")  # Muestra el FileNotFoundError
```

## Causas originales vs nuevas

> [!info]
> - `__cause__`: causa **explícita**, fijada por `raise ... from e`. Indica intención directa.
> - `__context__`: contexto **implícito**, fijado automáticamente al lanzar dentro de un `except`. Indica que la nueva excepción ocurrió mientras se manejaba otra.
> - `from None`: deja ambos en `None` y activa `__suppress_context__ = True`, evitando que el traceback imprima la original.

| Estrategia | `__cause__` | `__context__` se muestra | Cuándo |
|-----------|:-----------:|:------------------------:|--------|
| `raise` desnudo | — | (es la misma) | Log intermedio, manejo arriba |
| `raise Nueva` (en `except`) | `None` | sí (implícito) | Traducir error sin declarar causa |
| `raise Nueva from e` | `e` | suprimido por la causa | Traducir manteniendo trazabilidad |
| `raise Nueva from None` | `None` | no | Ocultar detalle interno |

## Ejemplo práctico: capas de aplicación

Patrón por capas: la capa de datos lanza errores técnicos (`DataLayerError`, `NotFoundInDB`); la capa de negocio los **traduce** con `from e` a errores de dominio (`UserNotFoundError`), conservando la causa para diagnóstico. Los errores de validación se re-lanzan con `raise` desnudo para no enmascararlos.

```python
# Ejemplo de una aplicación con múltiples capas
import json

# Excepciones de capa de datos
class DataLayerError(Exception):
    pass

class NotFoundInDB(DataLayerError):
    pass

class ValidationInDB(DataLayerError):
    pass

# Excepciones de capa de negocio
class BusinessLayerError(Exception):
    pass

class UserNotFoundError(BusinessLayerError):
    pass

class InvalidUserDataError(BusinessLayerError):
    pass

# Capa de datos (simulada)
class UserRepository:
    def __init__(self):
        self._users = {
            1: {"id": 1, "name": "Ana", "email": "ana@mail.com", "age": 25},
            2: {"id": 2, "name": "Juan", "email": "juan@mail.com", "age": 30},
        }
    
    def find_by_id(self, user_id):
        """Busca usuario por ID (capa datos)."""
        try:
            if not isinstance(user_id, int):
                raise ValidationInDB(f"ID debe ser entero: {user_id}")
            
            if user_id not in self._users:
                raise NotFoundInDB(f"Usuario {user_id} no encontrado en BD")
            
            return self._users[user_id]
        except ValidationInDB:
            # Errores de validación relanzamos sin contexto
            raise
        except Exception as e:
            # Otros errores (conexión, etc.) los encapsulamos
            raise DataLayerError("Error en operación de BD") from e
    
    def save(self, user_data):
        """Guarda usuario (capa datos)."""
        try:
            if not user_data.get("name"):
                raise ValidationInDB("Nombre requerido")
            
            if "@" not in user_data.get("email", ""):
                raise ValidationInDB("Email inválido")
            
            new_id = max(self._users.keys()) + 1
            user_data["id"] = new_id
            self._users[new_id] = user_data
            return user_data
        except ValidationInDB:
            raise
        except Exception as e:
            raise DataLayerError("Error guardando usuario") from e

# Capa de negocio
class UserService:
    def __init__(self):
        self.repository = UserRepository()
    
    def get_user(self, user_id):
        """Obtiene usuario por ID (capa negocio)."""
        try:
            user = self.repository.find_by_id(user_id)
            # Reglas de negocio
            if user["age"] < 18:
                user["category"] = "minor"
            else:
                user["category"] = "adult"
            return user
        except NotFoundInDB as e:
            # Convertir a excepción de negocio
            raise UserNotFoundError(f"Usuario {user_id} no existe") from e
        except ValidationInDB as e:
            raise InvalidUserDataError(f"Datos inválidos: {e}") from e
        except DataLayerError as e:
            # Error técnico, relanzamos igual
            raise
    
    def create_user(self, user_data):
        """Crea nuevo usuario."""
        try:
            # Validaciones de negocio
            if user_data.get("age", 0) < 18:
                raise InvalidUserDataError("Usuario debe ser mayor de edad")
            
            return self.repository.save(user_data)
        except ValidationInDB as e:
            raise InvalidUserDataError(f"Datos inválidos: {e}") from e
        except Exception as e:
            raise BusinessLayerError("Error creando usuario") from e

# Capa de presentación/API
def demostrar_capas():
    """Demuestra el manejo de excepciones en capas."""
    
    service = UserService()
    
    # Caso 1: Usuario existe
    try:
        user = service.get_user(1)
        print(f"✓ Usuario encontrado: {user}")
    except UserNotFoundError as e:
        print(f"✗ {e}")
    
    # Caso 2: Usuario no existe
    try:
        user = service.get_user(999)
        print(f"✓ Usuario encontrado: {user}")
    except UserNotFoundError as e:
        print(f"✗ {e}")
        print(f"  Causa: {e.__cause__}")
    
    # Caso 3: Crear usuario válido
    try:
        new_user = service.create_user({"name": "Carlos", "email": "carlos@mail.com", "age": 25})
        print(f"✓ Usuario creado: {new_user}")
    except InvalidUserDataError as e:
        print(f"✗ {e}")
    
    # Caso 4: Crear usuario menor de edad
    try:
        new_user = service.create_user({"name": "Luis", "email": "luis@mail.com", "age": 15})
        print(f"✓ Usuario creado: {new_user}")
    except InvalidUserDataError as e:
        print(f"✗ {e}")
    
    # Caso 5: Crear usuario con email inválido
    try:
        new_user = service.create_user({"name": "Maria", "email": "email-invalido", "age": 30})
        print(f"✓ Usuario creado: {new_user}")
    except InvalidUserDataError as e:
        print(f"✗ {e}")
        print(f"  Causa: {e.__cause__}")

demostrar_capas()
```

## Buenas prácticas

```python
# ✅ Usar encadenamiento cuando sea útil
def buena_encadenamiento():
    try:
        int("hola")
    except ValueError as e:
        raise TypeError("Error de conversión") from e  # ✅ Mantiene contexto

# ✅ Suprimir contexto cuando no sea relevante
def buena_suprimir():
    try:
        with open("config.json") as f:
            return json.load(f)
    except FileNotFoundError:
        raise RuntimeError("Configuración no encontrada") from None  # ✅ Suprime detalle interno

# ❌ No capturar y luego lanzar sin información
def mala_captura():
    try:
        x = 10 / 0
    except ZeroDivisionError:
        raise Exception("Error")  # ❌ Pierde información específica

# ✅ Mejor:
def buena_captura():
    try:
        x = 10 / 0
    except ZeroDivisionError as e:
        raise RuntimeError("Error en cálculo") from e  # ✅ Mantiene contexto
```
