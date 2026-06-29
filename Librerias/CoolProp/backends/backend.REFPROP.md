---
title: backend.REFPROP — NIST REFPROP (maxima precision, requiere licencia)
aliases:
  - REFPROP
  - NIST REFPROP
  - backend de referencia
tags:
  - coolprop
  - backend
  - refprop
lib: coolprop
tipo: concepto
draft: false
---

# backend.REFPROP — NIST REFPROP

`REFPROP` es el [[concepto_backend|backend]] que delega el cálculo en **REFPROP** (REFerence fluid PROPerties), la librería del NIST que es la **referencia mundial de máxima precisión** para propiedades termofísicas. A diferencia de [[backend.HEOS|HEOS]], [[backend.IF97|IF97]] o [[backend.SRK|SRK]], REFPROP **no viene incluido con CoolProp**: es software comercial del NIST que requiere **licencia** y debe **instalarse aparte**. CoolProp simplemente actúa de puente hacia él si lo encuentra en el sistema.

## Qué modelo usa

REFPROP usa las mismas familias de ecuaciones de estado de Helmholtz de referencia que HEOS, pero mantenidas y certificadas directamente por el NIST, con sus modelos de mezcla y de transporte más recientes. Es el estándar contra el que se comparan los demás. En la práctica, para fluidos puros comunes los resultados de HEOS y REFPROP son muy próximos; la diferencia importa en mezclas y en aplicaciones donde se exige trazabilidad a la referencia del NIST.

## Sintaxis

```python
from CoolProp.CoolProp import PropsSI

# Solo funciona si REFPROP esta instalado y licenciado en el sistema
rho = PropsSI('D', 'T', 300, 'P', 1e5, 'REFPROP::R134a')
```

Con [[AbstractState]], el backend es el primer argumento del constructor: `CP.AbstractState('REFPROP', 'R134a')`.

## Comprobar si REFPROP está disponible (CLAVE)

Antes de usar este backend, **comprueba que está instalado**. La forma canónica es preguntar por su versión:

```python
import CoolProp.CoolProp as CP

version = CP.get_global_param_string('REFPROP_version')
print(version)
```

- Si devuelve algo como `'10.0'`, REFPROP está instalado y operativo.
- Si devuelve `'n/a'` (o lanza un mensaje de error de carga de librería), **REFPROP NO está disponible** en ese sistema.

> [!warning] En ESTE entorno REFPROP NO está instalado (verificado)
> Ejecutado aquí, `CP.get_global_param_string('REFPROP_version')` devolvió **`'n/a'`**, acompañado de un mensaje indicando que no se pudo cargar la librería (`librefprop.so` no encontrada en `/opt/refprop/`). Por tanto, en este entorno cualquier llamada con `'REFPROP::...'` fallaría: hay que usar [[backend.HEOS|HEOS]].

## Qué hacer si no está: fallback a HEOS

Como REFPROP puede no estar presente, el patrón robusto es **detectarlo y caer en HEOS** si falta. HEOS da resultados muy cercanos para fluidos puros y siempre está disponible:

```python
import CoolProp.CoolProp as CP
from CoolProp.CoolProp import PropsSI

def backend_preferido():
    """Devuelve 'REFPROP' si esta instalado; si no, 'HEOS'."""
    version = CP.get_global_param_string('REFPROP_version')
    return 'REFPROP' if version not in ('', 'n/a') else 'HEOS'

bk = backend_preferido()                       # en este entorno -> 'HEOS'
rho = PropsSI('D', 'T', 300, 'P', 1e5, f'{bk}::R134a')
print(bk, rho)                                 # -> HEOS 4.173095241719476 kg/m3
```

Así el mismo código corre en una máquina con licencia REFPROP (usando la referencia) y en una sin ella (usando HEOS), sin tocar nada más: ese es el espíritu de los backends intercambiables.

## Cuándo usarlo

- Cuando necesitas la **máxima precisión de referencia** y tienes **licencia** del NIST.
- Cuando un cálculo debe ser **trazable al estándar REFPROP** (informes, certificación, validación).
- Para **mezclas** donde los modelos del NIST son los más fiables.

En cualquier otro caso, o si no hay licencia, [[backend.HEOS|HEOS]] es la opción por defecto y suficiente para la mayoría de la ingeniería.

## Notas relacionadas

- [[concepto_backend]] — qué es un backend y la sintaxis `BACKEND::Fluido`
- [[backend.HEOS]] — el motor por defecto y el fallback natural cuando REFPROP no está
- [[CoolProp.PropsSI]] — donde se escribe el prefijo `REFPROP::`
- [[AbstractState]] — el backend es el primer argumento del constructor
