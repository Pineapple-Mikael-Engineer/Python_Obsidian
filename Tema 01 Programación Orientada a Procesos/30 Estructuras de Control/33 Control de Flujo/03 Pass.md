---
title: 03 Pass
draft: false
tags: [python, teoria, control-de-flujo]
---

# Pass

`pass` es una operación nula: no hace nada cuando se ejecuta. Se usa como *placeholder* cuando Python exige sintácticamente una declaración pero no se quiere ejecutar ningún código. A diferencia de [[01 Break | break]] y [[02 Continue | continue]], no altera el flujo del bucle; solo rellena un bloque vacío para que el código compile.

## Sintaxis y Comportamiento
```python
# pass no hace nada, solo mantiene la sintaxis
if condición:
    pass  # TODO: implementar más tarde

class MiClase:
    pass  # Clase vacía por ahora

def funcion_sin_implementar():
    pass  # Por implementar
```

## Diferencias Clave

| Característica   | `pass`                  | Comentario (`#`)         |
| ---------------- | ----------------------- | ------------------------ |
| **Propósito**    | Placeholder sintáctico  | Comentario/documentación |
| **Sintaxis**     | Parte del código Python | No es código ejecutable  |
| **En bucles**    | Permite bucle vacío     | No permite bucle vacío   |
| **En funciones** | Permite función vacía   | No permite función vacía |

## Ejemplos Prácticos

### Desarrollo Incremental
```python
# Ejemplo 1: Esqueleto de funciones por implementar
def procesar_datos(datos):
    """Función para procesar datos (en desarrollo)"""
    pass  # TODO: implementar lógica de procesamiento

def generar_reporte():
    """Genera reporte (pendiente)"""
    pass  # Por implementar en la siguiente iteración

# Mientras tanto, el código puede ejecutar sin errores
print("Sistema en desarrollo...")
```

### Estructuras Temporales en Clases
```python
# Ejemplo 2: Clase base abstracta (simplificada)
class FiguraGeometrica:
    """Clase base para figuras geométricas"""
    
    def area(self):
        """Calcula el área (debe implementarse en subclases)"""
        pass
    
    def perimetro(self):
        """Calcula el perímetro (debe implementarse en subclases)"""
        pass

class Cuadrado(FiguraGeometrica):
    def __init__(self, lado):
        self.lado = lado
    
    def area(self):
        return self.lado ** 2
    
    def perimetro(self):
        return 4 * self.lado

# Cuadrado implementa los métodos, FiguraGeometrica usa pass
```

### Bucles con Lógica Pendiente
```python
# Ejemplo 3: Bucle con estructura definida
configuraciones = ["modo1", "modo2", "modo3"]

for modo in configuraciones:
    # Estructura definida, lógica pendiente
    if modo == "modo1":
        pass  # TODO: implementar configuración modo1
    elif modo == "modo2":
        pass  # TODO: implementar configuración modo2
    else:
        print(f"Modo desconocido: {modo}")

# Esto compila y ejecuta sin errores mientras se desarrolla
```

## Patrón: Esqueleto de Sistema
```python
# Esqueleto de sistema con funciones por implementar
def inicializar_sistema():
    pass  # TODO: agregar inicialización

def procesar_entrada(entrada):
    # Estructura con múltiples casos
    if entrada.startswith("comando_"):
        pass  # Por implementar
    elif entrada == "ayuda":
        pass  # Por implementar
    else:
        print(f"Entrada no reconocida: {entrada}")

def cerrar_sistema():
    pass  # Por implementar

# El sistema puede ejecutarse mientras se desarrolla
```

> [!warning] Consideraciones
> - `pass` es para sintaxis, no para lógica: no lo confundas con un comentario.
> - Úsalo solo como placeholder temporal durante el desarrollo; reemplázalo por la implementación real antes de producción.
