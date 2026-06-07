---
title: Ocultamiento de Implementación
order: 1
tags:
  - python
  - teoria
  - modularidad
draft: false
aliases:
  - Ocultamiento de Implementación
  - Information Hiding
  - Convención _privado
---

# Ocultamiento de Implementación

> [!definicion]
> El **ocultamiento de implementación** consiste en **exponer el *qué* y esconder el *cómo***: un módulo publica una interfaz reducida (las funciones y clases que otros deben usar) y trata todo lo demás —helpers, constantes auxiliares, estado interno— como **detalle privado** sujeto a cambio. En Python no hay privacidad forzada, sino una **convención**: un nombre que empieza por guion bajo (`_nombre`) es **privado por contrato**.

```python
# tarifas.py
IVA = 0.21                         # publico: parte de la interfaz
def precio_final(base):            # publico: el "que"
    return round(base + _impuesto(base), 2)

def _impuesto(base):               # _privado: el "como", no usar desde fuera
    return base * IVA
```

## La convención del guion bajo

> [!regla]
> Un nombre con **un guion bajo inicial** (`_helper`, `_CACHE`) señala "**uso interno, no forma parte de la API**". Python **no lo impide**: nada bloquea acceder a `modulo._helper`. Es un pacto entre desarrolladores. Hacerlo significa **acoplarte a un detalle** que el autor del módulo puede cambiar sin avisar.

```python
import tarifas
tarifas.precio_final(100)          # OK -> interfaz publica
tarifas._impuesto(100)             # FUNCIONA, pero rompes el contrato:
                                   # manana _impuesto puede desaparecer
```

## Qué publicar y qué ocultar

> [!info]
> **Publicar** lo que el usuario del módulo **necesita** para hacer su tarea: las operaciones de alto nivel, las clases principales, las constantes de configuración. **Ocultar** todo lo que es **andamiaje**: validaciones internas, funciones auxiliares, cachés, variables temporales, dependencias que podrías sustituir. La regla práctica: **expón lo mínimo** que haga útil al módulo.

```python
# parser.py
def cargar(ruta):                  # PUBLICO: lo que el usuario quiere
    texto = _leer(ruta)
    return _analizar(texto)

def _leer(ruta):    ...            # privado: detalle de E/S
def _analizar(t):   ...            # privado: detalle de parseo
```

## Por qué importa: libertad para cambiar

> [!info]
> Si los demás módulos solo dependen de lo público, puedes **reescribir el interior** —cambiar algoritmos, renombrar helpers, reorganizar el estado— sin romper a nadie, siempre que la interfaz siga comportándose igual. Eso es precisamente lo que mantiene **bajo el acoplamiento**: la superficie de contacto entre módulos es pequeña y estable.

```python
# v1: _impuesto calcula con un porcentaje fijo
# v2: _impuesto consulta una tabla por pais
# Los consumidores de precio_final() NO cambian: el "que" es el mismo.
```

## Ocultar no es lo mismo que esconder errores

> [!warning]
> Ocultar implementación **no** significa silenciar fallos. Un módulo debe **propagar** sus errores por la interfaz (con excepciones claras) aunque oculte el código que los origina. Lo privado es el *mecanismo*, no las *consecuencias visibles* para quien lo usa.

El conjunto de nombres públicos que un módulo ofrece forma su **interfaz**, el contrato con el exterior, tratado en [[02 Interfaces entre Modulos | Interfaces entre Módulos]]. La forma explícita de declarar esa interfaz —la lista `__all__`— se aborda en [[60 Diseno de APIs Modulares/index | Diseño de APIs Modulares]].
