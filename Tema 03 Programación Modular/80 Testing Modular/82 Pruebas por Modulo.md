---
title: Pruebas por Módulo
order: 82
tags:
  - python
  - teoria
  - testing
draft: false
aliases:
  - Pruebas por Modulo
  - Un test por módulo
  - tests/
---

# Pruebas por Módulo

> [!definicion]
> La organización modular de tests asigna **un archivo de test por módulo**: a `geometria.py` le corresponde `test_geometria.py`. La carpeta `tests/` **espeja** la estructura del paquete, de modo que cada módulo de producción tiene su contraparte de prueba en la misma posición relativa. Cada `test_<modulo>.py` verifica la **interfaz pública** de su módulo —las funciones y clases que otros módulos consumen—, no los detalles internos.

```python
# tests/test_geometria.py  -> prueba SOLO el módulo geometria
from mi_paquete.geometria import area_circulo, perimetro_circulo

def test_area_circulo():
    assert area_circulo(2) == 12.56636

def test_perimetro_circulo():
    assert perimetro_circulo(2) == 12.56636
```

Un test importa el módulo **por su interfaz pública** (los nombres que `geometria` exporta) y comprueba su comportamiento. Si el test importa funciones privadas (`_helper`), se acopla a la implementación y se rompe en cuanto esta cambie aunque la interfaz siga igual.

## La carpeta tests/ espeja el paquete

> [!regla]
> La convención es una carpeta `tests/` a la altura del paquete, con un `test_<modulo>.py` por cada módulo. La estructura de `tests/` **refleja** la del paquete: misma jerarquía de subcarpetas. Así, ante un módulo cualquiera se sabe de inmediato dónde está su test.

```tree
mi_proyecto/
├── mi_paquete/
│   ├── __init__.py
│   ├── geometria.py
│   ├── io_datos.py
│   └── utils/
│       └── validacion.py
└── tests/                       # espejo de mi_paquete/
    ├── test_geometria.py
    ├── test_io_datos.py
    └── utils/
        └── test_validacion.py
```

Con el paquete instalable (o `pytest` configurado), los tests importan los módulos con su ruta de paquete (`from mi_paquete.geometria import ...`), tal como lo haría el código real. Ejecutar `pytest` desde la raíz descubre toda la carpeta `tests/`.

## Probar la interfaz pública, no la privada

> [!info]
> Testear la **interfaz pública** mantiene los tests estables frente a *refactors*. Mientras la firma y el comportamiento públicos no cambien, el test sigue verde aunque las funciones internas se reescriban. Probar internos privados genera tests frágiles que fallan por cambios que no afectan a los consumidores.

```python
# geometria.py
def _grados_a_radianes(g):        # privado: detalle de implementación
    return g * 3.14159 / 180

def area_sector(radio, grados):   # público: forma parte de la interfaz
    rad = _grados_a_radianes(grados)
    return 0.5 * radio ** 2 * rad

# tests/test_geometria.py
from mi_paquete.geometria import area_sector

def test_area_sector():           # prueba lo público; ignora _grados_a_radianes
    assert area_sector(2, 180) == 6.28318
```

## Aislar el módulo bajo prueba

> [!ejemplo]
> Cada `test_<modulo>.py` debe ejercitar **un solo módulo**. Si ese módulo depende de otros (red, BD u otros módulos pesados), esas dependencias se **sustituyen** para que el test mida solo la lógica del módulo objetivo. Un fallo en `test_geometria.py` debe señalar a `geometria`, no a un módulo vecino.

```python
# Si geometria importara un servicio externo, se sustituye en el test
# para que la prueba dependa SOLO de geometria.
# -> ver Mocks para Dependencias Externas
```

El **aislamiento** de esas dependencias se logra con [[83 Mocks para Dependencias Externas | mocks]], y la **preparación de estado** reutilizable entre los tests de varios módulos con [[84 Fixtures Modulares | fixtures modulares]]. La mecánica base de `pytest` está en [[81 Pytest Basico | Pytest Básico]].
