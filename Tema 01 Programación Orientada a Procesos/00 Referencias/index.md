---
title: Referencias
order: 0
draft: false
tags:
  - Index
  - referencia
aliases:
  - Referencias del Tema
---
# Referencias

Material **transversal** al capítulo: tablas y reglas que se consultan desde cualquier otro módulo y que no pertenecen a un tema concreto. Son notas de **consulta rápida**, no de desarrollo conceptual.

## Notas de referencia

- [[Operadores de Variables | Operadores]] — catálogo completo de operadores (aritméticos, comparación, lógicos, asignación, identidad, pertenencia, bit a bit, ternario) con su precedencia y asociatividad.
- [[Valores Truthy y Falsy | Valores Truthy y Falsy]] — qué evalúa un objeto a `True` o `False` en un contexto booleano; base de toda condición en [[30 Estructuras de Control/index | estructuras de control]].

## Cuándo se consultan

| Desde | Se consulta | Para |
| ----- | ----------- | ---- |
| [[11 Datos Primitivos/index \| Tipos primitivos]] | Operadores | Operaciones soportadas por cada tipo |
| [[31 Condicionales/index \| Condicionales]] | Valores Truthy y Falsy | Evaluar la condición de un `if` |
| [[32 Bucles/index \| Bucles]] | Valores Truthy y Falsy | Condición de parada de un `while` |
| Cualquier expresión | Operadores · Precedencia | Resolver el orden de evaluación |
