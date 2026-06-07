---
title: Definición y Propósito
order: 1
tags:
  - python
  - teoria
  - modularidad
draft: false
aliases:
  - Definición de Módulo
  - Module definition
  - Módulo vs script
---

# Definición y Propósito

> [!definicion]
> Un **módulo** es una **unidad de código reutilizable con su propio espacio de nombres**. En Python, todo archivo `.py` es un módulo: al importarlo, su contenido (funciones, clases, variables) queda accesible como **atributos** de un objeto `module`, bajo el nombre del archivo. Su propósito es triple: **organizar** el código, **reutilizarlo** sin copiar y **aislar nombres** para evitar colisiones.

```python
# geometria.py  -> el archivo es el modulo "geometria"
PI = 3.14159
def area_circulo(r):
    return PI * r ** 2

# main.py  -> consume geometria por su namespace
import geometria
geometria.area_circulo(2)          # 12.566...  -> acceso cualificado
geometria.PI                       # 3.14159
type(geometria)                    # <class 'module'>
```

El nombre del módulo (`geometria`) actúa como **prefijo**: `geometria.PI` no choca con un `PI` definido en `main.py`. Ese aislamiento es el *namespace propio* del módulo.

## Los tres propósitos

> [!info]
> - **Organizar**: agrupar código relacionado en un archivo con un nombre con sentido (`io_datos.py`, `validacion.py`), en vez de un único fichero gigante.
> - **Reutilizar**: un módulo se importa desde cualquier programa; la lógica se escribe **una vez** y se usa en muchos sitios.
> - **Dar espacio de nombres**: cada módulo tiene su propio `__dict__`, así que dos módulos pueden definir `config` o `procesar` sin pisarse.

```python
import geometria
import fisica
geometria.PI                       # 3.14159   -> el de geometria
fisica.PI                          # 3.14159265 -> el de fisica, independiente
```

## Módulo frente a script

> [!regla]
> El mismo archivo `.py` puede usarse de dos formas. Como **script** se **ejecuta** directamente (`python archivo.py`): es el punto de entrada del programa. Como **módulo** se **importa** desde otro código (`import archivo`): aporta definiciones reutilizables. La diferencia no está en el archivo, sino en **cómo se invoca**.

```python
# herramienta.py
def saludar(nombre):
    return f"Hola, {nombre}"

# como SCRIPT:  python herramienta.py   -> se ejecuta de arriba a abajo
# como MODULO:  import herramienta       -> solo se cargan las definiciones
#                herramienta.saludar("Ana")
```

Un buen módulo suele estar pensado para **ser importado**; un script, para **ser ejecutado**. El idioma que decide qué código corre solo al ejecutar como script —y no al importar— es `if __name__ == "__main__":`, detallado en [[20 Modulos en Python/index | Módulos en Python]].

## Importar no es copiar

> [!warning]
> Importar un módulo **ejecuta su código una vez** y **cachea** el objeto resultante. Importarlo de nuevo en otro punto del programa reutiliza esa misma instancia (vía `sys.modules`), no vuelve a ejecutarlo. Por eso el código a nivel superior de un módulo solo debe tener **definiciones** y configuración ligera, no efectos secundarios pesados.

```python
import geometria       # ejecuta geometria.py
import geometria       # NO lo reejecuta: reutiliza el modulo cacheado
```

Por qué dividir en módulos en lugar de un solo archivo se desarrolla en [[02 Ventajas de la Modularidad | Ventajas de la Modularidad]]; cómo saber si una división concreta es acertada, en [[03 Cohesion y Acoplamiento | Cohesión y Acoplamiento]].
