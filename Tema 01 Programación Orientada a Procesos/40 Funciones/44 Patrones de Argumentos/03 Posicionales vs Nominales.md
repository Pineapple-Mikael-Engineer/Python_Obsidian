---
title: 03 Posicionales vs Nominales
draft: false
tags: [python, teoria, funciones]
---
# Posicionales vs Nominales

Un argumento se pasa **por posición** (su orden coincide con la definición) o **por nombre** (`parametro=valor`, el orden es irrelevante). Por defecto un parámetro admite ambos. Los marcadores `/` y `*` en la firma **restringen** qué forma se permite.

| Marcador | Efecto | Sintaxis |
| -------- | ------ | -------- |
| (ninguno) | Posicional o nominal | `def f(a, b)` |
| `/` | Lo anterior es **solo posicional** | `def f(a, b, /)` |
| `*` | Lo posterior es **solo nominal** | `def f(*, a, b)` |

## Argumentos Posicionales

Se pasan en el **orden** en que se definieron los parámetros; el orden determina a qué parámetro va cada valor.

```python
def describir_persona(nombre, edad, ciudad):
    """Función con tres parámetros posicionales."""
    print(f"{nombre} tiene {edad} años y vive en {ciudad}")

# Llamada con argumentos posicionales (el orden importa)
describir_persona("Ana", 25, "Madrid")     # ✅ Correcto
describir_persona(25, "Ana", "Madrid")     # ❌ Lógico: 25 años se llama Ana?

# Ejemplo con cálculo
def calcular_precio(base, impuesto, descuento):
    """Calcula precio final con impuesto y descuento."""
    precio_con_impuesto = base * (1 + impuesto)
    precio_final = precio_con_impuesto * (1 - descuento)
    return precio_final

# El orden debe coincidir con la definición
print(calcular_precio(100, 0.21, 0.10))  # 100€ +21% -10% = 108.9€
print(calcular_precio(0.21, 100, 0.10))  # ❌ Resultado sin sentido
```

## Argumentos Nominales (Keyword Arguments)

Se pasan con el **nombre** del parámetro; el orden no importa y la llamada gana en legibilidad.

```python
def crear_usuario(nombre, email, edad, activo=True):
    """Crea un usuario con varios atributos."""
    usuario = {
        "nombre": nombre,
        "email": email,
        "edad": edad,
        "activo": activo
    }
    return usuario

# Llamada con argumentos nominales (el orden NO importa)
usuario1 = crear_usuario(
    nombre="Ana",
    email="ana@email.com",
    edad=25,
    activo=True
)

usuario2 = crear_usuario(
    edad=30,
    nombre="Carlos",
    email="carlos@email.com",
    activo=False
)

print(usuario1)
print(usuario2)

# Ventaja: claridad en la llamada
def configurar_servidor(host, puerto, ssl, timeout, max_conexiones):
    """Configura un servidor con múltiples opciones."""
    print(f"Servidor: {host}:{puerto}, SSL={ssl}, timeout={timeout}, max={max_conexiones}")

# Con posicionales (difícil de leer)
configurar_servidor("localhost", 8080, True, 30, 100)

# Con nominales (mucho más claro)
configurar_servidor(
    host="localhost",
    puerto=8080,
    ssl=True,
    timeout=30,
    max_conexiones=100
)
```

## Mezcla y Orden

En la llamada, **primero los posicionales y luego los nominales**. Un posicional después de un nominal es `SyntaxError`.

```python
def registrar_transaccion(fecha, monto, tipo, descripcion="", moneda="EUR"):
    """Registra una transacción financiera."""
    print(f"Fecha: {fecha}")
    print(f"Monto: {monto} {moneda}")
    print(f"Tipo: {tipo}")
    if descripcion:
        print(f"Desc: {descripcion}")
    print("-" * 20)

# Regla: primero posicionales, luego nominales
registrar_transaccion("2024-01-15", 1500.50, "ingreso")

registrar_transaccion(
    "2024-01-16",           # posicional
    75.30,                  # posicional
    "gasto",                # posicional
    descripcion="Supermercado",  # nominal
    moneda="USD"            # nominal
)

# ❌ Error: nominal antes que posicional
# registrar_transaccion(
#     fecha="2024-01-17",  # nominal antes de posicionales
#     200,                  # ❌ SyntaxError
#     "transferencia"
# )

# ❌ Error: argumento posicional después de nominal
# registrar_transaccion(
#     "2024-01-17",
#     monto=200,            # nominal
#     "transferencia"       # ❌ posicional después de nominal
# )
```

## Solo Posicionales (`/`)

Los parámetros **antes de `/`** (Python 3.8+) no pueden pasarse por nombre. Útil cuando el nombre del parámetro es un detalle de implementación que podría cambiar, o cuando el orden es semánticamente obvio.

```python
# Los parámetros antes de / son SOLO posicionales
def dividir(numerador, denominador, /):
    """División: numerador y denominador solo posicionales."""
    if denominador == 0:
        return None
    return numerador / denominador

# ✅ Válido: argumentos posicionales
print(dividir(10, 2))  # 5.0

# ❌ Inválido: argumentos nominales
# print(dividir(numerador=10, denominador=2))  # TypeError

# Mezcla: algunos posicionales, otros normales
def registrar(nombre, edad, /, ciudad, activo=True):
    """Registra persona: nombre/edad posicionales, ciudad/activo pueden ser nominales."""
    print(f"Nombre: {nombre}")
    print(f"Edad: {edad}")
    print(f"Ciudad: {ciudad}")
    print(f"Activo: {activo}")

# ✅ Válido
registrar("Ana", 25, "Madrid")                    # ciudad posicional
registrar("Juan", 30, ciudad="Barcelona")         # ciudad nominal
registrar("Carlos", 22, ciudad="Valencia", activo=False)

# ❌ Inválido: nombre o edad como nominales
# registrar(nombre="Ana", edad=25, ciudad="Madrid")  # TypeError
```

```python
# 1. Función matemática donde el orden es importante
def potencia(base, exponente, /):
    """Potencia: base^exponente (solo posicional)."""
    return base ** exponente

# Tiene sentido porque intercambiar argumentos daría resultado diferente
print(potencia(2, 3))   # 8
print(potencia(3, 2))   # 9 (diferente)

# 2. Función con parámetros que deberían ser posicionales
def calcular_imc(peso, altura, /):
    """Calcula IMC: peso(kg) y altura(m) solo posicionales."""
    return peso / (altura ** 2)

# No confundir: calcular_imc(altura=1.75, peso=70) no tendría sentido

# 3. API donde los nombres podrían cambiar
def crear_vector(x, y, z, /):
    """Crea vector 3D con coordenadas posicionales."""
    return (x, y, z)

# Los nombres podrían cambiar a coord_x, etc., pero la llamada sigue funcionando
v = crear_vector(1, 2, 3)

# 4. Función con parámetros posicionales y nominales
def formatear_fecha(dia, mes, anio, /, formato="corto", separador="/"):
    """Formatea fecha: día, mes, año son solo posicionales."""
    if formato == "corto":
        return f"{dia:02d}{separador}{mes:02d}{separador}{anio}"
    else:
        meses = ["ene", "feb", "mar", "abr", "may", "jun",
                 "jul", "ago", "sep", "oct", "nov", "dic"]
        return f"{dia:02d} {meses[mes-1]} {anio}"

print(formatear_fecha(15, 3, 2024))
print(formatear_fecha(15, 3, 2024, formato="largo", separador="-"))
```

## Solo Nominales (`*`)

Los parámetros **después de `*`** (keyword-only) deben pasarse por nombre. Fuerzan explicitud en funciones con muchas opciones, donde una lista de posicionales sueltos sería ilegible.

```python
# Los parámetros después de * son SOLO nominales
def configurar(*, host, port, ssl=False):
    """Configura servidor: todos los parámetros solo nominales."""
    print(f"Config: {host}:{port}, SSL={ssl}")

# ✅ Válido: argumentos nominales
configurar(host="localhost", port=8080)
configurar(host="192.168.1.1", port=3000, ssl=True)

# ❌ Inválido: argumentos posicionales
# configurar("localhost", 8080)  # TypeError

# Mezcla: algunos posicionales, otros solo nominales
def crear_evento(fecha, hora, *, lugar, importancia="normal"):
    """Crea evento: fecha/hora posicionales, lugar/importancia nominales."""
    print(f"Evento: {fecha} {hora}")
    print(f"Lugar: {lugar} (importancia: {importancia})")

# ✅ Válido
crear_evento("2024-01-15", "18:30", lugar="Sala A")
crear_evento("2024-01-16", "10:00", lugar="Sala B", importancia="alta")

# ❌ Inválido: lugar como posicional
# crear_evento("2024-01-15", "18:30", "Sala A")  # TypeError
```

```python
# 1. Función con muchos parámetros opcionales
def enviar_email(destinatario, asunto, *, cc=None, bcc=None, importancia="normal", adjuntos=None):
    """Envía email: destinatario/asunto posicionales, resto nominales."""
    print(f"Enviando a: {destinatario}")
    print(f"Asunto: {asunto}")
    if cc:
        print(f"CC: {cc}")
    if bcc:
        print(f"BCC: {bcc}")
    print(f"Importancia: {importancia}")
    if adjuntos:
        print(f"Adjuntos: {len(adjuntos)} archivo(s)")

# Uso claro y explícito
enviar_email(
    "ana@email.com",
    "Reunión importante",
    cc="jefe@empresa.com",
    importancia="alta"
)

# 2. Operaciones con parámetros nominales obligatorios
def operacion_matematica(*, operacion, a, b):
    """Realiza operación matemática con parámetros nominales."""
    if operacion == "suma":
        return a + b
    elif operacion == "resta":
        return a - b
    elif operacion == "multiplica":
        return a * b
    elif operacion == "divide":
        return a / b if b != 0 else None

# Obliga a ser explícito
print(operacion_matematica(operacion="suma", a=10, b=5))
print(operacion_matematica(operacion="multiplica", a=7, b=8))

# 3. Función con parámetros posicionales y nominales obligatorios
def procesar_archivo(nombre_archivo, modo, *, encoding="utf-8", linea_por_linea=False):
    """Procesa archivo: nombre/modo posicionales, encoding/linea_por_linea nominales."""
    print(f"Abriendo {nombre_archivo} en modo {modo}")
    print(f"Encoding: {encoding}")
    print(f"Modo: {'línea por línea' if linea_por_linea else 'completo'}")

procesar_archivo("datos.txt", "r")
procesar_archivo("config.json", "w", encoding="ascii", linea_por_linea=True)
```

## Combinación de `/` y `*`

Una misma firma puede declarar las tres zonas: solo-posicional (`/`), mixta, y solo-nominal (`*`). El orden es: `pos_only, /, pos_o_nom, *, kw_only`.

```python
# Función con todo tipo de parámetros
def funcion_compleja(requerido1, requerido2, /,  # Solo posicionales
                     opcional1=None, opcional2=None,  # Posicionales o nominales
                     *,  # A partir de aquí solo nominales
                     nominal1, nominal2,  # Obligatorios nominales
                     nominal3="default"):  # Opcional nominal
    """Demuestra combinación de todos los patrones."""
    print(f"Posicionales: {requerido1}, {requerido2}")
    print(f"Opcionales: {opcional1}, {opcional2}")
    print(f"Nominales: {nominal1}, {nominal2}, {nominal3}")

# Llamada válida
funcion_compleja(
    1, 2,                    # Solo posicionales
    opcional1="x",           # Puede ser nominal
    opcional2="y",           # Puede ser nominal
    nominal1="A",            # Solo nominal
    nominal2="B",            # Solo nominal
    nominal3="C"             # Solo nominal
)

# También válida (opcionales posicionales)
funcion_compleja(
    1, 2,                    # Posicionales
    "x", "y",                # Opcionales posicionales
    nominal1="A",            # Solo nominal
    nominal2="B"             # Solo nominal
)

# Ejemplo práctico: función de base de datos
def consultar_bd(tabla, /,  # Solo posicional
                 columnas="*",  # Posicional o nominal
                 *,  # A partir de aquí solo nominal
                 where=None,
                 order_by=None,
                 limit=None):
    """Consulta a base de datos con parámetros flexibles."""
    query = f"SELECT {columnas} FROM {tabla}"
    if where:
        query += f" WHERE {where}"
    if order_by:
        query += f" ORDER BY {order_by}"
    if limit:
        query += f" LIMIT {limit}"
    return query

# Llamadas claras y flexibles
print(consultar_bd("usuarios"))
print(consultar_bd("productos", "nombre, precio", where="activo=true", limit=10))
print(consultar_bd("ventas", order_by="fecha DESC", limit=100))
```

## Claridad en APIs

```python
# API REST simulada
def api_request(endpoint, /,  # Solo posicional
                 method="GET",  # Posicional o nominal
                 *,  # A partir de aquí solo nominal
                 data=None,
                 headers=None,
                 auth=None,
                 timeout=30):
    """Realiza petición API con parámetros flexibles."""
    print(f"\n--- API Request ---")
    print(f"Endpoint: {endpoint}")
    print(f"Method: {method}")
    if data:
        print(f"Data: {data}")
    if headers:
        print(f"Headers: {headers}")
    if auth:
        print(f"Auth: {auth}")
    print(f"Timeout: {timeout}s")
    return f"Response from {endpoint}"

# Diferentes formas de llamar
api_request("/users")  # GET simple
api_request("/users", "POST", data={"name": "Ana"})  # POST con datos
api_request("/users", headers={"X-API-Key": "123"}, auth=("user", "pass"))  # Con auth
api_request("/search", "GET", timeout=60, headers={"Accept": "application/json"})
```

> [!tip] Criterio de diseño de API: usa `/` para parámetros estables cuyo nombre no quieres comprometer, y `*` para forzar que toda opción "bandera" (`ssl=`, `timeout=`, `verbose=`) se nombre en la llamada. Así el código cliente se autodocumenta y la firma puede evolucionar sin romper llamadas existentes.
