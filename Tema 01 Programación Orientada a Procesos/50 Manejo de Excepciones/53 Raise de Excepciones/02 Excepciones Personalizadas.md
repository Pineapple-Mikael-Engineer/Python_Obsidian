---
title: Excepciones Personalizadas
tags:
  - python
  - teoria
  - excepciones
draft: false
aliases:
  - Custom exceptions
  - Excepciones propias
---

# Excepciones Personalizadas

> [!definicion]
> Una excepción personalizada es una clase que hereda de `Exception` (o de otra excepción) y representa un error específico del dominio de la aplicación. Permite construir jerarquías propias, adjuntar atributos y métodos, y capturar errores de negocio de forma selectiva.

## Sintaxis

```python
class MiError(Exception):
    """Documentación de la excepción."""
    pass

raise MiError("descripción del fallo")
```

Para añadir datos se sobreescribe `__init__` llamando a `super().__init__(mensaje)`:

```python
class SaldoInsuficienteError(Exception):
    def __init__(self, saldo, requerido):
        self.saldo = saldo
        self.requerido = requerido
        super().__init__(f"Saldo insuficiente: {saldo} < {requerido}")
```

## Creación de excepciones básicas

Heredar de `Exception` (nunca de `BaseException` directamente) y definir una **clase base por aplicación** de la que cuelguen las demás. Así un único `except ErrorDeAplicacion` captura toda la familia.

```python
# Excepción personalizada más simple
class ErrorDeAplicacion(Exception):
    """Excepción base para toda la aplicación."""
    pass

class ErrorDeValidacion(ErrorDeAplicacion):
    """Error durante la validación de datos."""
    pass

class ErrorDeNegocio(ErrorDeAplicacion):
    """Error en reglas de negocio."""
    pass

class ErrorDePersistencia(ErrorDeAplicacion):
    """Error en operaciones de base de datos."""
    pass

# Uso
def demostrar_excepciones_personalizadas():
    """Muestra el uso de excepciones personalizadas básicas."""
    
    def registrar_usuario(nombre, email):
        if not nombre:
            raise ErrorDeValidacion("El nombre es requerido")
        
        if '@' not in email:
            raise ErrorDeValidacion(f"Email inválido: {email}")
        
        if email in usuarios_registrados:
            raise ErrorDeNegocio(f"El email {email} ya está registrado")
        
        # Simular guardado en BD
        try:
            guardar_en_bd(nombre, email)
        except Exception as e:
            raise ErrorDePersistencia(f"Error guardando usuario: {e}") from e
        
        return {"nombre": nombre, "email": email}
    
    usuarios_registrados = ["ana@mail.com", "juan@mail.com"]
    
    def guardar_en_bd(nombre, email):
        # Simular error de BD
        if email == "error@mail.com":
            raise ConnectionError("Error de conexión a BD")
        print(f"Guardado: {nombre}, {email}")
    
    # Probar diferentes casos
    casos = [
        ("", "ana@mail.com"),
        ("Ana", "correo-invalido"),
        ("Ana", "ana@mail.com"),  # Ya registrado
        ("Pedro", "pedro@mail.com"),  # Válido
        ("Luis", "error@mail.com"),  # Error de BD
    ]
    
    for nombre, email in casos:
        try:
            resultado = registrar_usuario(nombre, email)
            print(f"✓ Usuario registrado: {resultado}")
        except ErrorDeValidacion as e:
            print(f"✗ Validación: {e}")
        except ErrorDeNegocio as e:
            print(f"✗ Negocio: {e}")
        except ErrorDePersistencia as e:
            print(f"✗ Persistencia: {e}")
            print(f"  Causa original: {e.__cause__}")

demostrar_excepciones_personalizadas()
```

> [!info]
> El uso de `raise ... from e` aparece arriba para encapsular el error de BD. El detalle del encadenamiento de causas se desarrolla en [[03 Re-raise y Encadenamiento | Re-raise y encadenamiento]].

## Excepciones con atributos personalizados

Adjuntar atributos (`codigo`, `detalles`) permite transportar metadatos del error y serializarlos. Sobreescribir `__str__` controla el formato del mensaje.

```python
class ErrorHttp(Exception):
    """Excepción HTTP con código de estado."""
    
    def __init__(self, mensaje, codigo, detalles=None):
        super().__init__(mensaje)
        self.codigo = codigo
        self.detalles = detalles or {}
    
    def __str__(self):
        return f"[{self.codigo}] {super().__str__()}"
    
    def to_dict(self):
        """Convierte a diccionario para respuesta JSON."""
        return {
            "error": self.__class__.__name__,
            "codigo": self.codigo,
            "mensaje": str(self),
            "detalles": self.detalles
        }

class Error404(ErrorHttp):
    def __init__(self, recurso, tipo=None):
        mensaje = f"Recurso no encontrado: {recurso}"
        detalles = {"recurso": recurso, "tipo": tipo}
        super().__init__(mensaje, 404, detalles)

class Error400(ErrorHttp):
    def __init__(self, mensaje, campos_invalidos=None):
        detalles = {"campos_invalidos": campos_invalidos or []}
        super().__init__(mensaje, 400, detalles)

class Error500(ErrorHttp):
    def __init__(self, mensaje, error_interno=None):
        detalles = {"error_interno": str(error_interno) if error_interno else None}
        super().__init__(mensaje, 500, detalles)

def demostrar_excepciones_con_atributos():
    """Muestra excepciones con atributos personalizados."""
    
    def buscar_usuario(usuario_id):
        usuarios = {1: "Ana", 2: "Juan", 3: "Carlos"}
        
        if not isinstance(usuario_id, int):
            raise Error400(
                "ID de usuario inválido",
                campos_invalidos=["usuario_id"]
            )
        
        if usuario_id not in usuarios:
            raise Error404(f"usuario/{usuario_id}", tipo="usuario")
        
        return {"id": usuario_id, "nombre": usuarios[usuario_id]}
    
    def procesar_solicitud(usuario_id):
        try:
            return buscar_usuario(usuario_id)
        except ErrorHttp as e:
            # Los errores HTTP ya están formateados
            return e.to_dict()
        except Exception as e:
            # Errores inesperados se convierten en 500
            error = Error500("Error interno del servidor", e)
            return error.to_dict()
    
    # Probar diferentes casos
    for caso in [1, 2, "hola", 999]:
        print(f"\nBuscando usuario {caso}:")
        resultado = procesar_solicitud(caso)
        if isinstance(resultado, dict) and "error" in resultado:
            print(f"  Error: {resultado}")
        else:
            print(f"  Éxito: {resultado}")

demostrar_excepciones_con_atributos()
```

## Excepciones con métodos personalizados

Una excepción puede ofrecer métodos de formateo (`to_log`, `to_response`) y constructores alternativos (`@classmethod from_dict`), convirtiéndose en un objeto rico que centraliza la representación del error.

```python
class ErrorValidacionCompleja(Exception):
    """Excepción de validación con funcionalidad adicional."""
    
    def __init__(self, mensaje, campo=None, valor=None, regla=None):
        super().__init__(mensaje)
        self.campo = campo
        self.valor = valor
        self.regla = regla
        self.timestamp = __import__('datetime').datetime.now()
    
    def __str__(self):
        partes = [super().__str__()]
        if self.campo:
            partes.append(f"campo='{self.campo}'")
        if self.valor is not None:
            partes.append(f"valor={self.valor}")
        if self.regla:
            partes.append(f"regla={self.regla}")
        return " | ".join(partes)
    
    def to_log(self):
        """Formato para logging."""
        return {
            "tipo": "VALIDATION_ERROR",
            "mensaje": str(self),
            "campo": self.campo,
            "valor": self.valor,
            "regla": self.regla,
            "timestamp": self.timestamp.isoformat()
        }
    
    def to_response(self, include_details=True):
        """Formato para respuesta al cliente."""
        response = {
            "error": "VALIDATION_ERROR",
            "message": str(self)
        }
        if include_details and self.campo:
            response["field"] = self.campo
            response["rule"] = self.regla
        return response
    
    @classmethod
    def from_dict(cls, dict_error):
        """Crea excepción desde diccionario."""
        return cls(
            dict_error.get("mensaje", "Error de validación"),
            dict_error.get("campo"),
            dict_error.get("valor"),
            dict_error.get("regla")
        )

def demostrar_metodos_personalizados():
    """Muestra excepciones con métodos personalizados."""
    
    def validar_edad(edad, nombre):
        if not isinstance(edad, (int, float)):
            raise ErrorValidacionCompleja(
                "La edad debe ser numérica",
                campo="edad",
                valor=edad,
                regla="tipo_numérico"
            )
        
        if edad < 0:
            raise ErrorValidacionCompleja(
                "La edad no puede ser negativa",
                campo="edad",
                valor=edad,
                regla="no_negativo"
            )
        
        if edad > 150:
            raise ErrorValidacionCompleja(
                "Edad fuera de rango",
                campo="edad",
                valor=edad,
                regla="rango_realista"
            )
        
        if edad < 18 and nombre in ["admin", "root"]:
            raise ErrorValidacionCompleja(
                "Usuarios especiales deben ser mayores de edad",
                campo="nombre",
                valor=nombre,
                regla="permiso_especial"
            )
        
        return True
    
    # Probar validaciones
    casos = [
        (25, "normal"),
        (-5, "normal"),
        (200, "normal"),
        ("veinte", "normal"),
        (15, "admin"),
    ]
    
    for edad, nombre in casos:
        print(f"\nValidando {nombre} con edad {edad}:")
        try:
            validar_edad(edad, nombre)
            print("  ✓ Válido")
        except ErrorValidacionCompleja as e:
            print(f"  ✗ {e}")
            print(f"  Log: {e.to_log()}")
            print(f"  Response: {e.to_response()}")

demostrar_metodos_personalizados()
```

## Jerarquía de excepciones personalizadas

Una jerarquía profunda permite capturar a distintos niveles de granularidad: una base `AppError`, una rama de API (`APIError` con `status_code`) y una rama de negocio (`BusinessError`). El manejador centralizado captura la base y serializa cualquier descendiente.

```python
# Jerarquía completa para una aplicación
class AppError(Exception):
    """Excepción base de la aplicación."""
    
    def __init__(self, mensaje, codigo="APP_ERROR", detalles=None):
        super().__init__(mensaje)
        self.codigo = codigo
        self.detalles = detalles or {}

# Errores de API
class APIError(AppError):
    def __init__(self, mensaje, codigo="API_ERROR", status_code=500, detalles=None):
        super().__init__(mensaje, codigo, detalles)
        self.status_code = status_code

class NotFoundError(APIError):
    def __init__(self, recurso, id_recurso):
        mensaje = f"{recurso} con id {id_recurso} no encontrado"
        super().__init__(
            mensaje,
            codigo="NOT_FOUND",
            status_code=404,
            detalles={"recurso": recurso, "id": id_recurso}
        )

class ValidationError(APIError):
    def __init__(self, campo, valor, regla):
        mensaje = f"Validación falló para {campo}"
        super().__init__(
            mensaje,
            codigo="VALIDATION_ERROR",
            status_code=400,
            detalles={"campo": campo, "valor": valor, "regla": regla}
        )

class AuthenticationError(APIError):
    def __init__(self, razon="Credenciales inválidas"):
        super().__init__(
            razon,
            codigo="AUTH_ERROR",
            status_code=401
        )

class AuthorizationError(APIError):
    def __init__(self, usuario, recurso):
        mensaje = f"Usuario {usuario} no autorizado para acceder a {recurso}"
        super().__init__(
            mensaje,
            codigo="FORBIDDEN",
            status_code=403,
            detalles={"usuario": usuario, "recurso": recurso}
        )

# Errores de negocio
class BusinessError(AppError):
    pass

class InsufficientStockError(BusinessError):
    def __init__(self, producto, cantidad_solicitada, stock_actual):
        mensaje = f"Stock insuficiente para {producto}: solicitado {cantidad_solicitada}, disponible {stock_actual}"
        super().__init__(
            mensaje,
            codigo="INSUFFICIENT_STOCK",
            detalles={
                "producto": producto,
                "solicitado": cantidad_solicitada,
                "disponible": stock_actual
            }
        )

class InsufficientFundsError(BusinessError):
    def __init__(self, cuenta, cantidad, saldo):
        mensaje = f"Fondos insuficientes en cuenta {cuenta}: requerido {cantidad}, disponible {saldo}"
        super().__init__(
            mensaje,
            codigo="INSUFFICIENT_FUNDS",
            detalles={
                "cuenta": cuenta,
                "requerido": cantidad,
                "disponible": saldo
            }
        )

# Uso de la jerarquía
def demostrar_jerarquia_personalizada():
    """Muestra el uso de jerarquía de excepciones."""
    
    def api_endpoint(usuario, producto_id, cantidad):
        try:
            # Simular validaciones
            if not usuario:
                raise AuthenticationError()
            
            if usuario == "invitado" and producto_id == "admin":
                raise AuthorizationError(usuario, producto_id)
            
            if producto_id == "999":
                raise NotFoundError("producto", producto_id)
            
            if cantidad < 0:
                raise ValidationError("cantidad", cantidad, "positiva")
            
            if producto_id == "1" and cantidad > 10:
                raise InsufficientStockError("Producto 1", cantidad, 10)
            
            if usuario == "pobre" and cantidad * 100 > 50:
                raise InsufficientFundsError(usuario, cantidad * 100, 50)
            
            return {"status": "success", "compra": f"{cantidad} x {producto_id}"}
            
        except AppError as e:
            # Manejo centralizado de errores
            return {
                "error": e.codigo,
                "message": str(e),
                "details": e.detalles
            }
    
    # Probar diferentes escenarios
    escenarios = [
        (None, "1", 5),        # Auth error
        ("invitado", "admin", 1),  # Authz error
        ("user", "999", 1),    # Not found
        ("user", "1", -5),     # Validation error
        ("user", "1", 20),     # Stock error
        ("pobre", "1", 1),     # Funds error
        ("user", "1", 5),      # Success
    ]
    
    for usuario, producto, cantidad in escenarios:
        print(f"\nUsuario: {usuario}, Producto: {producto}, Cantidad: {cantidad}")
        resultado = api_endpoint(usuario, producto, cantidad)
        print(f"Resultado: {resultado}")

demostrar_jerarquia_personalizada()
```

## Documentación

> [!regla]
> Toda excepción personalizada lleva docstring que describa **cuándo** se lanza. Las funciones que la lanzan la declaran en la sección `Raises:` de su propio docstring, de modo que el llamador conozca el contrato sin leer la implementación.

```python
class SaldoInsuficienteError(Exception):
    """Se lanza cuando una operación de retiro o transferencia
    excede el saldo disponible de la cuenta."""
    def __init__(self, saldo, requerido):
        self.saldo = saldo
        self.requerido = requerido
        super().__init__(f"Saldo insuficiente: {saldo} < {requerido}")
```
