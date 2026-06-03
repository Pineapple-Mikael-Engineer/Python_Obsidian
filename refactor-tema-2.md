---
title: refactor tema 2
draft: true
---


Estructura completa para **Tema 02 Programación Orientada a Objetos** con ramificación profunda por concepto. Mezcla del enriquecido (herramientas modernas) con el Capítulo 2 de `Conocimiento-Listado.md` (herencia multinivel, extensión de métodos, relaciones completas, patrones de diseño). Continuación de Tema 01, mismo estándar `redactar-nota`.

```
Tema 02 Programación Orientada a Objetos/
│
├── index.md
│   # Visión general de la POO en Python
│   # Los 4 pilares: abstracción, encapsulamiento, herencia, polimorfismo
│   # Clase vs objeto/instancia; objeto = estado + comportamiento
│   # Mapa de navegación de todo el tema
│
├── 00 Referencias/
│   ├── index.md
│   ├── Catalogo de Metodos Dunder.md     # tabla transversal de métodos especiales por categoría
│   └── Glosario POO.md                    # clase, instancia, atributo, método, self, MRO... (consulta rápida)
│
├── 10 Clases y Objetos/
│   ├── index.md
│   ├── 11 Definicion de Clases/
│   │   ├── index.md
│   │   ├── 01 Sentencia class.md
│   │   ├── 02 Instanciacion.md
│   │   ├── 03 El parametro self.md
│   │   └── 04 Constructor __init__.md
│   ├── 12 Atributos/
│   │   ├── index.md
│   │   ├── 01 Atributos de Instancia.md
│   │   ├── 02 Atributos de Clase.md
│   │   └── 03 Atributos Dinamicos y __dict__.md
│   └── 13 Metodos/
│       ├── index.md
│       ├── 01 Metodos de Instancia.md
│       ├── 02 Metodos de Clase (classmethod).md
│       └── 03 Metodos Estaticos (staticmethod).md
│
├── 20 Encapsulamiento/
│   ├── index.md
│   ├── 21 Visibilidad/
│   │   ├── index.md
│   │   ├── 01 Atributos Publicos.md
│   │   ├── 02 Atributos Protegidos (_).md
│   │   └── 03 Privados y Name Mangling (__).md
│   └── 22 Properties/
│       ├── index.md
│       ├── 01 property y getters-setters.md
│       ├── 02 Propiedades Solo-Lectura.md
│       └── 03 Propiedades Calculadas.md
│
├── 30 Herencia/
│   ├── index.md
│   ├── 31 Tipos de Herencia/
│   │   ├── index.md
│   │   ├── 01 Herencia Simple.md
│   │   ├── 02 Herencia Multinivel.md
│   │   └── 03 Herencia Multiple.md
│   ├── 32 Mecanismos de Herencia/
│   │   ├── index.md
│   │   ├── 01 super() y Constructor del Padre.md
│   │   ├── 02 Sobrescritura de Metodos (override).md
│   │   └── 03 Extension de Metodos.md
│   └── 33 MRO y super() Cooperativo/
│       ├── index.md
│       ├── 01 MRO (Method Resolution Order).md
│       └── 02 super() Cooperativo.md
│
├── 40 Polimorfismo/
│   ├── index.md
│   ├── 01 Duck Typing.md
│   ├── 02 Polimorfismo de Subtipos.md
│   └── 03 Sobrecarga de Operadores.md     # enlaza a 52
│
├── 50 Metodos Especiales (Dunder)/
│   ├── index.md
│   ├── 51 Representacion/
│   │   ├── index.md
│   │   ├── 01 __str__ y __repr__.md
│   │   └── 02 __format__.md
│   ├── 52 Sobrecarga de Operadores/
│   │   ├── index.md
│   │   ├── 01 Operadores Aritmeticos.md
│   │   └── 02 Operadores de Comparacion.md
│   └── 53 Comportamiento de Objeto/
│       ├── index.md
│       ├── 01 Contenedores (__len__, __getitem__).md
│       ├── 02 Invocable (__call__).md
│       └── 03 Context Managers (__enter__, __exit__).md
│
├── 60 Abstraccion/
│   ├── index.md
│   ├── 01 Clases Abstractas (ABC).md
│   ├── 02 abstractmethod.md
│   └── 03 Interfaces Informales vs Formales.md
│
├── 70 Relaciones entre Objetos/
│   ├── index.md
│   ├── 01 Composicion.md          # "tiene un" (fuerte, ciclo de vida ligado)
│   ├── 02 Agregacion.md           # "tiene un" (débil, independiente)
│   ├── 03 Asociacion.md           # "usa un"
│   ├── 04 Dependencia.md          # "depende de"
│   ├── 05 Mixins.md
│   └── 06 Composicion vs Herencia.md
│
├── 80 Patrones de Diseño/
│   ├── index.md
│   ├── 01 Singleton.md
│   ├── 02 Factory Method.md
│   ├── 03 Strategy.md
│   └── 04 Observer.md
│
└── 90 Herramientas Modernas/
    ├── index.md
    ├── 01 Dataclasses.md          # @dataclass, field, frozen
    ├── 02 __slots__.md            # memoria y atributos fijos
    ├── 03 __new__ vs __init__.md  # creación vs inicialización
    └── 04 Enumeraciones (Enum).md
```

Total ≈ 75 notas (índices + hojas), profundidad y densidad equivalentes a Tema 01.
