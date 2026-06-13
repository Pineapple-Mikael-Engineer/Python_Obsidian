---
title: modelo personalizado — subclasear QAbstractTableModel
aliases: [modelo personalizado, QAbstractTableModel, modelo de datos, model view]
tags: [pyqt6, patron, widgets]
lib: pyqt6
tipo: patron
requiere: [concepto_model_view, QTableView]
draft: false
---

# modelo personalizado — subclasear QAbstractTableModel

Cuando tienes **TUS** datos —una lista de objetos, las filas de una base de datos, un CSV en memoria— y quieres mostrarlos en una [[QTableView]] **sin copiarlos celda a celda** a un `QTableWidget`, subclaseas `QAbstractTableModel`. La idea del patron [[concepto_model_view|Modelo/Vista]] es que el modelo es un **ADAPTADOR** entre tus datos y la vista: la vista no conoce tus datos, solo le **pregunta** al modelo "cuantas filas hay", "cuantas columnas", "que pongo en esta celda". Tu escribes ese adaptador una vez y la vista se encarga del resto (pintar, hacer scroll, seleccionar, ordenar).

La ventaja sobre `QTableWidget`: no duplicas los datos (el modelo guarda una **referencia** a tu lista real), escala a miles de filas (la vista solo pide las celdas visibles) y un mismo modelo puede alimentar varias vistas a la vez. El coste: implementar unos pocos metodos. Esta nota los recorre de menos a mas, desde la receta minima de solo lectura hasta una tabla editable que inserta filas.

## Los metodos obligatorios

Un modelo de tabla **DEBE** implementar tres metodos. La vista los llama sola:

| Metodo | Firma | Devuelve | La vista pregunta... |
|--------|-------|----------|----------------------|
| `rowCount` | `rowCount(self, parent)` | `int` | cuantas filas tengo que pintar |
| `columnCount` | `columnCount(self, parent)` | `int` | cuantas columnas |
| `data` | `data(self, index, role)` | el valor | que pongo en esta celda, para este uso |

Dos parametros aparecen por todos lados y conviene entenderlos:

- **`index`** es un `QModelIndex`: identifica **una celda**. Te interesan `index.row()` (la fila) e `index.column()` (la columna). Con eso localizas el dato dentro de tu lista. Tambien tiene `index.isValid()`, que es `True` si apunta a una celda real (y `False` para el indice "raiz" que la vista usa de forma interna).
- **`role`** dice **para que** te pide la vista el dato de esa celda. La misma celda se consulta varias veces con roles distintos: uno para el texto, otro para el color de fondo, otro para la alineacion, otro para el tooltip... El rol estrella es `Qt.ItemDataRole.DisplayRole` = **el texto a mostrar**. Para cualquier rol que no manejes, devuelves `None` (asi la vista usa su valor por defecto).

> [!important] Regla de oro de `data`
> Para todo rol e indice que no manejes, **devuelve `None`**. Si te olvidas y devuelves algo (o caes por debajo del `if` sin `return`), veras celdas vacias, valores raros o errores intermitentes. `data` que no sabe que contestar contesta `None`.

## La receta minima

Un modelo de solo lectura que envuelve una **lista de listas** (cada sublista es una fila) y la muestra en una [[QTableView]]. Es ejecutable tal cual:

```python
from PyQt6.QtWidgets import QApplication, QTableView
from PyQt6.QtCore import QAbstractTableModel, Qt
import sys


class TablaModel(QAbstractTableModel):
    def __init__(self, datos):
        super().__init__()
        self._datos = datos                       # referencia a TUS datos (lista de listas)

    def rowCount(self, parent=None):
        return len(self._datos)                   # cuantas filas

    def columnCount(self, parent=None):
        return len(self._datos[0]) if self._datos else 0   # cuantas columnas

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:   # solo el rol "texto a mostrar"
            return str(self._datos[index.row()][index.column()])
        return None                               # cualquier otro rol: None


app = QApplication(sys.argv)

filas = [
    ["Ana",  "Madrid",    30],
    ["Luis", "Sevilla",   25],
    ["Marta","Barcelona", 41],
]
modelo = TablaModel(filas)

vista = QTableView()
vista.setModel(modelo)                            # conectar modelo <-> vista
vista.show()

sys.exit(app.exec())
```

Con tres metodos ya tienes una tabla funcional. La vista pinta solo, hace scroll y permite seleccionar; los datos siguen viviendo en `filas`, el modelo solo los expone.

## Construccion paso a paso

### 1. Guardar los datos

En el `__init__` llamas a `super().__init__()` (imprescindible: inicializa la maquinaria de `QObject`) y guardas una **referencia** a tus datos. No los copies ni los transformes: el modelo es un adaptador, no un almacen.

```python
def __init__(self, datos):
    super().__init__()
    self._datos = datos          # referencia, no copia
```

### 2. rowCount y columnCount

Devuelven cuantas filas y columnas tiene la tabla. Con una lista de listas, `rowCount` es `len(self._datos)` y `columnCount` es la longitud de una fila. El parametro `parent` existe por la firma comun de todos los modelos (lo usan los arboles); en una tabla lo ignoras.

```python
def rowCount(self, parent=None):
    return len(self._datos)

def columnCount(self, parent=None):
    return len(self._datos[0]) if self._datos else 0
```

### 3. data y los roles

`data` traduce **(celda, rol) -> valor**. El patron es un `if`/`elif` por rol, validando primero que el indice sea real, y un `return None` final para todo lo demas:

```python
def data(self, index, role=Qt.ItemDataRole.DisplayRole):
    if not index.isValid():
        return None
    fila, col = index.row(), index.column()
    valor = self._datos[fila][col]

    if role == Qt.ItemDataRole.DisplayRole:
        return str(valor)                                   # el texto

    if role == Qt.ItemDataRole.TextAlignmentRole:
        if isinstance(valor, (int, float)):                 # numeros a la derecha
            return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

    if role == Qt.ItemDataRole.ForegroundRole:
        if isinstance(valor, (int, float)) and valor < 0:   # negativos en rojo
            from PyQt6.QtGui import QColor
            return QColor("red")

    return None
```

Roles utiles ademas de `DisplayRole`:

| Rol | Para que | Que devuelves |
|-----|----------|---------------|
| `DisplayRole` | el texto de la celda | un `str` |
| `EditRole` | el valor al **empezar a editar** (a menudo igual que Display) | el valor "crudo" |
| `TextAlignmentRole` | alineacion del texto | una `Qt.AlignmentFlag` |
| `BackgroundRole` | color de fondo de la celda | un `QBrush`/`QColor` |
| `ForegroundRole` | color del texto | un `QBrush`/`QColor` |
| `ToolTipRole` | tooltip al posar el raton | un `str` |

> El color y la alineacion se dan **por rol**, no formateando el texto. Devolver `"  30"` con espacios para "alinear" es un error: para eso esta `TextAlignmentRole`.

### 4. Cabeceras: headerData

Los titulos de columna ("Nombre", "Ciudad"...) y de fila no son celdas, salen de `headerData(section, orientation, role)`. `section` es el indice de la columna o fila; `orientation` es `Qt.Orientation.Horizontal` (cabecera de columnas) o `Qt.Orientation.Vertical` (de filas). Solo respondes para `DisplayRole`:

```python
def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
    if role != Qt.ItemDataRole.DisplayRole:
        return None
    if orientation == Qt.Orientation.Horizontal:
        return ["Nombre", "Ciudad", "Edad"][section]    # titulos de columna
    return str(section + 1)                              # numero de fila (1, 2, 3...)
```

### 5. Editable: flags + setData + dataChanged

Por defecto el modelo es de **solo lectura**. Para que el usuario pueda editar una celda con doble clic hacen falta tres piezas:

1. **`flags(index)`** declara que la celda es editable añadiendo `ItemIsEditable` a las flags por defecto.
2. **`setData(index, value, role)`** recibe el nuevo valor, lo escribe en tus datos, **emite `dataChanged`** y devuelve `True` (o `False` si rechazas el valor).
3. **`self.dataChanged.emit(index, index)`** avisa a la vista de que esa celda cambio. **Sin esto la vista no se refresca**: tu dato cambia pero la pantalla sigue mostrando el viejo.

```python
def flags(self, index):
    base = super().flags(index)                          # selectable + enabled
    return base | Qt.ItemFlag.ItemIsEditable             # ...y ademas editable

def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
    if role != Qt.ItemDataRole.EditRole or not index.isValid():
        return False
    self._datos[index.row()][index.column()] = value     # 1. escribe el dato
    self.dataChanged.emit(index, index)                  # 2. AVISA a la vista (crucial)
    return True                                          # 3. confirma el cambio
```

`dataChanged.emit(top_left, bottom_right)` toma el rango de celdas afectadas; para una sola celda, el mismo `index` dos veces.

### 6. Añadir/quitar filas: beginInsertRows / endInsertRows

Cambiar el **tamaño** de la tabla (insertar o borrar filas) es distinto de cambiar un valor: la vista mantiene sus propios indices y seleccion, asi que **debe enterarse antes y despues** de la mutacion. Por eso rodeas el cambio de la lista con un par de llamadas:

```python
def insertar_fila(self, valores):
    fila = self.rowCount()                               # la insertaremos al final
    self.beginInsertRows(QModelIndex(), fila, fila)      # AVISO: voy a insertar [fila..fila]
    self._datos.append(valores)                          # muta la lista AQUI dentro
    self.endInsertRows()                                 # FIN: la vista ya se reajusto
```

El primer argumento de `beginInsertRows` es el **padre** (`QModelIndex()` vacio = la raiz, lo normal en una tabla); luego la primera y ultima fila que vas a añadir. Para borrar es identico con `beginRemoveRows(QModelIndex(), fila, fila)` ... `endRemoveRows()`.

> [!warning] Nunca mutes la lista "a pelo"
> Hacer `self._datos.append(...)` o `del self._datos[i]` **sin** el par `begin.../end...` deja a la vista desincronizada con los datos: filas fantasma, celdas que no responden o un crash al hacer scroll. La mutacion va **siempre** entre `beginInsertRows`/`endInsertRows` (o `beginRemoveRows`/`endRemoveRows`).

## Ejemplo completo: tabla editable de productos

Modelo sobre una lista de listas (columnas: nombre, precio, stock). Es editable, tiene cabeceras, alinea los numeros a la derecha, pinta el stock cero en rojo y trae un boton "Añadir fila" que usa `beginInsertRows`. Ejecutable de principio a fin:

```python
from PyQt6.QtWidgets import (
    QApplication, QTableView, QWidget, QVBoxLayout, QPushButton,
)
from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtGui import QColor
import sys


class ProductosModel(QAbstractTableModel):
    CABECERAS = ["Nombre", "Precio", "Stock"]

    def __init__(self, productos):
        super().__init__()
        self._datos = productos                          # lista de listas

    # --- obligatorios ---
    def rowCount(self, parent=None):
        return len(self._datos)

    def columnCount(self, parent=None):
        return len(self.CABECERAS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        fila, col = index.row(), index.column()
        valor = self._datos[fila][col]

        if role == Qt.ItemDataRole.DisplayRole:
            if col == 1:                                  # precio con formato
                return f"{valor:.2f} EUR"
            return str(valor)

        if role == Qt.ItemDataRole.EditRole:             # al editar, el valor crudo
            return str(valor)

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if col in (1, 2):                            # precio y stock a la derecha
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

        if role == Qt.ItemDataRole.ForegroundRole:
            if col == 2 and valor == 0:                  # stock agotado en rojo
                return QColor("red")

        return None                                      # todo lo demas: None

    # --- cabeceras ---
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self.CABECERAS[section]
        return str(section + 1)

    # --- edicion ---
    def flags(self, index):
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role != Qt.ItemDataRole.EditRole or not index.isValid():
            return False
        col = index.column()
        try:
            if col == 1:                                 # precio -> float
                value = float(value)
            elif col == 2:                               # stock -> int
                value = int(value)
        except ValueError:
            return False                                 # rechaza texto invalido
        self._datos[index.row()][col] = value
        self.dataChanged.emit(index, index)             # refresca la vista
        return True

    # --- insertar fila ---
    def anadir_producto(self, nombre="(nuevo)", precio=0.0, stock=0):
        fila = self.rowCount()
        self.beginInsertRows(QModelIndex(), fila, fila)
        self._datos.append([nombre, precio, stock])
        self.endInsertRows()


class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Productos")

        productos = [
            ["Teclado", 29.90, 12],
            ["Raton",   15.50,  0],
            ["Monitor", 199.00, 4],
        ]
        self.modelo = ProductosModel(productos)

        self.tabla = QTableView()
        self.tabla.setModel(self.modelo)
        self.tabla.resizeColumnsToContents()

        boton = QPushButton("Añadir fila")
        boton.clicked.connect(self.modelo.anadir_producto)

        layout = QVBoxLayout(self)
        layout.addWidget(self.tabla)
        layout.addWidget(boton)


app = QApplication(sys.argv)
ventana = Ventana()
ventana.resize(420, 320)
ventana.show()
sys.exit(app.exec())
```

Doble clic en una celda para editarla; el boton inserta una fila nueva y la tabla se actualiza sola. Fijate en que `productos` (la lista real) y el modelo no se duplican: el modelo opera sobre la misma lista.

## Buenas practicas

1. **El modelo es un ADAPTADOR, no un almacen.** Guarda una **referencia** a tus datos (`self._datos = datos`), no una copia. Asi no hay dos verdades que mantener sincronizadas.
2. **Implementa como minimo `rowCount`, `columnCount` y `data`.** Son el contrato basico; sin los tres la tabla no funciona.
3. **SIEMPRE `return None` para roles e indices que no manejas.** Es la causa numero uno de celdas vacias y errores raros. En PyQt6 `None` equivale al `QVariant()` vacio de C++.
4. **Valida `index.isValid()` al inicio de `data` y `setData`.** La vista puede pasarte indices invalidos; sin el chequeo, un `IndexError` te tumba.
5. **Emite `dataChanged` despues de cada edicion.** Sin `self.dataChanged.emit(index, index)` la vista no se entera y sigue mostrando el valor viejo aunque tus datos hayan cambiado.
6. **Rodea inserciones y borrados con `beginInsertRows`/`endInsertRows` (o `beginRemoveRows`/`endRemoveRows`).** Nunca mutes la lista a pelo: la vista necesita el aviso para no desincronizarse ni crashear.
7. **Usa los roles correctos.** Alineacion via `TextAlignmentRole`, color via `Background`/`ForegroundRole`, tooltip via `ToolTipRole`. No "formatees" el texto con espacios o caracteres para imitar esos efectos.
8. **Un modelo, varias vistas.** Si necesitas la misma tabla en dos sitios, conecta el **mismo** modelo a dos vistas con `setModel`; no copies los datos.
9. **Elige el modelo base segun la forma:** `QAbstractTableModel` para tablas (filas x columnas), `QAbstractListModel` para listas simples (una columna), `QAbstractItemModel` solo si necesitas arboles.
10. **Si solo buscas comodidad y no vas a reutilizar ni escalar, [[QTableWidget]] basta.** Subclasea un modelo cuando los datos son tuyos, grandes, cambian o se comparten entre vistas.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Celdas vacias o valores raros | te falto el `return None` final, o no filtras por `role` en `data` | devuelve el dato solo en su rol y `None` para el resto |
| La vista no refresca tras editar | `setData` no emite `dataChanged` | añade `self.dataChanged.emit(index, index)` tras escribir |
| Filas fantasma, celdas muertas o crash al insertar | mutaste la lista sin `beginInsertRows`/`endInsertRows` | rodea siempre la mutacion con el par `begin.../end...` |
| `IndexError` al hacer scroll o seleccionar | no validaste `index.isValid()` en `data`/`setData` | comprueba `if not index.isValid(): return None` al inicio |
| La celda no deja editarse con doble clic | falta `ItemIsEditable` en `flags` | `return super().flags(index) \| Qt.ItemFlag.ItemIsEditable` |
| Al editar aparece el texto formateado ("29.90 EUR") en el editor | devuelves el texto de `DisplayRole` tambien en `EditRole` | en `EditRole` devuelve el valor crudo, no el formateado |
| `super().__init__()` olvidado | el modelo "no responde" o falla al conectarse | llama siempre a `super().__init__()` en tu `__init__` |

## Notas relacionadas

- [[concepto_model_view]] — el patron Modelo/Vista/Delegate y cuando Widget vs View
- [[QTableView]] — la vista que consume este modelo via `setModel`
- [[QAbstractItemView]] — la base que aporta `setModel`, seleccion y señales a las vistas
- [[QTableWidget]] — el atajo item-based (modelo+vista en una clase) para datos pequeños
