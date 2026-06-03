---
title: refactor tema 1
draft: true
---


Aquí tienes la estructura completa para **Tema 01 Programación Orientada a Procesos** con ramificación profunda:

```
Tema 01 Programación Orientada a Procesos/
│
├── index.md
│   # Visión general de la programación orientada a procesos en Python
│   # Flujo secuencial, características, filosofía
│   # Mapa de navegación de todo el tema
│
├── 10 Variables y Tipos de Datos/
│   ├── index.md
│   │   # Concepto de variable en Python
│   │   # Tipado dinámico y fuerte
│   │   # Asignación y referencia
│   │   # Sistema de tipos en Python
│   │
│   ├── 11 Datos Primitivos/
│   │   ├── index.md
│   │   │   # Visión general de tipos básicos o fundamentales
│   │   │   # Inmutabilidad de los primitivos
│   │   │   # Representación en memoria
│   │   │
│   │   ├── 01 Numeros.md
│   │   │   # int: enteros sin límite
│   │   │   # float: punto flotante, precisión
│   │   │   # complex: números complejos
│   │   │   # Operaciones matemáticas básicas
│   │   │
│   │   ├── 02 Booleanos.md
│   │   │   # True y False
│   │   │   # Operadores lógicos: and, or, not
│   │   │   # Evaluación en cortocircuito
│   │   │
│   │   └── 03 NoneType.md
│   │       # El valor None
│   │       # Ausencia de valor
│   │       # Usos comunes: retorno de funciones, valores opcionales
│   │
│   ├── 12 Mutabilidad/
│   │   ├── index.md
│   │   │   # Concepto de mutabilidad vs inmutabilidad
│   │   │   # Identidad vs valor
│   │   │   # Implicaciones en rendimiento y comportamiento
│   │   │
│   │   ├── 01 Objetos Inmutables.md
│   │   │   # int, float, complex
│   │   │   # str, tuple
│   │   │   # frozenset
│   │   │   # Comportamiento: cada cambio crea nuevo objeto
│   │   │
│   │   └── 02 Objetos Mutables.md
│   │       # list, dict, set
│   │       # bytearray, array
│   │       # Objetos personalizados
│   │       # Modificación in-place
│   │
│   └── 13 Transformación de Tipos/
│       ├── index.md
│       │   # Conversión entre tipos de datos
│       │   # Coerción vs casting
│       │   # Pérdida de información
│       │
│       ├── 01 Conversion Implicita.md
│       │   # Coerción automática en operaciones
│       │   # Promoción de tipos: int → float
│       │   # Reglas de conversión implícita
│       │
│       └── 02 Conversion Explicita.md
│           # Funciones de conversión: int(), float(), str()
│           # Conversiones seguras
│           # Manejo de errores en conversiones
│
├── 20 Estructura de Datos/
│   ├── index.md
│   │   # Colecciones en Python
│   │   # Clasificación: secuencias, mapas, conjuntos
│   │   # Características comunes: iterables, contenedores
│   │   # Módulos: collections, array, heapq
│   │
│   ├── 21 Secuencias/
│   │   ├── index.md
│   │   │   # Características de las secuencias
│   │   │   # Indexación y slicing
│   │   │   # Operaciones comunes: len(), in, concatenación
│   │   │   # Secuencias mutables vs inmutables
│   │   │
│   │   ├── 01 Cadenas.md
│   │   │   # str: secuencia inmutable de caracteres
│   │   │   # Métodos principales: split(), join(), replace()
│   │   │   # Formato: f-strings, format(), %
│   │   │   # Slicing avanzado
│   │   │   # Codificación: encode(), decode()
│   │   │
│   │   ├── 02 Listas.md
│   │   │   # list: secuencia mutable
│   │   │   # Métodos: append(), extend(), insert(), remove()
│   │   │   # Slicing con asignación
│   │   │   # List comprehensions
│   │   │   # Uso como pila y cola
│   │   │
│   │   └── 03 Tuplas.md
│   │       # tuple: secuencia inmutable
│   │       # Empaquetado y desempaquetado
│   │       # Tuplas vs listas: cuándo usar cada una
│   │       # Tuplas con nombre: namedtuple
│   │
│   ├── 22 Mapas/
│   │   ├── index.md
│   │   │   # Estructuras clave-valor
│   │   │   # Hash tables
│   │   │   # Requisitos de las claves: hashables
│   │   │
│   │   └── 01 Diccionarios.md
│   │       # dict: tabla hash mutable
│   │       # Métodos: keys(), values(), items(), get()
│   │       # Dict comprehensions
│   │       # defaultdict, Counter, OrderedDict
│   │       # Merge de diccionarios (| operador)
│   │
│   └── 23 Conjuntos/
│       ├── index.md
│       │   # Teoría de conjuntos en Python
│       │   # Elementos únicos y hashables
│       │   # Operaciones de conjuntos
│       │
│       └── 01 Sets.md
│           # set: mutable, desordenado
│           # frozenset: inmutable
│           # Operaciones: unión, intersección, diferencia
│           # Set comprehensions
│           # Pruebas de pertenencia eficientes
│
├── 30 Estructuras de Control/
│   ├── index.md
│   │   # Control del flujo de ejecución
│   │   # Bloques de código e indentación
│   │   # Sentencias vs expresiones
│   │
│   ├── 31 Condicionales/
│   │   ├── index.md
│   │   │   # Toma de decisiones en el código
│   │   │   # Evaluación de condiciones
│   │   │   # Valores truthy y falsy
│   │   │
│   │   ├── 01 If-Elif-Else.md
│   │   │   # Sintaxis básica: if, elif, else
│   │   │   # Anidamiento de condicionales
│   │   │   # Buenas prácticas
│   │   │
│   │   ├── 02 Operador Ternario.md
│   │   │   # Expresiones condicionales
│   │   │   # Sintaxis: x if condicion else y
│   │   │   # Usos y limitaciones
│   │   │
│   │   └── 03 Match Case.md
│   │       # Pattern matching (Python 3.10+)
│   │       # Sintaxis match/case
│   │       # Patrones literales, de captura, OR
│   │       # Guards
│   │
│   ├── 32 Bucles/
│   │   ├── index.md
│   │   │   # Iteración en Python
│   │   │   # Bucles definidos e indefinidos
│   │   │   # Iterables e iteradores
│   │   │
│   │   ├── 01 While.md
│   │   │   # Bucle condicional
│   │   │   # Sintaxis: while condicion:
│   │   │   # Bucles infinitos y cómo evitarlos
│   │   │   # Uso con else
│   │   │
│   │   └── 02 For.md
│   │       # Bucle sobre secuencias
│   │       # Sintaxis: for elemento in iterable:
│   │       # range(), enumerate(), zip()
│   │       # Iteración sobre diccionarios
│   │       # For-else
│   │
│   └── 33 Control de Flujo/
│       ├── index.md
│       │   # Modificadores de bucles
│       │   # Interrupción y control fino
│       │
│       ├── 01 Break.md
│       │   # Salir del bucle prematuramente
│       │   # Uso en bucles anidados
│       │   # Ejemplos prácticos
│       │
│       ├── 02 Continue.md
│       │   # Saltar a la siguiente iteración
│       │   # Filtrar elementos
│       │   # Diferencias con break
│       │
│       └── 03 Pass.md
│           # Sentencia nula
│           # Placeholder para código futuro
│           # En clases y funciones vacías
│
├── 40 Funciones/
│   ├── index.md
│   │   # Concepto de función en Python
│   │   # Abstracción y reutilización
│   │   # Funciones como objetos de primera clase
│   │   # Documentación con docstrings
│   │
│   ├── 41 Definicion y Llamada/
│   │   ├── index.md
│   │   │   # Estructura básica de una función
│   │   │   # Sintaxis def
│   │   │   # Nomenclatura y convenciones
│   │   │
│   │   ├── 01 Sintaxis Basica.md
│   │   │   # Definición con def
│   │   │   # Parámetros y argumentos
│   │   │   # La indentación como bloque
│   │   │
│   │   ├── 02 Parametros y Argumentos.md
│   │   │   # Paso por asignación
│   │   │   # Mutabilidad y efectos secundarios
│   │   │   # Copia vs referencia
│   │   │
│   │   └── 03 Valor de Retorno.md
│   │       # return y su funcionamiento
│   │       # Múltiples valores (tuplas implícitas)
│   │       # None como retorno implícito
│   │
│   ├── 42 Clasificacion de Funciones/
│   │   ├── index.md
│   │   │   # Taxonomía de funciones en Python
│   │   │   # Según origen, estructura, comportamiento
│   │   │
│   │   ├── 01 Funciones Built-in.md
│   │   │   # Funciones incorporadas: print(), len(), type()
│   │   │   # Funciones matemáticas: abs(), round(), sum()
│   │   │   # Funciones de conversión: int(), str(), list()
│   │   │
│   │   ├── 02 Funciones de Usuario.md
│   │   │   # Definición propia
│   │   │   # Reutilización y modularización
│   │   │   # Encapsulación de lógica
│   │   │
│   │   ├── 03 Funciones Lambda.md
│   │   │   # Funciones anónimas
│   │   │   # Sintaxis: lambda args: expresion
│   │   │   # Usos con map(), filter(), sorted()
│   │   │   # Limitaciones
│   │   │
│   │   └── 04 Funciones Recursivas.md
│   │       # Auto-llamada de funciones
│   │       # Casos base y casos recursivos
│   │       # Profundidad de recursión y límites
│   │       # Ejemplos: factorial, Fibonacci
│   │
│   ├── 43 Ambito y Espacios de Nombres/
│   │   ├── index.md
│   │   │   # Concepto de scope (ámbito)
│   │   │   # Namespaces en Python
│   │   │   # Tiempo de vida de las variables
│   │   │
│   │   ├── 01 Variables Locales.md
│   │   │   # Variables definidas dentro de funciones
│   │   │   # Alcance limitado
│   │   │   # Ocultamiento de variables globales
│   │   │
│   │   ├── 02 Variables Globales.md
│   │   │   # Variables a nivel de módulo
│   │   │   # Acceso desde funciones
│   │   │   # La palabra clave global
│   │   │   # Problemas de las globales
│   │   │
│   │   ├── 03 Regla LEGB.md
│   │   │   # Orden de búsqueda: Local, Enclosing, Global, Built-in
│   │   │   # Ejemplos de cada nivel
│   │   │   # Resolución de nombres
│   │   │
│   │   └── 04 Nonlocal.md
│   │       # Ámbito en funciones anidadas
│   │       # La palabra clave nonlocal
│   │       # Closures
│   │
│   └── 44 Patrones de Argumentos/
│       ├── index.md
│       │   # Flexibilidad en la llamada a funciones
│       │   # Parámetros posicionales y nominales
│       │   # Combinaciones
│       │
│       ├── 01 Args y Kwargs.md
│       │   # *args: número variable de argumentos posicionales
│       │   # **kwargs: número variable de argumentos nominales
│       │   # Desempaquetado en llamadas
│       │   # Convenciones de nombres
│       │
│       ├── 02 Argumentos por Defecto.md
│       │   # Valores por omisión en parámetros
│       │   # Evaluación en tiempo de definición
│       │   # Peligro de mutables como default
│       │   # Buenas prácticas
│       │
│       └── 03 Posicionales vs Nominales.md
│           # Parámetros solo-posicionales (/)
│           # Parámetros solo-nominales (*)
│           # Combinaciones y orden
│           # Claridad en APIs
│
└── 50 Manejo de Excepciones/
    ├── index.md
    │   # Filosofía de manejo de errores en Python
    │   # EAFP vs LBYL
    │   # Excepciones vs errores
    │   # Jerarquía de excepciones
    │
    ├── 51 Excepciones Built-in/
    │   ├── index.md
    │   │   # Sistema de excepciones de Python
    │   │   # Cuándo ocurren
    │   │   # Cómo interpretarlas
    │   │
    │   ├── 01 Jerarquia de Excepciones.md
    │   │   # BaseException
    │   │   # Exception (para excepciones controlables)
    │   │   # Subclases principales
    │   │   # Excepciones del sistema: KeyboardInterrupt, SystemExit
    │   │
    │   ├── 02 Excepciones Comunes.md
    │   │   # TypeError, ValueError
    │   │   # IndexError, KeyError
    │   │   # AttributeError, NameError
    │   │   # ZeroDivisionError, FileNotFoundError
    │   │   # Ejemplos y causas
    │   │
    │   └── 03 Excepciones por Tipo.md
    │       # Errores de tipo (TypeError, ValueError)
    │       # Errores de índice/acceso (IndexError, KeyError)
    │       # Errores de atributo (AttributeError)
    │       # Errores de E/S (IOError, FileNotFoundError)
    │       # Errores de importación (ImportError, ModuleNotFoundError)
    │
    ├── 52 Try Except Finally/
    │   ├── index.md
    │   │   # Estructura de manejo de excepciones
    │   │   # Captura controlada de errores
    │   │   # Flujo con excepciones
    │   │
    │   ├── 01 Sintaxis Try Except.md
    │   │   # Bloque try
    │   │   # Bloques except específicos
    │   │   # Múltiples except
    │   │   # Except genérico (except Exception:)
    │   │
    │   ├── 02 Else y Finally.md
    │   │   # Bloque else: se ejecuta si no hay excepción
    │   │   # Bloque finally: se ejecuta siempre
    │   │   # Usos típicos: limpieza, recursos
    │   │   # Orden de ejecución
    │   │
    │   └── 03 Captura de Excepciones.md
    │       # Acceso a la instancia de la excepción (as e)
    │       # Capturar múltiples excepciones en un except
    │       # Inspeccionar el error
    │       # Tracebacks
    │
    └── 53 Raise de Excepciones/
        ├── index.md
        │   # Lanzar excepciones intencionalmente
        │   # Validación de entrada
        │   # Señalizar condiciones de error
        │
        ├── 01 Raise Simple.md
        │   # raise Exception("mensaje")
        │   # Lanzar excepciones built-in
        │   # Cuándo lanzar cada tipo
        │   # Re-lanzar excepciones
        │
        ├── 02 Excepciones Personalizadas.md
        │   # Crear clases de excepción propias
        │   # Heredar de Exception
        │   # Añadir atributos y métodos
        │   # Documentación de excepciones
        │
        └── 03 Re-raise y Encadenamiento.md
            # raise sin argumentos (re-lanzar)
            # raise ... from ... (encadenar excepciones)
            # raise ... from None (suprimir contexto)
            # Causas originales vs nuevas
```

Esta estructura proporciona:

1. **Jerarquía numérica clara** (10, 20, 30... y 11, 12, 13...)
2. **Índices en cada nivel** que resumen el contenido
3. **Archivos granulares** para conceptos específicos
4. **Relaciones visuales** entre temas relacionados
5. **Escalabilidad** para añadir más contenido en el futuro

¿Necesitas que te ayude con el contenido específico de algún archivo o con la migración?