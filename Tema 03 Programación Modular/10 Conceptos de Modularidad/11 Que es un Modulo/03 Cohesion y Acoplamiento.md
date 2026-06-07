---
title: Cohesión y Acoplamiento
order: 3
tags:
  - python
  - teoria
  - modularidad
draft: false
aliases:
  - Cohesión y Acoplamiento
  - Cohesion and Coupling
  - Alta cohesión bajo acoplamiento
---

# Cohesión y Acoplamiento

> [!definicion]
> La **cohesión** mide cuánto se relaciona entre sí lo que hay **dentro** de un módulo; el **acoplamiento** mide cuánto **depende** un módulo de otros. El objetivo de toda buena división modular es **alta cohesión** (cada módulo hace **una** cosa) y **bajo acoplamiento** (los módulos se conocen lo mínimo, y solo a través de su interfaz pública).

```python
# ALTA cohesion: el modulo entero gira sobre UNA responsabilidad (geometria)
# geometria.py
def area_circulo(r):   ...
def perimetro_circulo(r): ...
def area_rectangulo(b, h): ...

# BAJO acoplamiento: depende de otro modulo por su INTERFAZ, no de sus detalles
import geometria
geometria.area_circulo(2)          # usa la funcion publica, ignora el "como"
```

## Alta cohesión: un módulo, una responsabilidad

> [!regla]
> Un módulo cohesivo tiene un **tema único**: todo lo que contiene contribuye a la misma responsabilidad y podrías describirlo en una frase sin la palabra "y". Si un módulo "valida entradas **y** envía emails **y** dibuja gráficos", su cohesión es baja: son tres módulos disfrazados de uno.

```python
# BAJA cohesion -> tres responsabilidades en un archivo
# utilidades.py
def validar_email(e): ...
def conectar_bd(): ...
def renderizar_html(p): ...

# ALTA cohesion -> separadas
# validacion.py  -> validar_email
# bd.py          -> conectar_bd
# plantillas.py  -> renderizar_html
```

## Bajo acoplamiento: depender de la interfaz, no de los detalles

> [!regla]
> Dos módulos están **poco acoplados** cuando uno usa al otro solo a través de su **interfaz pública** (sus funciones y clases documentadas) e ignora **cómo** está implementado por dentro. Así, reescribir las tripas de un módulo no rompe a quienes lo usan, mientras la interfaz no cambie.

```python
# ALTO acoplamiento -> el consumidor hurga en detalles internos
import config
config._cache["clave"]             # depende de una estructura interna fragil

# BAJO acoplamiento -> usa la interfaz publica estable
import config
config.obtener("clave")            # da igual como se guarde por dentro
```

## Por qué buscar las dos a la vez

> [!info]
> Cohesión y acoplamiento son **dos caras del mismo diseño**. Cuando cada módulo concentra una responsabilidad (alta cohesión), las dependencias entre módulos se vuelven **pocas y claras** (bajo acoplamiento) de forma natural. Al revés, un módulo que hace de todo acaba **enredado** con muchos otros. La meta clásica del diseño modular se resume en **"alta cohesión, bajo acoplamiento"**.

| | Alta cohesión | Baja cohesión |
| --- | --- | --- |
| **Bajo acoplamiento** | objetivo: módulos limpios y reutilizables | módulos poco enfocados pero aislados |
| **Alto acoplamiento** | módulos buenos pero muy entrelazados | el peor caso: un *espagueti* de dependencias |

## Síntomas de mal diseño

> [!warning]
> Señales de **alto acoplamiento**: importaciones que se vuelven **circulares**, acceder a nombres `_privados` de otro módulo, o que un cambio pequeño obligue a tocar muchos archivos. Señal de **baja cohesión**: un módulo `utils.py` o `misc.py` donde acaba todo lo que no encaja en otro sitio.

La técnica concreta para mantener bajo el acoplamiento —exponer una interfaz estable y ocultar el resto— es la [[12 Abstraccion y Encapsulacion Modular/index | abstracción y encapsulación modular]]. Las importaciones circulares, síntoma típico de acoplamiento excesivo, se tratan en [[20 Modulos en Python/index | Módulos en Python]].
