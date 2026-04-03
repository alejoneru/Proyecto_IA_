# Escape Room Solver — Búsqueda Híbrida BFS + A*

## Descripción General

Este proyecto implementa un sistema de **búsqueda híbrida** para resolver un **Escape Room** representado como un grafo dirigido. Combina dos estrategias de búsqueda:

- **BFS (Búsqueda por Amplitud)** para recorrer el grafo global del Escape Room.
- **A* (A-Star)** como búsqueda informada local para desbloquear nodos bloqueados (puzzles) encontrados durante el recorrido.

El agente navega por el grafo del Escape Room desde un nodo inicial hasta un nodo meta. Cuando encuentra un nodo bloqueado, lanza automáticamente un solver A* para resolverlo y continuar el recorrido.

---

## Integrantes

| Nombre                  |
|-------------------------|
| Alejandro Urrego        |
| Juan David Ascencio     |
| Andrés Felipe Salcedo   |
| Juan Camilo Vélez       |

---

##  Estructura del Proyecto

```
├── models.py           # Definición de la clase Node
├── global_graph.py     # Definición del grafo global (EscapeRoomGraph)
├── global_search.py    # Algoritmo BFS global con integración de puzzles
├── Puzzle_solver.py    # Algoritmo A* para resolver puzzles locales
└── test_librerias.py   # Script de verificación de dependencias
```

---

##  Descripción de Archivos

### `models.py`
Define la clase `Node`, unidad base del grafo. Cada nodo tiene:
- `name`: identificador del nodo.
- `blocked`: indica si el nodo está bloqueado (requiere resolver un puzzle).
- `unlocked`: indica si el nodo ya fue desbloqueado.
- `is_start` / `is_goal`: marcan el nodo de inicio y el nodo meta.
- Método `unlock()`: desbloquea el nodo una vez el puzzle es resuelto.

---

### `global_graph.py`
Define la clase `EscapeRoomGraph`, que representa el grafo global del Escape Room:
- Permite agregar nodos con `add_node()` y aristas con `add_edge()`.
- Provee métodos para obtener vecinos, nodo inicio, nodo meta y desbloquear nodos.
- Incluye métodos de visualización (`show_graph()`, `show_nodes()`) para mostrar el estado actual del grafo.

---

### `global_search.py`
Implementa la clase `GlobalSearchBFS`, el núcleo del sistema híbrido:
- Recorre el grafo global usando **BFS**.
- Al encontrar un nodo bloqueado, invoca `PuzzleSolverAStar` para resolverlo localmente.
- Si el puzzle es resuelto, el nodo se desbloquea y el BFS continúa.
- Registra métricas: nodos expandidos, profundidad máxima, tiempo de ejecución, puzzles resueltos y detalle de cada puzzle.

**Flujo principal:**
```
Inicio → BFS expande nodos → Nodo bloqueado encontrado
       → A* resuelve puzzle → Nodo desbloqueado
       → BFS continúa → Nodo meta alcanzado
```

---

### `Puzzle_solver.py`
Implementa la clase `PuzzleSolverAStar`, que resuelve puzzles locales mediante el algoritmo **A***:
- Usa una cola de prioridad (`heapq`) con función de evaluación `f(n) = g(n) + h(n)`.
- Puzzles disponibles:
  - **Puzzle C**: grafo `S → A/B → C → G` con heurísticas definidas.
  - **Puzzle I**: grafo `S → X/Y → Z → T` con heurísticas definidas.
- Registra el camino solución, costo total, nodos expandidos y tiempo de ejecución.

**Fórmula A*:**
> `f(n) = g(n) + h(n)`
> donde `g(n)` = costo acumulado desde el inicio, `h(n)` = heurística estimada al objetivo.

---

### `test_librerias.py`
Script de verificación que confirma que todas las dependencias necesarias están correctamente instaladas:

```python
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import tkinter as tk

print("Todo instalado correctamente")
```

---

## ⚙️ Dependencias

| Librería       | Uso                                      |
|----------------|------------------------------------------|
| `networkx`     | Representación y análisis de grafos      |
| `matplotlib`   | Visualización de grafos                  |
| `pyvis`        | Visualización interactiva de grafos      |
| `tkinter`      | Interfaz gráfica (GUI)                   |
| `heapq`        | Cola de prioridad para A* (stdlib)       |
| `collections`  | `deque` para BFS (stdlib)                |

### Instalación

```bash
pip install networkx matplotlib pyvis
```

> `tkinter` viene incluido con la instalación estándar de Python.

---

##  Ejecución

1. Verificar dependencias:
```bash
python test_librerias.py
```

2. Ejecutar la búsqueda principal (desde el archivo principal que instancia el grafo y llama a `GlobalSearchBFS`):
```bash
python main.py
```

---

##  Métricas Reportadas

Al finalizar la ejecución, el sistema reporta:

- **Búsqueda Global (BFS):**
  - Nodos expandidos
  - Profundidad máxima alcanzada
  - Tiempo de ejecución
  - Camino solución global

- **Puzzles Locales (A*):**
  - Cantidad de puzzles resueltos
  - Nodos expandidos por puzzle
  - Costo total acumulado
  - Tiempo total en puzzles
  - Detalle de cada puzzle (camino, costo, nodos, tiempo)

---

##  Algoritmos Utilizados

### BFS — Búsqueda por Amplitud
Garantiza encontrar el camino más corto en grafos no ponderados. Explora nivel por nivel desde el nodo inicial.

### A* — Búsqueda Heurística Informada
Encuentra el camino de menor costo usando `f(n) = g(n) + h(n)`. Es completo y óptimo cuando la heurística es admisible (no sobreestima el costo real).

---

*Proyecto desarrollado para la asignatura de Inteligencia Artificial — 2026*
