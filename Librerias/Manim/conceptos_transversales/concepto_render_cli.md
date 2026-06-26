---
title: el render y el CLI (manim ...) — de construct() al vídeo
aliases:
  - render
  - CLI
  - manim cli
  - render cli
tags:
  - manim
  - concepto
order: 8
lib: manim
tipo: concepto
requiere:
  - concepto_scene_construct
draft: false
---

# el render y el CLI (manim ...) — de construct() al vídeo

Escribir la `Scene` es solo la mitad del trabajo: el guion de `construct()` no se ejecuta solo. Para convertirlo en un vídeo se invoca el **comando `manim`** desde la terminal, apuntándolo al archivo `.py` y a la escena concreta que quieres renderizar. Ese comando es la herramienta que usas a diario —cada vez que cambias una línea y quieres ver el resultado—, así que dominar sus flags principales es lo que separa iterar rápido de esperar minutos por cada prueba. Esta nota explica qué pasa por dentro cuando ejecutas `manim`, cuál es el comando base, y cómo el objeto `config` te deja ajustar el render tanto desde la línea de comandos como desde el propio código.

## Por qué existe un comando aparte

En Manim no ejecutas tu archivo con `python archivo.py`: ese guion solo *define* una clase `Scene`, no la renderiza. El motor de Manim necesita **instanciar** tu escena, ejecutar su `construct()` en modo "grabación", convertir las animaciones en fotogramas y unirlos en un vídeo. Toda esa maquinaria vive detrás del comando `manim`, que actúa como punto de entrada: le dices *qué archivo* y *qué escena*, y él se encarga del resto. Por eso una animación de Manim siempre se lanza igual —`manim <flags> archivo.py NombreEscena`— sin importar lo que contenga el `construct` (descrito en [[concepto_scene_construct]]).

## El comando base

La forma que usarás el 90 % del tiempo durante el desarrollo es esta:

```bash
manim -pql archivo.py NombreEscena
```

Se lee de izquierda a derecha: el ejecutable `manim`, un grupo de flags (`-pql` son tres flags juntos: `-p`, `-q`, `l`), el archivo Python donde está la escena, y por último el **nombre exacto de la clase** `Scene` que quieres renderizar (sensible a mayúsculas). Si omites el nombre de la escena y el archivo tiene varias, Manim te pregunta cuál; si tiene una sola, la usa directamente.

### Los flags del día a día

Estos son los que se combinan constantemente. Casi todos tienen forma corta (`-p`) y, muchos, una larga equivalente (`--preview`):

| Flag | Qué hace |
|------|----------|
| `-p` | **preview**: abre y reproduce el vídeo automáticamente al terminar el render |
| `-q` | fija la **calidad** (lleva detrás una letra: `l`, `m`, `h`, `k`) |
| `-s` | **save_last_frame**: no genera vídeo, guarda solo el ÚLTIMO fotograma como `.png` |
| `-a` | **all**: renderiza TODAS las escenas del archivo, no solo una |
| `--format gif` | exporta el resultado como `.gif` animado en vez de `.mp4` |
| `-o NOMBRE` | **output_file**: fija el nombre del archivo de salida |

### El flag de calidad en detalle

La letra que acompaña a `-q` decide la resolución y los FPS, y por tanto el tiempo de render. Es el flag con más impacto en tu velocidad de iteración:

| Flag | Letra | Resolución | FPS | Cuándo |
|------|-------|------------|-----|--------|
| `-ql` | `l` (low) | 480p | 15 | desarrollo: lo más rápido, para iterar |
| `-qm` | `m` (medium) | 720p | 30 | revisión intermedia |
| `-qh` | `h` (high) | 1080p | 60 | render final de entrega |
| `-qk` | `k` (4K) | 2160p | 60 | máxima calidad, muy lento |

La regla práctica: **desarrolla en `-ql` y exporta el final en `-qh`**. A baja calidad cada render tarda segundos; a 4K puede tardar minutos por la cantidad de píxeles y fotogramas que hay que calcular. Cambiar la calidad no cambia tu código: la misma `Scene` se renderiza a cualquier resolución.

## El flujo por dentro: de construct() a .mp4

Cuando pulsas Enter, Manim recorre estos pasos en orden. Entenderlos te dice *por qué* tarda lo que tarda y *dónde* aparece el archivo:

1. **Importa y localiza**: carga `archivo.py`, busca la clase `NombreEscena` y comprueba que hereda de `Scene`.
2. **Instancia la Scene**: crea el objeto (`NombreEscena()`), lo que prepara la cámara y el lienzo según la calidad pedida.
3. **Ejecuta `construct()` una vez**: recorre tu guion de arriba abajo grabando cada `self.play(...)` y `self.wait(...)` como una porción de tiempo con sus animaciones.
4. **Renderiza a fotogramas**: por cada animación, calcula los fotogramas intermedios. El número de fotogramas sale de `run_time × FPS` (una animación de 2 s a 15 FPS son 30 imágenes; a 60 FPS, 120). Aquí está el grueso del coste.
5. **Une con ffmpeg**: pasa la secuencia de fotogramas a `ffmpeg`, que los codifica en un único `.mp4` (o `.gif` con `--format gif`).
6. **Guarda y (opcional) reproduce**: deja el archivo en `media/videos/<archivo>/<calidad>/NombreEscena.mp4` y, si pusiste `-p`, lo abre en el reproductor.

Ese paso 4 es la razón de que la calidad importe tanto: subir de 480p15 a 1080p60 multiplica por 16 los píxeles y por 4 los fotogramas. El paso 6 explica la ruta donde "desaparece" tu vídeo: Manim organiza la salida en `media/` por archivo y por calidad, de modo que los renders a distinta calidad no se pisan.

### Dónde acaban los archivos

| Salida | Ruta típica |
|--------|-------------|
| Vídeo | `media/videos/<archivo>/<calidad>/NombreEscena.mp4` |
| Imagen (`-s`) | `media/images/<archivo>/NombreEscena.png` |
| Fotogramas parciales | `media/videos/<archivo>/<calidad>/partial_movie_files/` |

## El objeto `config`: ajustes globales

Más allá de los flags, Manim expone un objeto global `config` que centraliza **todos** los ajustes del render: resolución, FPS, color de fondo, nombre de salida, directorios... Cada flag de la línea de comandos no es más que un atajo que escribe en `config`. Lo interesante es que puedes tocar `config` **desde el propio código**, lo que fija un ajuste de forma permanente para esa escena sin tener que recordar pasar el flag cada vez. Para los detalles completos del objeto, ver [[config]]; para la lista exhaustiva de flags, ver [[cli]].

### Atributos más usados de config

| Atributo | Controla | Equivalente en CLI |
|----------|----------|--------------------|
| `config.background_color` | color de fondo del lienzo | (no hay flag directo) |
| `config.frame_rate` | FPS de salida | parte de `-q` |
| `config.pixel_height` / `config.pixel_width` | resolución en píxeles | `-r 1920,1080` |
| `config.output_file` | nombre del archivo de salida | `-o` |
| `config.quality` | calidad por nombre (`"low_quality"`...) | `-q` |

### Ejemplo: fondo blanco desde el código

Fijar `config.background_color` antes de la clase hace que todas las escenas del archivo se rendericen sobre blanco, sin tener que pasarlo por línea de comandos:

```python
from manim import *

config.background_color = WHITE   # ajuste global: afecta a todo el render

class FondoBlanco(Scene):
    def construct(self):
        c = Circle(color=BLUE)
        self.play(Create(c))
        self.wait()
```

```bash
manim -pql archivo.py FondoBlanco   # el fondo ya sale blanco, sin flags extra
```

La regla mental: lo que cambia **poco** (calidad, preview) va como flag al lanzar; lo que es **propio de la escena** (fondo, FPS especiales) va en `config` dentro del código para que quede fijo.

## Atajos para iterar rápido

El ciclo de trabajo eficiente se apoya en dos ideas:

- **Baja calidad mientras desarrollas** (`-ql`): renderiza en segundos, así pruebas cambios sin esperar. Reserva `-qh` para cuando la animación ya está lista y vas a exportar.
- **`-s` para componer sin animar**: si solo estás ajustando *posiciones, colores o tamaños* (la composición del fotograma final) y no te importa todavía el movimiento, `-s` guarda únicamente el último fotograma como PNG y se salta todo el render del vídeo. Es la forma más rápida de iterar sobre cómo *queda* la escena antes de preocuparte por cómo se *anima*.

## Ejemplos de comandos

Los comandos que cubren casi todos los casos, comentados:

```bash
# Desarrollo: rapido, baja calidad, se reproduce al terminar
manim -pql archivo.py MiEscena

# Render final: alta calidad (1080p60) para entregar
manim -qh archivo.py MiEscena

# Solo el ultimo fotograma como PNG (iterar la composicion, sin video)
manim -s archivo.py MiEscena

# Exportar como GIF en baja calidad (para incrustar en web/chat)
manim -pql --format gif archivo.py MiEscena

# Renderizar TODAS las escenas del archivo de una vez
manim -pqh -a archivo.py

# Nombre de salida personalizado
manim -qh -o intro_final archivo.py MiEscena
```

## Casos que fallan

| Error | Causa | Solución |
|-------|-------|----------|
| `No scenes inside that module` | el archivo no tiene ninguna clase que herede de `Scene` | revisa el `class X(Scene):` y el import |
| `There are no scenes named ...` | el nombre tras el archivo no coincide con la clase (mayúsculas) | copia el nombre exacto de la clase |
| El vídeo no se reproduce solo | olvidaste el flag `-p` | añade `-p` (o abre el `.mp4` a mano en `media/`) |
| Render lento eternamente | estás en `-qh`/`-qk` mientras desarrollas | baja a `-ql` hasta el render final |
| `ffmpeg not found` | falta ffmpeg en el sistema | instálalo (Manim lo usa para unir fotogramas) |
| El GIF no sale | olvidaste `--format gif` | añádelo; sin él la salida es `.mp4` |

## Relación con otros conceptos

- [[concepto_scene_construct]] — la `Scene` y el `construct()` que este comando renderiza.
- [[config]] — el objeto global con todos los ajustes del render.
- [[cli]] — la referencia completa de flags del comando `manim`.
