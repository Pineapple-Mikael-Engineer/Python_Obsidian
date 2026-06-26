---
title: patrones — las recetas que combinan todo lo de Manim
aliases:
  - patrones
  - recetas
tags:
  - manim
  - indice
lib: manim
order: 10
draft: false
---

# patrones — las recetas que combinan todo lo de Manim

Esta carpeta reúne las **recetas** de Manim: plantillas de código completas y ejecutables que resuelven una tarea concreta de principio a fin. A diferencia de las otras carpetas —que documentan piezas sueltas (una clase, un método, un concepto)—, aquí cada nota **combina** varias de esas piezas en un patrón que se copia y se adapta. Son las cuatro cosas que separan a quien ha leído sobre Manim de quien sabe usarlo: el **esqueleto mínimo** de una escena, crear tus propios **objetos** y **animaciones** subclaseando, y la **gráfica de función** completa con ejes y `c2p`. Si las otras carpetas enseñan el vocabulario, esta enseña a escribir frases. Empieza por [[escena_basica]] si arrancas de cero; salta a [[grafica_de_funcion]] si lo tuyo son las matemáticas.

## Las recetas

Las cuatro recetas, con el problema que resuelven y las piezas de las otras carpetas que combinan.

| Patron | Resuelve | Conceptos que combina |
|--------|----------|------------------------|
| [[escena_basica]] | el esqueleto mínimo para que algo aparezca y se anime | `Scene` + `construct` + `self.play`/`add`/`wait` + el comando `manim` |
| [[mobject_personalizado]] | crear un objeto dibujable propio y reutilizable | herencia de `VMobject` + `super().__init__()` + componer submobjects o fijar puntos |
| [[animacion_personalizada]] | crear un movimiento a medida que no viene de fábrica | herencia de `Animation` + `interpolate_mobject(alpha)` + `starting_mobject` + `rate_func` |
| [[grafica_de_funcion]] | graficar `y = f(x)` con punto, área, tangente o Riemann | `Axes` + `plot` + `c2p` + `ValueTracker`/`always_redraw` |

## Como elegir

Eliges la receta por lo que necesitas hacer, no por la clase que usa.

| Necesito… | Receta |
|-----------|--------|
| Arrancar un archivo nuevo / que algo aparezca por primera vez | [[escena_basica]] |
| Una figura propia que repito y quiero con nombre y parámetros | [[mobject_personalizado]] |
| Un efecto o movimiento que ninguna animación de fábrica cubre | [[animacion_personalizada]] |
| Dibujar una función, un punto sobre ella, un área o una tangente | [[grafica_de_funcion]] |
| Que un punto recorra una curva animado | [[grafica_de_funcion]] (variación con `ValueTracker`) |

La progresión natural es de arriba abajo: el esqueleto primero, los objetos y animaciones propios cuando lo de fábrica se queda corto, y la gráfica de función como aplicación que junta varias piezas a la vez.

## Una escena que usa varias

Una sola escena que combina **tres** patrones: el esqueleto base ([[escena_basica]]), un Mobject propio ([[mobject_personalizado]]) y la gráfica de función ([[grafica_de_funcion]]). Define una clase `Marcador` propia (un punto con halo) y la usa para señalar el máximo de una parábola graficada sobre `Axes`, anclándolo con `c2p`.

```python
from manim import *

class Marcador(VMobject):                          # patron: mobject_personalizado
    def __init__(self, color=YELLOW, **kwargs):
        super().__init__(**kwargs)                 # super().__init__ lo primero
        self.add(
            Dot(color=color),                      # el punto
            Circle(radius=0.3, color=color, stroke_width=2),  # el halo alrededor
        )

class MaximoDeParabola(Scene):                     # patron: escena_basica (esqueleto)
    def construct(self):
        ax = Axes(x_range=[-3, 3, 1], y_range=[-1, 9, 2])      # patron: grafica_de_funcion
        curva = ax.plot(lambda x: x**2, color=BLUE)
        etiquetas = ax.get_axis_labels(x_label="x", y_label="y")

        marca = Marcador().move_to(ax.c2p(0, 0))   # el minimo en (0, 0), anclado con c2p

        self.play(Create(ax), Write(etiquetas))
        self.play(Create(curva))
        self.play(FadeIn(marca))
        self.wait()
```

```bash
manim -pql archivo.py MaximoDeParabola      # -p reproduce, -ql = calidad baja (rapido)
```

## Notas relacionadas

- [[concepto_scene_construct]] — el modelo mental de la Scene y `construct` en el que se apoya [[escena_basica]]
- [[concepto_herencia_mobjects]] — la base de [[mobject_personalizado]] y [[animacion_personalizada]]: subclasear para crear lo propio
- [[Axes]] — la clase central de [[grafica_de_funcion]], con `c2p`, `plot` y el cálculo
- [[Manim/conceptos_transversales/index | conceptos_transversales]] — el modelo mental (Scene/Mobject/Animation) que las recetas dan por sabido
- [[Manim/index | Manim]] — el índice raíz con el `classDiagram` global de la librería
