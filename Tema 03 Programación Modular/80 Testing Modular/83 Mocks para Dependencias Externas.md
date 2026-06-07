---
title: Mocks para Dependencias Externas
order: 83
tags:
  - python
  - teoria
  - testing
draft: false
aliases:
  - Mocks
  - unittest.mock
  - patch
  - monkeypatch
---

# Mocks para Dependencias Externas

> [!definicion]
> Un **mock** es un objeto **falso** que sustituye a una dependencia real durante un test. Aísla el módulo bajo prueba de recursos externos —**red, disco, base de datos, hora del sistema**— que son lentos, no deterministas o indeseables en un test. Python ofrece `unittest.mock` (`Mock`, `MagicMock`, `patch`) y `pytest` ofrece la *fixture* `monkeypatch`. La idea común: **reemplazar** la dependencia por un doble controlado y verificar cómo el módulo interactúa con ella.

```python
from unittest.mock import Mock

api = Mock()                      # objeto falso: cualquier atributo/llamada es válido
api.obtener_usuario.return_value = {"id": 1, "nombre": "Ada"}

api.obtener_usuario(1)            # {'id': 1, 'nombre': 'Ada'}  -> valor simulado
api.obtener_usuario.assert_called_once_with(1)   # verifica la interacción
```

El `Mock` no llama a ninguna API real: devuelve lo que se le configura en `return_value` y **registra** cómo se le llamó, lo que permite afirmar sobre la interacción.

## patch: sustituir en el sitio donde se usa

> [!regla]
> `patch` reemplaza temporalmente un objeto **por la ruta donde se importa y usa**, no donde se define. Si `clima.py` hace `import requests` y llama `requests.get`, se parchea `"clima.requests.get"`. Al salir del `with` (o terminar el test), `patch` **restaura** el original automáticamente.

```python
# clima.py  -> el módulo bajo prueba
import requests

def temperatura(ciudad):
    resp = requests.get(f"https://api/clima/{ciudad}")
    return resp.json()["temp"]

# tests/test_clima.py
from unittest.mock import patch
from mi_paquete import clima

def test_temperatura():
    with patch("mi_paquete.clima.requests.get") as mock_get:   # parchea en clima
        mock_get.return_value.json.return_value = {"temp": 21}
        assert clima.temperatura("Madrid") == 21               # no toca la red
        mock_get.assert_called_once()
```

`patch` también funciona como **decorador**; entonces inyecta el mock como primer argumento del test:

```python
@patch("mi_paquete.clima.requests.get")
def test_temperatura_decorador(mock_get):
    mock_get.return_value.json.return_value = {"temp": 21}
    assert clima.temperatura("Madrid") == 21
```

## monkeypatch: el equivalente de pytest

> [!info]
> `monkeypatch` es una *fixture* de `pytest` que modifica atributos, variables de entorno o el `cwd` y **deshace** los cambios al acabar el test. Se recibe como argumento. Es la forma idiomática en `pytest` de sustituir una dependencia sin gestores de contexto.

```python
# tests/test_clima.py
def test_temperatura_monkeypatch(monkeypatch):
    def fake_get(url):
        respuesta = Mock()
        respuesta.json.return_value = {"temp": 21}
        return respuesta
    monkeypatch.setattr(clima.requests, "get", fake_get)   # reemplaza get
    assert clima.temperatura("Madrid") == 21
```

```python
# monkeypatch también para variables de entorno
def test_config(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-123")    # se restaura al final
    assert leer_api_key() == "test-123"
```

## Verificar la interacción, no solo el retorno

> [!ejemplo]
> Un mock no solo simula valores: **graba** cada llamada. Eso permite afirmar **cómo** se usó la dependencia —con qué argumentos y cuántas veces—, clave cuando el efecto del módulo es la propia llamada (enviar un correo, escribir en BD) y no un valor de retorno.

```python
from unittest.mock import patch

def test_envia_alerta():
    with patch("mi_paquete.alertas.smtp_enviar") as mock_envio:
        mi_paquete.alertas.notificar("caída")
        mock_envio.assert_called_once_with(asunto="caída")  # afirma la interacción
```

Con las dependencias aisladas, los tests de cada módulo quedan rápidos y deterministas. La **preparación reutilizable** de esos mocks y del estado de prueba se centraliza en [[84 Fixtures Modulares | Fixtures Modulares]]; el reparto por módulos está en [[82 Pruebas por Modulo | Pruebas por Módulo]] y la base de ejecución en [[81 Pytest Basico | Pytest Básico]].
