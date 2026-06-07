---
title: Pytest Básico
order: 81
tags:
  - python
  - teoria
  - testing
draft: false
aliases:
  - pytest
  - Pruebas con pytest
  - Testing básico
---

# Pytest Básico

> [!definicion]
> **`pytest`** es el *framework* de pruebas más usado en Python. **Descubre** los tests por convención: busca archivos `test_*.py` (o `*_test.py`) y, dentro, **funciones** cuyo nombre empieza por `test_`. Cada test usa la sentencia **`assert` plana** del lenguaje: si la condición es falsa, el test **falla**; si no lanza ninguna excepción, **pasa**. Se ejecuta con el comando `pytest` desde la terminal.

```python
# test_calculadora.py
def suma(a, b):
    return a + b

def test_suma_positivos():        # función test_*  -> la descubre pytest
    assert suma(2, 3) == 5        # assert plano: condición a verificar

def test_suma_negativos():
    assert suma(-1, -1) == -2
```

```bash
$ pytest                          # descubre y ejecuta todos los test_*.py
========================= test session starts =========================
collected 2 items

test_calculadora.py ..                                          [100%]

========================== 2 passed in 0.01s ==========================
```

Cada punto (`.`) es un test que **pasó**. `pytest` no necesita clases ni heredar de nada: una función `test_*` con `assert` basta. Esa ligereza es lo que lo hace ideal para probar módulos.

## El assert plano y su introspección

> [!regla]
> A diferencia de `unittest` (que exige métodos como `assertEqual`), `pytest` usa el `assert` nativo y **reescribe** la expresión para mostrar los valores reales cuando falla. No hay que aprender una API de aserciones: cualquier expresión booleana sirve.

```python
def test_suma_falla():
    assert suma(2, 2) == 5        # falla a propósito
```

```bash
$ pytest test_calculadora.py
========================== FAILURES ===========================
________________________ test_suma_falla _____________________

    def test_suma_falla():
>       assert suma(2, 2) == 5
E       assert 4 == 5
E        +  where 4 = suma(2, 2)

test_calculadora.py:9: AssertionError
==================== 1 failed in 0.02s ========================
```

La línea `assert 4 == 5` y el `where 4 = suma(2, 2)` los genera `pytest` solo: muestra el **valor obtenido** frente al **esperado** sin que el test lo imprima.

## Comprobar excepciones

> [!info]
> Para verificar que un código **lanza** una excepción se usa el gestor de contexto `pytest.raises`. El test pasa si dentro del bloque se eleva la excepción indicada; falla si no se eleva.

```python
import pytest

def dividir(a, b):
    return a / b

def test_division_por_cero():
    with pytest.raises(ZeroDivisionError):
        dividir(1, 0)            # debe lanzar la excepción
```

## Lectura de la salida

> [!ejemplo]
> El resumen final clasifica cada test. Conviene reconocer los estados y las banderas de ejecución más usadas.

| Símbolo / estado | Significado |
| ---------------- | ----------- |
| `.` / `passed` | el test pasó |
| `F` / `failed` | un `assert` falló |
| `E` / `error` | excepción fuera del `assert` (p. ej. en el *setup*) |
| `s` / `skipped` | test omitido (`@pytest.mark.skip`) |

```bash
$ pytest -v          # verbose: un test por línea con su nombre y estado
$ pytest -q          # quiet: salida mínima
$ pytest -k suma     # solo tests cuyo nombre contiene "suma"
$ pytest test_calculadora.py::test_suma_positivos   # un test concreto
```

Con la base de `pytest` clara, el siguiente paso es **organizar** estos tests: un archivo por módulo, como se ve en [[82 Pruebas por Modulo | Pruebas por Módulo]]. Para sustituir dependencias externas, [[83 Mocks para Dependencias Externas | Mocks]]; para reutilizar preparación de estado, [[84 Fixtures Modulares | Fixtures Modulares]].
