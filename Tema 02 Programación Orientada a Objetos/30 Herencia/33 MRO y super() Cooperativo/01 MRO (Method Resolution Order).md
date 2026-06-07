---
title: MRO (Method Resolution Order)
order: 1
tags:
  - python
  - teoria
  - herencia
draft: false
aliases:
  - Method Resolution Order
  - Linearización C3
  - C3
---

# MRO (Method Resolution Order)

> [!definicion]
> El **MRO** (*Method Resolution Order*) es la secuencia **lineal** en la que Python busca un atributo o método a través de las clases base de una clase. Al resolver `obj.x`, recorre las clases **en orden de MRO** y se queda con la **primera** que define `x`. Lo calcula el algoritmo de **linearización C3** y se consulta con `Clase.__mro__` (tupla) o `Clase.mro()` (lista).

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

D.__mro__         # (<class D>, <class B>, <class C>, <class A>, <class object>)
D.mro()           # misma secuencia como lista
```

Toda clase tiene MRO, no solo las de herencia múltiple. En una cadena simple es trivial (`C → B → A → object`); el MRO importa de verdad cuando hay **varios padres** y el orden deja de ser obvio.

## El algoritmo C3 y sus propiedades

C3 produce una **única** linealización que respeta tres garantías simultáneas:

- **Orden local:** una clase aparece **antes** que sus padres.
- **Precedencia de padres:** si `D(B, C)`, en el MRO `B` precede a `C` (se respeta el orden en que se declaran las bases).
- **Monotonía:** el orden relativo entre dos clases en el MRO de una subclase no contradice el de ninguna de sus bases. Lo que es válido para `B` y para `C` sigue siéndolo para `D`.

La consecuencia práctica es que el padre común (`A`) se coloca **una sola vez y al final**, después de todas las clases que heredan de él. Nunca se visita una clase antes que alguna de sus subclases.

## El problema del diamante, resuelto

> [!ejemplo]
> Diamante clásico: `A` en la cima, `B` y `C` heredan de `A`, y `D` hereda de `B` y `C`. Sin un orden definido, sería ambiguo si `D` ve la versión de `B` o la de `C`. El MRO lo resuelve de forma determinista.

```python
class A:
    def quien(self): return "A"
class B(A):
    def quien(self): return "B"
class C(A):
    def quien(self): return "C"
class D(B, C):
    pass

D().quien()       # "B"  -> primera coincidencia en el MRO (D, B, C, A)
[k.__name__ for k in D.__mro__]   # ['D', 'B', 'C', 'A', 'object']
```

`A` aparece **una sola vez** y al final, pese a estar como base de `B` y de `C`: C3 evita duplicarla y la pospone hasta después de `B` y `C`.

## Cuándo C3 falla

> [!info]
> Si las restricciones de orden son **incompatibles** entre sí, C3 no puede producir una linealización y Python lanza `TypeError` **al definir la clase**, no al usarla. El caso típico es invertir el orden de las bases respecto a otra subclase, generando una jerarquía inconsistente.

```python
class A: pass
class B(A): pass
# B exige A después de B; aquí se pide A antes de B -> contradicción
class X(A, B): pass
# TypeError: Cannot create a consistent method resolution
#            order (MRO) for bases A, B
```

El error es una **garantía**, no un estorbo: detecta en tiempo de definición jerarquías cuyo orden de búsqueda sería ambiguo. El MRO así calculado es justamente la secuencia que recorre [[02 super() Cooperativo | super()]].
</content>
