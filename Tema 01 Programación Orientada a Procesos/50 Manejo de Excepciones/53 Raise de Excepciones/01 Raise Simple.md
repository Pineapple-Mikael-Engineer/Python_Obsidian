---
title: Raise Simple
tags:
  - python
  - teoria
  - excepciones
draft: false
aliases:
  - raise
  - Lanzar excepciones
---

# Raise Simple

> [!definicion]
> La sentencia `raise` lanza una excepción de forma intencional, interrumpiendo el flujo normal y propagando el error hacia arriba hasta que un `except` lo capture o el programa termine. Se usa para señalar condiciones de error, validar precondiciones y rechazar entradas inválidas.

## Sintaxis

```python
raise Exception("mensaje")        # instancia con mensaje
raise ValueError                  # clase sin instanciar (sin mensaje)
raise ValueError("msg", 500, {})  # múltiples argumentos -> e.args
```

| Forma | Sintaxis | Uso |
|-------|----------|-----|
| **Con mensaje** | `raise Exception("mensaje")` | Lanzar nueva excepción con descripción |
| **Sin args** | `raise ValueError` | Lanzar sin mensaje |
| **Args múltiples** | `raise ValueError("msg", 500, {...})` | Adjuntar datos extra en `e.args` |

## Ejemplo temprano

```python
def demostrar_raise_basico():
    """Muestra la sintaxis básica de raise."""
    
    print("1. Raise con excepción incorporada:")
    try:
        raise ValueError("Este es un error intencional")
    except ValueError as e:
        print(f"   Capturado: {e}")
    
    print("\n2. Raise sin mensaje:")
    try:
        raise KeyError
    except KeyError as e:
        print(f"   Capturado: {e} (sin mensaje)")
    
    print("\n3. Raise con args múltiples:")
    try:
        raise ValueError("Error crítico", 500, {"detalle": "información extra"})
    except ValueError as e:
        print(f"   Capturado: {e}")
        print(f"   Args: {e.args}")
        print(f"   Primer arg: {e.args[0]}")
        print(f"   Segundo arg: {e.args[1]}")
        print(f"   Tercer arg: {e.args[2]}")
    
    print("\n4. Raise en función condicional:")
    def validar_edad(edad):
        if edad < 0:
            raise ValueError("La edad no puede ser negativa")
        if edad > 150:
            raise ValueError("Edad fuera de rango realista")
        if not isinstance(edad, (int, float)):
            raise TypeError("La edad debe ser un número")
        return f"Edad válida: {edad}"
    
    for valor in [-5, 200, "veinte", 25]:
        try:
            print(f"Validando {valor}: {validar_edad(valor)}")
        except (ValueError, TypeError) as e:
            print(f"   Error: {e}")

demostrar_raise_basico()
```

## Cuándo lanzar cada built-in

> [!info]
> Lanzar siempre la excepción **más específica** que describa el fallo. `raise Exception("Error")` es demasiado general y obliga al llamador a capturar todo.

| Excepción | Situación |
|-----------|-----------|
| `ValueError` | El argumento tiene el tipo correcto pero un valor inadmisible (edad negativa, email sin `@`) |
| `TypeError` | El argumento es de un tipo incorrecto (se esperaba número, llegó string) |
| `KeyError` | Falta una clave requerida en un diccionario |
| `IndexError` | Índice fuera de rango en una secuencia |
| `RuntimeError` | Error genérico que no encaja en otra categoría más concreta |
| `NotImplementedError` | Método abstracto que la subclase debe sobrescribir |

## Raise en validaciones y precondiciones

Validar al inicio del método y lanzar antes de mutar estado: si una precondición falla, la excepción detiene la operación sin dejar el objeto en estado inconsistente.

```python
class CuentaBancaria:
    """Ejemplo de uso de raise para validaciones."""
    
    def __init__(self, titular, saldo_inicial=0):
        if not titular or not isinstance(titular, str):
            raise ValueError("El titular debe ser un string no vacío")
        
        if not isinstance(saldo_inicial, (int, float)):
            raise TypeError("El saldo debe ser numérico")
        
        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo")
        
        self.titular = titular
        self.saldo = saldo_inicial
        self._movimientos = []
    
    def depositar(self, cantidad):
        """Realiza un depósito."""
        if not isinstance(cantidad, (int, float)):
            raise TypeError("La cantidad debe ser numérica")
        
        if cantidad <= 0:
            raise ValueError("La cantidad a depositar debe ser positiva")
        
        self.saldo += cantidad
        self._movimientos.append(f"Depósito: +{cantidad}")
        return self.saldo
    
    def retirar(self, cantidad):
        """Realiza un retiro."""
        if not isinstance(cantidad, (int, float)):
            raise TypeError("La cantidad debe ser numérica")
        
        if cantidad <= 0:
            raise ValueError("La cantidad a retirar debe ser positiva")
        
        if cantidad > self.saldo:
            raise ValueError(f"Saldo insuficiente. Disponible: {self.saldo}")
        
        self.saldo -= cantidad
        self._movimientos.append(f"Retiro: -{cantidad}")
        return self.saldo
    
    def transferir(self, destino, cantidad):
        """Transfiere a otra cuenta."""
        if not isinstance(destino, CuentaBancaria):
            raise TypeError("El destino debe ser una cuenta bancaria")
        
        if destino is self:
            raise ValueError("No se puede transferir a la misma cuenta")
        
        # Retirar de esta cuenta (puede lanzar excepción)
        self.retirar(cantidad)
        
        # Depositar en la cuenta destino
        destino.depositar(cantidad)
        
        self._movimientos.append(f"Transferencia a {destino.titular}: -{cantidad}")
        return self.saldo

# Probar validaciones
try:
    cuenta = CuentaBancaria("Ana", 1000)
    print(f"Cuenta creada: {cuenta.titular} - Saldo: {cuenta.saldo}")
    
    # Operaciones válidas
    cuenta.depositar(500)
    print(f"Depósito exitoso: {cuenta.saldo}")
    
    cuenta.retirar(200)
    print(f"Retiro exitoso: {cuenta.saldo}")
    
    # Operaciones inválidas
    cuenta.retirar(2000)  # Saldo insuficiente
    
except ValueError as e:
    print(f"Error de validación: {e}")
except TypeError as e:
    print(f"Error de tipo: {e}")
```

## Raise con condiciones complejas

Cuando la entrada es una estructura anidada, encadenar validaciones progresivas y lanzar la excepción que identifique con precisión el campo que falló.

```python
def procesar_pedido(pedido):
    """Procesa un pedido con múltiples validaciones."""
    
    # Validación 1: Estructura básica
    if not isinstance(pedido, dict):
        raise TypeError(f"El pedido debe ser un diccionario, no {type(pedido).__name__}")
    
    # Validación 2: Campos requeridos
    campos_requeridos = ['usuario', 'productos', 'total']
    for campo in campos_requeridos:
        if campo not in pedido:
            raise KeyError(f"Campo requerido '{campo}' no encontrado en el pedido")
    
    # Validación 3: Usuario
    if not pedido['usuario'].get('email'):
        raise ValueError("El usuario debe tener un email")
    
    if '@' not in pedido['usuario']['email']:
        raise ValueError(f"Email inválido: {pedido['usuario']['email']}")
    
    # Validación 4: Productos
    if not pedido['productos']:
        raise ValueError("El pedido debe tener al menos un producto")
    
    for i, producto in enumerate(pedido['productos']):
        if not isinstance(producto, dict):
            raise TypeError(f"Producto {i} debe ser diccionario, no {type(producto).__name__}")
        
        if 'precio' not in producto:
            raise KeyError(f"Producto {i} no tiene precio")
        
        if producto['precio'] <= 0:
            raise ValueError(f"Producto {i} tiene precio inválido: {producto['precio']}")
    
    # Validación 5: Total
    total_calculado = sum(p['precio'] * p.get('cantidad', 1) for p in pedido['productos'])
    
    if abs(total_calculado - pedido['total']) > 0.01:  # Tolerancia para floats
        raise ValueError(f"Total incorrecto. Calculado: {total_calculado}, Pedido: {pedido['total']}")
    
    return "Pedido válido"

# Probar con diferentes pedidos
pedidos = [
    {"usuario": {"email": "ana@mail.com"}, "productos": [{"precio": 100}], "total": 100},
    {"usuario": {"email": "juan@mail.com"}, "productos": [{"precio": 50}, {"precio": 30}], "total": 80},
    {"usuario": {"email": "invalido"}, "productos": [{"precio": 100}], "total": 100},  # Email inválido
    {"productos": [{"precio": 100}], "total": 100},  # Falta usuario
    {"usuario": {"email": "ana@mail.com"}, "productos": [], "total": 0},  # Sin productos
]

for i, pedido in enumerate(pedidos):
    try:
        print(f"\nPedido {i}:")
        resultado = procesar_pedido(pedido)
        print(f"  ✓ {resultado}")
    except (TypeError, KeyError, ValueError) as e:
        print(f"  ✗ Error: {type(e).__name__}: {e}")
```

## Re-lanzar

Capturar una excepción y volver a lanzarla con `raise` (sin argumentos) preserva el rastreo original; lanzar una nueva excepción a partir de la capturada permite traducir el error a un dominio distinto. Ambos casos, junto al encadenamiento con `from`, se desarrollan en [[03 Re-raise y Encadenamiento | Re-raise y encadenamiento]].

## Buenas prácticas

```python
# 1. ✅ Usar excepciones específicas
def buena_especifica(valor):
    if valor < 0:
        raise ValueError("Valor no puede ser negativo")  # ✅ Específica
    # raise Exception("Error")  # ❌ Demasiado general

# 2. ✅ Proporcionar mensajes informativos
def buena_mensaje(usuario):
    if not usuario:
        raise ValueError("El usuario no puede ser None o vacío")  # ✅ Claro
        # raise ValueError("Error")  # ❌ Poco informativo

# 6. ✅ Validar precondiciones al inicio
def buena_precondiciones(usuario):
    if not usuario.get("nombre"):
        raise ValueError("Nombre requerido")  # ✅ Validar temprano
    # Resto del código...

# 7. ✅ Documentar qué excepciones lanza
def procesar_archivo(nombre):
    """
    Procesa un archivo.

    Args:
        nombre: Nombre del archivo

    Returns:
        Contenido del archivo

    Raises:
        FileNotFoundError: Si el archivo no existe
        PermissionError: Si no hay permisos de lectura
        ValueError: Si el archivo está vacío
    """
    pass
```
