---
title: Asociación
tags:
  - python
  - teoria
  - relaciones
draft: false
aliases:
  - Association
  - Asociación de objetos
---

# Asociación

> [!definicion]
> La **asociación** es la relación general **"usa un"** / **"se conoce con"**: dos objetos **independientes** se **referencian y colaboran**, **sin que uno sea parte del otro**. No hay contención ni propiedad: solo un vínculo por el que un objeto puede invocar al otro. Es **más débil que la agregación**, porque no implica "parte de".

```python
class Pedido:
    def __init__(self, importe):
        self.importe = importe

class Cliente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.pedidos = []
    def asociar(self, pedido):
        self.pedidos.append(pedido)     # el Cliente conoce sus Pedidos

ana = Cliente("Ana")
p = Pedido(50)
ana.asociar(p)
ana.pedidos[0].importe                  # 50 -> colabora con el Pedido
```

`Cliente` y `Pedido` **existen por separado** y ninguno *contiene* al otro como una de sus partes; simplemente se **conocen** para colaborar.

## Direccionalidad

> [!info]
> La asociación puede ser:
> - **Unidireccional**: solo un extremo conoce al otro (el `Cliente` referencia sus `Pedido`, pero el `Pedido` no al `Cliente`).
> - **Bidireccional**: ambos se referencian mutuamente y pueden navegarse en los dos sentidos.

```python
class Medico:
    def __init__(self, nombre):
        self.nombre = nombre
        self.pacientes = []

class Paciente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.medico = None

def asignar(medico, paciente):          # establece el vínculo en ambos sentidos
    medico.pacientes.append(paciente)
    paciente.medico = medico            # bidireccional

m, pac = Medico("Dr. House"), Paciente("Ana")
asignar(m, pac)
pac.medico.nombre                       # "Dr. House"
m.pacientes[0].nombre                   # "Ana"
```

> [!warning]
> Una asociación **bidireccional** introduce un ciclo de referencias y obliga a **mantener ambos extremos sincronizados**: al romper el vínculo hay que actualizar los dos lados, o quedarán referencias inconsistentes.

## Posición en el espectro de acoplamiento

> [!regla]
> Las relaciones "tiene/usa un" se ordenan de **más fuerte a más débil**:
> **composición** → **agregación** → **asociación** → **dependencia**.

| Relación | Vínculo | Fuerza |
| -------- | ------- | ------ |
| [[01 Composicion \| Composición]] | "tiene un" exclusivo, la parte muere con el todo | más fuerte |
| [[02 Agregacion \| Agregación]] | "tiene un" compartido, la parte sobrevive al todo | fuerte |
| Asociación | "usa un", objetos que se conocen y colaboran | media |
| [[04 Dependencia \| Dependencia]] | "depende de", uso puntual (parámetro, retorno) | más débil |

La asociación se distingue de la **agregación** en que **no expresa "parte de"** (solo "se conoce con"), y de la **dependencia** en que el vínculo es **persistente** (se guarda como atributo) en vez de existir solo durante una llamada concreta.
