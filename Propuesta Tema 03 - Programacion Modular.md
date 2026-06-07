---
title: Propuesta Tema 03 - Programación Modular
draft: true
tags:
  - propuesta
  - estructura
  - modular
---

# Propuesta de estructura — Tema 03: Programación Modular

> [!info] Propósito
> Estructura de archivos **propuesta** (no redactada aún) para el `Tema 03 Programación Modular`,
> continuación de [[Tema 01 Programación Orientada a Procesos/index | Tema 01]] (Procesos) y
> [[Tema 02 Programación Orientada a Objetos/index | Tema 02]] (POO).
> Fuente: **Capítulo 3** de `Conocimiento-Listado.md`. Este `.md` es para revisar y ajustar el
> árbol **antes** de crear la rama de desarrollo y rellenar las notas.

## Convención aplicada (igual que Tema 01 / Tema 02)

- **Carpeta de sección**: prefijo `X0` (`10`, `20`, … `90`); `00 Referencias`.
- **Hijo directo de una sección**: prefijo `‹decena›‹n›`, sea **carpeta** (`21`) o **nota** (`61`).
- **Hoja dentro de una subcarpeta**: `01`, `02`, `03`…
- `index.md` en cada carpeta (nota madre).
- Nombres de archivo/carpeta **sin tildes** (ASCII); `__dunder__` y signos sí se conservan.
- Frontmatter de cada nota:
  ```yaml
  ---
  title: Definición y Propósito      # nombre sin número, en español con tildes
  order: 1                            # solo el número del prefijo (index = nº de su carpeta)
  tags: [python, teoria, modular]
  draft: false
  aliases: [...]
  ---
  ```

## Árbol propuesto

```tree
Tema 03 Programación Modular/
│
├── index.md                                    # order 0 — mapa del tema
│
├── 00 Referencias/
│   ├── index.md                                # order 0
│   ├── Glosario Modular.md                      # modulo, paquete, namespace, import, __all__…
│   └── Catalogo de Archivos Especiales.md       # __init__.py, __main__.py, __version__.py, __all__
│
├── 10 Conceptos de Modularidad/
│   ├── index.md                                # order 10
│   ├── 11 Que es un Modulo/
│   │   ├── index.md                            # order 11
│   │   ├── 01 Definicion y Proposito.md
│   │   ├── 02 Ventajas de la Modularidad.md
│   │   └── 03 Cohesion y Acoplamiento.md        # alta cohesion / bajo acoplamiento
│   └── 12 Abstraccion y Encapsulacion Modular/
│       ├── index.md                            # order 12
│       ├── 01 Ocultamiento de Implementacion.md
│       └── 02 Interfaces entre Modulos.md
│
├── 20 Modulos en Python/
│   ├── index.md                                # order 20
│   ├── 21 Estructura de Modulos/
│   │   ├── index.md                            # order 21
│   │   ├── 01 Archivos .py como Modulos.md
│   │   ├── 02 Namespace del Modulo.md           # __dict__, globals() del modulo
│   │   └── 03 __name__ y __main__.md            # if __name__ == "__main__"
│   └── 22 Importacion de Modulos/
│       ├── index.md                            # order 22
│       ├── 01 Import Simple.md
│       ├── 02 Import con Alias.md               # import numpy as np
│       ├── 03 Import Selectivo (from import).md
│       └── 04 Importacion Circular y Soluciones.md
│
├── 30 Paquetes y Subpaquetes/
│   ├── index.md                                # order 30
│   ├── 31 Estructura de Paquetes/
│   │   ├── index.md                            # order 31
│   │   ├── 01 __init__.py y Directorios.md
│   │   ├── 02 Namespace de Paquetes.md
│   │   └── 03 Paquetes Anidados.md
│   └── 32 Sistemas de Importacion/
│       ├── index.md                            # order 32
│       ├── 01 Import Absoluto.md
│       ├── 02 Import Relativo.md                # from . import x ; from ..pkg import y
│       └── 03 Paquetes Namespace (PEP 420).md
│
├── 40 Sistema de Modulos de Python/
│   ├── index.md                                # order 40
│   ├── 41 Jerarquia de Modulos/
│   │   ├── index.md                            # order 41
│   │   ├── 01 Modulos Built-in.md
│   │   ├── 02 Libreria Estandar.md
│   │   ├── 03 Modulos de Terceros.md            # pip / PyPI
│   │   └── 04 Modulos Personalizados.md
│   └── 42 Mecanismos de Importacion/
│       ├── index.md                            # order 42
│       ├── 01 sys.path y PYTHONPATH.md
│       ├── 02 sys.modules (Cache).md
│       └── 03 Reloading (importlib.reload).md
│
├── 50 Organizacion de Proyectos/
│   ├── index.md                                # order 50
│   ├── 51 Archivos Especiales/                  # carpeta -> va primero (regla "directorios antes que archivos")
│   │   ├── index.md                            # order 51
│   │   ├── 01 __init__.py.md                    # inicializacion y exportacion
│   │   ├── 02 __main__.py.md                    # punto de entrada ejecutable (python -m)
│   │   └── 03 __version__.py.md                 # control de version
│   ├── 52 Estructura de Directorios.md          # layout src/ vs flat
│   └── 53 Module vs Package vs Subpackage.md
│
├── 60 Diseno de APIs Modulares/
│   ├── index.md                                # order 60
│   ├── 61 Interfaces Publicas vs Privadas.md    # convencion _privado
│   ├── 62 Exposicion Selectiva (__all__).md
│   └── 63 Facade Pattern.md                     # simplificar la API publica
│
├── 70 Patrones de Diseno Modular/
│   ├── index.md                                # order 70
│   ├── 71 Registry Pattern.md                   # registro de componentes
│   ├── 72 Plugin Architecture.md                # sistema extensible
│   └── 73 Module Factory.md                     # creacion dinamica (importlib)
│
└── 80 Testing Modular/
    ├── index.md                                # order 80
    ├── 81 Pytest Basico.md                      # (enriquecimiento sugerido en el propio doc fuente)
    ├── 82 Pruebas por Modulo.md
    ├── 83 Mocks para Dependencias Externas.md   # unittest.mock
    └── 84 Fixtures Modulares.md
```

## Recuento

| Bloque | Subcarpetas | Notas de concepto | index.md |
|--------|:-----------:|:-----------------:|:--------:|
| 00 Referencias | 0 | 2 | 1 |
| 10 Conceptos de Modularidad | 2 | 5 | 3 |
| 20 Modulos en Python | 2 | 7 | 3 |
| 30 Paquetes y Subpaquetes | 2 | 6 | 3 |
| 40 Sistema de Modulos | 2 | 7 | 3 |
| 50 Organizacion de Proyectos | 1 | 5 | 2 |
| 60 Diseno de APIs Modulares | 0 | 3 | 1 |
| 70 Patrones de Diseno Modular | 0 | 3 | 1 |
| 80 Testing Modular | 0 | 4 | 1 |
| raíz | — | — | 1 |
| **Total** | **11** | **42** | **19** |

**≈ 61 notas** (42 de concepto + 19 índices).

## Decisiones de diseño (para validar)

1. **Mapeo fiel al Capítulo 3** del listado: las 8 áreas del capítulo son las secciones 10–80.
   Profundidad mixta permitida: secciones grandes anidan (10–40), las pequeñas son planas (60–80).
2. **Sección 50 — caso de contenedor mixto**: tiene una subcarpeta (`51 Archivos Especiales`) y
   dos notas sueltas (`52`, `53`). Por tu regla *"directorios antes que archivos"*, la carpeta
   va primero (`51`). Si prefieres el orden pedagógico (Estructura de Directorios → Archivos
   Especiales) lo reordeno.
3. **Enriquecimiento mínimo** sobre el listado: añadí `81 Pytest Basico` porque el propio
   `Conocimiento-Listado.md` (opinión de ChatGPT) recomienda introducir testing básico aquí, y
   `Catalogo de Archivos Especiales` como nota de referencia rápida. Si quieres ceñirme 100% al
   listado, los quito.
4. **Importación circular** queda como hoja propia (`22/04`) por ser un problema consultado de
   forma aislada.

## Pendiente de tu decisión

- ¿Apruebas el árbol tal cual, o ajusto secciones/granularidad?
- ¿Sección 50 con "directorios primero" o con orden pedagógico?
- ¿Mantengo los 2 nodos de enriquecimiento (`Pytest Basico`, `Catalogo de Archivos Especiales`)?

## Siguiente paso (tras tu visto bueno)

1. Crear rama `refactor/tema-03-modular` (o `feat/tema-03-modular`) desde `main`.
2. Crear el árbol de carpetas + `index.md`.
3. Redactar las hojas con `redactar-nota` (en lotes, con verificación), estilo idéntico a Tema 02.
4. Merge a `main` y push, como en los temas anteriores.

> Fuente del temario: `Conocimiento-Listado.md` → **CAPÍTULO 3: PROGRAMACIÓN MODULAR**.
> Convención de nombres/orden: ver memoria `tema-naming-order-convention`.
