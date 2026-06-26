---
title: cli — el comando manim (flags de render)
aliases:
  - cli
  - comando manim
  - flags manim
tags:
  - manim
  - referencia
  - config_cli
lib: manim
tipo: concepto
order: 2
draft: false
---

# cli — el comando `manim`

`manim` es la **herramienta de línea de comandos** que renderiza una `Scene`. No ejecutas tu archivo con `python archivo.py` (eso solo *define* la clase); en su lugar invocas `manim`, le indicas el archivo `.py` y el nombre de la escena, y él instancia la clase, ejecuta su `construct()`, calcula los fotogramas y los une en un vídeo. Esta nota es la referencia de sus **flags**; el flujo completo de qué ocurre por dentro está en [[concepto_render_cli]], y la otra cara (fijar lo mismo desde el código) en [[config]].

## Forma del comando

El comando siempre tiene la misma estructura: el ejecutable, los flags, el archivo y el nombre de la escena.

```bash
manim [flags] archivo.py NombreEscena
```

Tiene **tres partes** detrás del ejecutable:

- **`[flags]`** — las opciones que controlan el render (calidad, preview, formato...). Son opcionales y se pueden agrupar: `-pql` es `-p` + `-q` + `l` en un solo bloque. Van **antes** del archivo.
- **`archivo.py`** — la ruta al archivo Python que contiene la escena. El `.py` es obligatorio (es un argumento de fichero, no un módulo).
- **`NombreEscena`** — el **nombre exacto de la clase** `Scene` que quieres renderizar, sensible a mayúsculas. Si lo omites y el archivo tiene varias escenas, Manim te pregunta cuál; si tiene una sola, la usa directamente.

## Flags de calidad

La calidad decide resolución y FPS, y por tanto el tiempo de render. Es el flag con más impacto: desarrolla en baja, exporta en alta. Junto a ellos, los dos flags de comodidad más usados (`-p` y `-f`).

| Flag | Qué fija | Resolución / efecto |
|------|----------|---------------------|
| `-ql` | calidad **baja** (low) | 480p15 — lo más rápido, para iterar |
| `-qm` | calidad **media** (medium) | 720p30 — revisión intermedia |
| `-qh` | calidad **alta** (high) | 1080p60 — render final de entrega |
| `-qk` | calidad **4K** (k) | 2160p60 — máxima calidad, muy lento |
| `-p` | **preview** | abre y reproduce el vídeo al terminar |
| `-f` | **show in file browser** | abre la carpeta donde quedó el archivo |

## Flags utiles

Más allá de la calidad, estos son los flags que se combinan a diario para cambiar qué se genera y cómo.

| Flag | Qué hace |
|------|----------|
| `-a` | **all**: renderiza TODAS las escenas del archivo, no solo una |
| `-s` | **save_last_frame**: no genera vídeo, guarda solo el último fotograma como imagen |
| `--format gif` | exporta como `.gif` animado (también `png`, `mp4`, `webm`) |
| `-o NOMBRE` | **output_file**: fija el nombre del archivo de salida |
| `-r W,H` | **resolution**: fija la resolución a medida, p. ej. `-r 1920,1080` |
| `--fps N` | fija los fotogramas por segundo de salida |
| `-t` | **transparent**: fondo transparente (fuerza `.mov`/`.webm` con canal alfa) |
| `--disable_caching` | desactiva la caché de animaciones (re-renderiza todo desde cero) |
| `-v NIVEL` | **verbosity**: nivel de log (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `-n A,B` | renderiza solo el **rango** de animaciones de la A a la B (saltarse el principio) |

> [!tip] `-r` y `--fps` mandan sobre `-q`
> Si combinas un flag de calidad con `-r` o `--fps`, los valores explícitos **ganan**: `-ql -r 1920,1080` renderiza a 1080p pero con los FPS de `-ql`. Útil para una resolución a medida sin renunciar a la rapidez de la baja calidad.

## Combinaciones frecuentes

Los lanzamientos que cubren casi todos los casos, sobre una escena llamada `Demo`.

```bash
# Iterar: baja calidad + preview (el comando del dia a dia)
manim -pql archivo.py Demo
```

```bash
# Render final: alta calidad + preview
manim -pqh archivo.py Demo
```

```bash
# Solo el ultimo frame como imagen (ajustar la composicion, sin video)
manim -ps archivo.py Demo
```

```bash
# Exportar un GIF en baja calidad
manim -pql --format gif archivo.py Demo
```

## Donde queda el video

Manim no deja el archivo junto a tu `.py`: lo organiza dentro de `media/`, separado por archivo y por calidad, de modo que los renders a distinta calidad **no se pisan**.

```
media/videos/<archivo>/<calidad>/NombreEscena.mp4
```

Por ejemplo, `manim -qh archivo.py Demo` deja el vídeo en `media/videos/archivo/1080p60/Demo.mp4`. Con `-s`, la imagen va a `media/images/<archivo>/Demo.png`. Si no encuentras tu salida, mira ahí (o usa `-f` para que Manim te abra la carpeta).

## Errores comunes

Los fallos que más se repiten al lanzar el comando.

| Error | Causa | Solución |
|-------|-------|----------|
| `There are no scenes named ...` | el nombre tras el archivo no coincide con la clase (mayúsculas) | copia el nombre **exacto** de la clase `Scene` |
| `No scenes inside that module` | el archivo no tiene ninguna clase que herede de `Scene`, o falta el import | revisa `class X(Scene):` y `from manim import *` |
| Error de "fichero no encontrado" | olvidaste el `.py` o la ruta es incorrecta | pasa el archivo con su extensión y ruta correcta |
| Un flag "no hace nada" | lo pusiste **después** del nombre de la escena | los flags van **antes** del archivo: `manim -pql archivo.py Demo` |
| El GIF no sale (salió `.mp4`) | olvidaste `--format gif` | añádelo; sin él la salida por defecto es `.mp4` |

## Notas relacionadas

- [[concepto_render_cli]] — qué hace `manim` por dentro: de `construct()` al vídeo, paso a paso
- [[config]] — el objeto global donde cada flag de aquí escribe su valor
- [[config_cli/index | config_cli]] — la carpeta padre: las dos vías para controlar el render
- [[concepto_scene_construct]] — la `Scene` y el `construct()` que este comando renderiza
