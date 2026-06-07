---
title: Interfaces Públicas vs Privadas
order: 61
tags:
  - python
  - teoria
  - apis
draft: false
aliases:
  - Public vs Private API
  - API Pública
  - Interfaz Privada
---

# Interfaces Públicas vs Privadas

> [!definicion]
> La **interfaz pública** (API) de un módulo es el conjunto de nombres que **prometes mantener estables** para quien lo importe: funciones, clases y constantes pensadas para uso externo. La **implementación privada** es todo lo demás —helpers, estado interno, detalles— que puedes **cambiar libremente** sin avisar. Python no tiene `private` real: la frontera se marca por **convención**, con un **guion bajo inicial** (`_nombre`) en lo privado.

```python
# calculadora.py
PRECISION = 4                     # publico: constante de la API

def redondear(x):                 # publico: contrato estable
    return round(_ajustar(x), PRECISION)

def _ajustar(x):                  # privado: detalle, el _ lo indica
    return x * 1.0
```

`redondear` y `PRECISION` forman el **contrato**: otros módulos los usan y cuentan con ellos. `_ajustar` es interno; aunque sea accesible (`calculadora._ajustar`), el guion bajo dice *"no dependas de esto, puede desaparecer"*.

## La convención `_nombre`

> [!regla]
> Un **único guion bajo inicial** (`_helper`, `_CACHE`) marca un nombre como **privado por convención**: sigue siendo accesible, pero señala que es implementación interna y queda **fuera del contrato**. No lo protege el intérprete; protege el acuerdo entre quien escribe y quien usa el módulo.

```python
import calculadora
calculadora.redondear(3.14159)    # OK -> uso previsto, es publico
calculadora._ajustar(2)           # funciona... pero violas la convencion
```

A nivel de **módulo** el guion bajo es solo señal social. Es distinto del **doble** guion bajo dentro de una clase (`__attr`), que sí activa el *name mangling* del intérprete; eso pertenece a la encapsulación de [[Tema 02 Programación Orientada a Objetos/index | POO]], no al diseño de módulos.

## Estabilidad de la API

> [!warning]
> Una vez un nombre es público, **otros dependen de él**: renombrarlo, cambiar su firma o eliminarlo **rompe** su código. Mantén la superficie pública **mínima y estable**; deja como `_privado` todo lo que aún pueda cambiar. Es más fácil **publicar después** algo privado que **retirar** algo que ya es público.

```python
# v1 publico
def cargar(ruta): ...

# v2: cambiar 'ruta' por 'path' rompe a TODOS los que llamaban cargar(ruta=...)
def cargar(path): ...             # cambio incompatible en la API publica
```

Por eso conviene exponer poco: cada función pública es un compromiso futuro. Lo que no forma parte del contrato se oculta con `_` y, cuando se quiere declarar la frontera de forma explícita, con [[62 Exposicion Selectiva (__all__) | __all__]].

## Documentar lo público

> [!info]
> Lo público se **documenta**; lo privado, como mucho, se comenta. Un **docstring** en cada función o clase pública describe su contrato —qué hace, qué recibe, qué devuelve— y es lo que ven `help()` y los IDE. Si un nombre merece docstring de cara al usuario, es señal de que pertenece a la API.

```python
def redondear(x):
    """Redondea x a PRECISION decimales. <- contrato visible en help()."""
    return round(_ajustar(x), PRECISION)

help(calculadora.redondear)       # muestra el docstring publico
```

Distinguir público de privado es el primer paso del [[60 Diseno de APIs Modulares/index | diseño de una API modular]]: define la **frontera**, y la nota siguiente la hace **explícita** con [[62 Exposicion Selectiva (__all__) | __all__]], que además controla qué se trae con `import *`.
