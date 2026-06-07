---
title: Métodos Estáticos (staticmethod)
order: 3
tags:
  - python
  - teoria
  - metodos
draft: false
aliases:
  - Métodos Estáticos
  - staticmethod
---

# Métodos Estáticos (`@staticmethod`)

> [!definicion]
> Un **método estático** está marcado con el decorador **`@staticmethod`** y **no recibe `self` ni `cls`**. Es una **función ordinaria** alojada dentro de la clase por **cohesión** y para usar su *namespace*. No accede al estado: ni a la instancia ni a la clase.

```python
class Temperatura:
    def __init__(self, celsius):
        self.celsius = celsius

    @staticmethod
    def c_a_f(c):                    # ni self ni cls
        return c * 9 / 5 + 32

Temperatura.c_a_f(100)              # 212.0  -> se llama por la clase
t = Temperatura(20)
t.c_a_f(20)                        # 68.0   -> también desde la instancia
```

Funciona como cualquier función: solo opera con sus argumentos explícitos. Vive en la clase únicamente para indicar que **pertenece conceptualmente** a ella.

## Sin acceso al estado

Al no recibir ni `self` ni `cls`, un método estático **no puede leer ni modificar** atributos de instancia o de clase. Si necesitara hacerlo, es señal de que debe ser otro tipo de método.

```python
class Validador:
    @staticmethod
    def es_email(s):                # utilidad de validación pura
        return "@" in s and "." in s.split("@")[-1]

Validador.es_email("a@b.com")      # True
Validador.es_email("invalido")     # False
```

> [!regla]
> Si el método usa `self` → es de [[01 Metodos de Instancia | instancia]]. Si usa `cls` → es de [[02 Metodos de Clase (classmethod) | clase]]. Si **no usa ninguno** → es estático.

## Estático vs. función de módulo

Técnicamente un método estático **podría** vivir como función suelta en el módulo. La elección es de **diseño/legibilidad**, no de capacidad.

| Preferir `@staticmethod` cuando... | Preferir función de módulo cuando... |
| --- | --- |
| La utilidad solo tiene sentido **junto a esa clase** | La utilidad es **genérica** y reutilizable fuera |
| Se quiere acceder vía `Clase.util(...)` (namespace) | No hay relación conceptual con ninguna clase |
| Puede **redefinirse** en una subclase | No participa de la jerarquía de clases |

> [!info]
> Agrupar la utilidad en la clase mejora el descubrimiento (`Temperatura.c_a_f`) y permite que una subclase la **sobrescriba**. Si nada de eso aporta, una función de módulo es más simple.

## Contraste con `classmethod`

Ambos se invocan por la clase, pero `@classmethod` **sí recibe `cls`** y por tanto ve el estado de clase y reacciona a la herencia; `@staticmethod` no.

```python
class Base:
    nombre = "Base"
    @classmethod
    def quien_cls(cls):    return cls.nombre     # depende de la clase real
    @staticmethod
    def quien_est():       return Base.nombre    # fijo, nombre cableado

class Sub(Base):
    nombre = "Sub"

Sub.quien_cls()   # 'Sub'   -> cls = Sub
Sub.quien_est()   # 'Base'  -> no hay cls; referencia fija a Base
```

Regla práctica: si el método necesitase referirse a **la propia clase** (para construir instancias o leer su estado), use `@classmethod`; si es una **función auxiliar autónoma**, use `@staticmethod`.
