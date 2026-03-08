# Cuándo usar lambda y cuándo no

Usa `lambda` cuando:
- la función es corta y de una sola expresión,
- se pasa como argumento (por ejemplo a `sorted`, `map`, `filter`).

Prefiere `def` cuando:
- hay lógica compleja,
- necesitas documentación y tests,
- quieres reutilizarla ampliamente.
