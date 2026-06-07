---
title: Import Simple
order: 1
tags:
  - python
  - teoria
  - modulos
draft: false
aliases:
  - import modulo
  - Simple import
  - Importacion simple
---

# Import Simple

> [!definicion]
> El **import simple** —`import modulo`— trae el **módulo entero** al namespace actual bajo su propio nombre. Sus miembros se usan con **acceso cualificado**: `modulo.atributo`. Es la forma más explícita: en el punto de uso siempre se ve de qué módulo procede cada nombre.

```python
import math

math.pi                          # 3.141592653589793
math.sqrt(16)                    # 4.0
math.factorial(5)                # 120
```

Tras `import math`, lo único que entra al namespace es el nombre `math` (el objeto módulo). `pi` y `sqrt` **no** quedan sueltos: se llega a ellos siempre como `math.pi`, `math.sqrt`.

## Acceso cualificado: la ventaja de saber de dónde viene

> [!regla]
> Con `import modulo`, cada uso lleva el prefijo `modulo.`. Esto **evita colisiones** (`math.sqrt` y `cmath.sqrt` conviven sin ambigüedad) y deja el origen a la vista, a costa de algo más de verbosidad. Es la forma recomendada para módulos cuyo nombre es corto o cuyos nombres podrían chocar.

```python
import math
import statistics

math.sqrt(9)                     # 3.0   -> raiz real
statistics.mean([1, 2, 3])       # 2     -> sin ambiguedad de origen
```

## Se importa una sola vez: la caché

> [!info]
> Importar un módulo lo **ejecuta una vez** y lo guarda en `sys.modules`. Los `import` posteriores del mismo módulo —en este o en cualquier otro archivo— **no lo reejecutan**: reutilizan el objeto ya cargado. Por eso varios `import math` repartidos por el programa comparten el **mismo** objeto módulo y su estado.

```python
import sys
import math
"math" in sys.modules            # True   -> quedo cacheado
import math as m2                # no reejecuta math; reusa el cacheado
m2 is sys.modules["math"]        # True   -> es el mismo objeto
```

> [!warning]
> Como el módulo es único y compartido, **modificar** uno de sus atributos (`math.pi = 3`) afecta a **todos** los que lo usan en el programa. La caché es global; trata las constantes de un módulo como estado compartido.

El acceso cualificado se acorta con un [[02 Import con Alias | alias]], se sustituye por nombres directos con el [[03 Import Selectivo (from import) | import selectivo]], y la naturaleza cacheada del import es justo lo que hace delicada la [[04 Importacion Circular y Soluciones | importación circular]].
