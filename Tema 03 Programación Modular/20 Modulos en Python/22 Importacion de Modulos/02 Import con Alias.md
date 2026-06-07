---
title: Import con Alias
order: 2
tags:
  - python
  - teoria
  - modulos
draft: false
aliases:
  - import as
  - Alias de modulo
  - import numpy as np
---

# Import con Alias

> [!definicion]
> El **import con alias** —`import modulo as nombre`— trae el módulo bajo un **nombre alternativo** elegido por quien importa. El módulo sigue siendo el mismo objeto; solo cambia el identificador con que se referencia. Sirve para **acortar** nombres largos y para **evitar colisiones** con otros nombres del namespace.

```python
import numpy as np               # alias corto y convencional
import matplotlib.pyplot as plt

np.array([1, 2, 3])             # en vez de numpy.array(...)
plt.plot([0, 1], [0, 1])        # en vez de matplotlib.pyplot.plot(...)
```

El alias **reemplaza** al nombre original en el namespace actual: tras `import numpy as np`, el nombre `numpy` no queda definido; solo `np`.

## Convenciones: alias que todo el mundo reconoce

> [!regla]
> Ciertos alias son **convención de facto** y conviene respetarlos para que el código sea legible por cualquiera: `import numpy as np`, `import pandas as pd`, `import matplotlib.pyplot as plt`, `import tensorflow as tf`. Inventar alias propios para estas librerías perjudica la legibilidad más de lo que ayuda.

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({"x": np.arange(3)})   # alias estandar, reconocibles
```

## Evitar colisiones de nombres

> [!info]
> Cuando dos módulos comparten nombre (módulo local `json.py` frente a `json` estándar) o un nombre largo invade el código, el alias resuelve el choque sin tocar el resto. También se usa para renombrar un módulo a un nombre más expresivo en el contexto del proyecto.

```python
import datetime as dt           # mas corto, sin perder claridad
dt.datetime.now()

# import mi_paquete.json as cfg_json   -> evita chocar con el json estandar
```

> [!warning]
> El alias **no** crea un módulo nuevo ni una copia: `import math as m` deja `m is math` (el mismo objeto cacheado en `sys.modules`). Modificar `m.pi` modifica `math.pi`. El alias es solo otro nombre apuntando al mismo módulo.

El alias es una variante del [[01 Import Simple | import simple]] —mantiene el acceso cualificado, pero con otro prefijo—; cuando se quieren los nombres **sin** prefijo se usa el [[03 Import Selectivo (from import) | import selectivo]].
