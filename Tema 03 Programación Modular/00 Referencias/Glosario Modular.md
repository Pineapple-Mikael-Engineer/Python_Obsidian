---
title: Glosario Modular
order: 2
tags:
  - python
  - teoria
  - modular
draft: false
aliases:
  - Glosario de Programación Modular
  - Términos Modular
---

# Glosario Modular

Definiciones breves de los términos del paradigma modular en Python. Entrada de consulta para fijar el significado preciso; el desarrollo de cada concepto se delega a su sección. El catálogo de los archivos y atributos `__x__` referidos aquí está en [[Catalogo de Archivos Especiales | Catálogo de Archivos Especiales]].

## Unidades de organización

| Término | Definición breve |
| ------- | ---------------- |
| Módulo | Archivo `.py` con su propio namespace; unidad mínima de organización e importación. Ver [[20 Modulos en Python/index \| Módulos en Python]] |
| Paquete | Directorio con `__init__.py` que agrupa módulos y subpaquetes bajo un namespace común. Ver [[30 Paquetes y Subpaquetes/index \| Paquetes y Subpaquetes]] |
| Subpaquete | Paquete anidado dentro de otro paquete; un directorio con `__init__.py` interior. Ver [[03 Paquetes Anidados \| Paquetes Anidados]] |
| Namespace | Espacio de nombres que asocia identificadores a objetos; cada módulo tiene el suyo (`modulo.__dict__`). Evita colisiones entre módulos. Ver [[02 Namespace del Modulo \| Namespace del Módulo]] |
| Namespace package (PEP 420) | Paquete **sin** `__init__.py` que puede repartirse entre varios directorios de `sys.path`; el intérprete lo une vía `__path__`. Ver [[03 Paquetes Namespace (PEP 420) \| Paquetes Namespace]] |

## Importación

| Término | Definición breve |
| ------- | ---------------- |
| Import absoluto | Importación por la ruta completa desde la raíz del proyecto: `from mi_paquete.sub import x`. Preferido por claridad. Ver [[01 Import Absoluto \| Import Absoluto]] |
| Import relativo | Importación relativa al paquete actual con puntos: `from . import x`, `from ..pkg import y`. Solo dentro de paquetes. Ver [[02 Import Relativo \| Import Relativo]] |
| Import circular | Dos módulos que se importan mutuamente; provoca `ImportError` o nombres a medio definir. Se rompe difiriendo el import o reorganizando. Ver [[04 Importacion Circular y Soluciones \| Importación Circular]] |

## Diseño de módulos

| Término | Definición breve |
| ------- | ---------------- |
| Cohesión | Grado en que los elementos de un módulo pertenecen juntos; **alta** cohesión = una sola responsabilidad clara. Ver [[03 Cohesion y Acoplamiento \| Cohesión y Acoplamiento]] |
| Acoplamiento | Grado de dependencia entre módulos; **bajo** acoplamiento = mínimas dependencias, a través de interfaces. Ver [[03 Cohesion y Acoplamiento \| Cohesión y Acoplamiento]] |
| Interfaz | Conjunto de nombres que un módulo ofrece al exterior como contrato de uso; oculta la implementación. Ver [[02 Interfaces entre Modulos \| Interfaces entre Módulos]] |
| API pública | Parte de la interfaz declarada estable y de uso externo; en Python se marca con `__all__` y la ausencia de `_` inicial. Ver [[61 Interfaces Publicas vs Privadas \| Interfaces Públicas vs Privadas]] |

## Maquinaria de importación

| Término | Definición breve |
| ------- | ---------------- |
| `sys.path` | Lista de directorios donde el intérprete busca módulos al importar; se recorre en orden. Ver [[01 sys.path y PYTHONPATH \| sys.path y PYTHONPATH]] |
| `PYTHONPATH` | Variable de entorno que añade directorios a `sys.path` antes de arrancar. Ver [[01 sys.path y PYTHONPATH \| sys.path y PYTHONPATH]] |
| `sys.modules` | Diccionario caché de los módulos ya importados; un segundo import reusa la entrada en vez de reejecutar. Ver [[02 sys.modules (Cache) \| sys.modules]] |
| `importlib` | Módulo estándar que expone el sistema de importación: `import_module`, `reload`, carga dinámica. Ver [[03 Reloading (importlib.reload) \| Reloading]] |

## Librerías y testing

| Término | Definición breve |
| ------- | ---------------- |
| Librería estándar | Conjunto de módulos que vienen con Python sin instalar nada (`os`, `sys`, `json`, ...). Ver [[02 Libreria Estandar \| Librería Estándar]] |
| Módulo built-in | Módulo compilado en el propio intérprete (escrito en C), sin archivo `.py` (`sys`, `builtins`, `math`). Ver [[01 Modulos Built-in \| Módulos Built-in]] |
| Fixture | Estado o recurso preparado de antemano para una prueba (datos, conexión, objeto); en `pytest`, función decorada con `@pytest.fixture`. Ver [[84 Fixtures Modulares \| Fixtures Modulares]] |
| Mock | Objeto sustituto que imita una dependencia externa para aislar la prueba; vía `unittest.mock`. Ver [[83 Mocks para Dependencias Externas \| Mocks]] |
