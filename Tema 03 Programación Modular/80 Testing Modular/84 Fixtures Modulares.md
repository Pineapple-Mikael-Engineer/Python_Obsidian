---
title: Fixtures Modulares
order: 84
tags:
  - python
  - teoria
  - testing
draft: false
aliases:
  - Fixtures
  - pytest.fixture
  - conftest.py
---

# Fixtures Modulares

> [!definicion]
> Una **fixture** es una función decorada con **`@pytest.fixture`** que **prepara** (y opcionalmente **limpia**) un estado reutilizable para los tests: una conexión, un archivo temporal, datos de ejemplo, un mock configurado. Un test la **recibe declarándola como parámetro**; `pytest` resuelve el nombre, ejecuta la fixture e **inyecta** su valor de retorno. Evita repetir el *setup* en cada test y centraliza el *teardown*.

```python
import pytest

@pytest.fixture
def usuario():                    # fixture: prepara un dato reutilizable
    return {"id": 1, "nombre": "Ada"}

def test_nombre(usuario):         # recibe la fixture por su nombre
    assert usuario["nombre"] == "Ada"

def test_id(usuario):             # cada test obtiene su propia instancia
    assert usuario["id"] == 1
```

El parámetro `usuario` no es un argumento ordinario: `pytest` reconoce que coincide con una fixture y le pasa su valor. Así varios tests comparten la **misma preparación** sin duplicar código.

## Setup y teardown con yield

> [!regla]
> Una fixture con **`yield`** divide su cuerpo en dos fases: lo anterior al `yield` es el **setup** (se ejecuta antes del test) y lo posterior es el **teardown** (se ejecuta después, pase o falle el test). Es el patrón para recursos que deben **liberarse**: archivos, conexiones, procesos.

```python
@pytest.fixture
def conexion_bd():
    conn = abrir_conexion(":memory:")    # setup: antes del test
    yield conn                           # se entrega al test
    conn.close()                         # teardown: siempre, al terminar

def test_inserta(conexion_bd):
    conexion_bd.execute("INSERT ...")
    assert conexion_bd.total() == 1
```

## conftest.py: fixtures compartidas entre módulos

> [!info]
> Una fixture definida en **`conftest.py`** está disponible para **todos los tests del directorio y sus subdirectorios**, sin necesidad de importarla. Es el lugar para fixtures compartidas entre varios `test_<modulo>.py`. `pytest` lo descubre de forma automática: basta con que el archivo exista en el árbol de `tests/`.

```python
# tests/conftest.py  -> visible para todos los test_*.py bajo tests/
import pytest

@pytest.fixture
def cliente_api():
    from unittest.mock import Mock
    api = Mock()
    api.ping.return_value = "ok"
    return api

# tests/test_servicio.py  -> usa la fixture SIN importarla
def test_servicio(cliente_api):
    assert cliente_api.ping() == "ok"
```

Así, la preparación común a los tests de varios módulos vive en un único `conftest.py` en lugar de repetirse en cada archivo.

## Ámbitos: cada cuánto se recrea

> [!ejemplo]
> El parámetro **`scope`** controla **cuántas veces** se ejecuta la fixture. Por defecto es `function`: una vez por test (máximo aislamiento). Ampliar el ámbito reutiliza el recurso y acelera la suite, a cambio de compartir estado.

| `scope` | Se crea una vez por… | Uso típico |
| ------- | -------------------- | ---------- |
| `function` (def.) | cada función de test | aislamiento total, datos mutables |
| `class` | cada clase de test | tests agrupados en una clase |
| `module` | cada archivo `test_*.py` | recurso costoso por módulo |
| `session` | toda la ejecución de `pytest` | recurso caro y de solo lectura (BD, servidor) |

```python
@pytest.fixture(scope="session")    # una sola vez en toda la suite
def servidor():
    srv = arrancar_servidor()
    yield srv
    srv.detener()
```

Las fixtures completan el testing modular: junto a los [[83 Mocks para Dependencias Externas | mocks]] preparan el entorno aislado de cada [[82 Pruebas por Modulo | módulo bajo prueba]], todo sobre la base de [[81 Pytest Basico | Pytest Básico]].
