---
title: np/manipulacion_forma/reordenar_ejes — permutar dimensiones
tags:
  - numpy
  - indice
draft: false
---

# np/manipulacion_forma/reordenar_ejes — permutar dimensiones

`reordenar_ejes/` cambia el orden de los ejes de un array sin mover los datos en memoria: solo se modifican los `strides`. Es fundamental para algebra lineal (transponer matrices) y para preparar arrays para broadcasting cuando los ejes no estan en el orden esperado.

Las tres funciones difieren en granularidad: `np.transpose` actua sobre todos los ejes a la vez, `np.moveaxis` mueve uno o varios ejes a posiciones arbitrarias y `np.swapaxes` intercambia exactamente dos.

## Funciones

| Funcion | Que hace | Nivel de control |
|---------|----------|-----------------|
| [[np.transpose]] | Invierte o permuta todos los ejes segun un patron | Global |
| [[np.moveaxis]] | Mueve uno o varios ejes a posiciones especificas | Selectivo |
| [[np.swapaxes]] | Intercambia exactamente dos ejes entre si | Par de ejes |

## Notas relacionadas

- [[np.transpose]]
- [[np.moveaxis]]
- [[np.swapaxes]]
