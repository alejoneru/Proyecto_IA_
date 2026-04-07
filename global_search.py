from collections import deque
import time
from puzzle_solver import PuzzleSolverAStar


class GlobalSearchBFS:
    def __init__(self, graph):
        self.graph = graph
        self.nodes_expanded = 0
        self.max_depth = 0
        self.execution_time = 0
        self.solution_path = []
        self.log = []

        self.puzzles_solved = 0
        self.local_nodes_expanded = 0
        self.local_total_cost = 0
        self.local_execution_time = 0

        self.puzzle_details = []

    def reconstruct_path(self, parent, goal):
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path

    def solve_locked_node(self, node_name):
        self.log.append(f"Se encontró nodo bloqueado: {node_name}")
        self.log.append(f"Iniciando búsqueda informada para desbloquear {node_name}")

        puzzle = PuzzleSolverAStar(node_name)
        solved = puzzle.search()

        for line in puzzle.log:
            self.log.append(f"[PUZZLE {node_name}] {line}")

        if solved:
            self.graph.unlock_node(node_name)
            self.puzzles_solved += 1
            self.local_nodes_expanded += puzzle.nodes_expanded
            self.local_total_cost += puzzle.total_cost
            self.local_execution_time += puzzle.execution_time

            self.puzzle_details.append({
                "node": node_name,
                "path": puzzle.solution_path,
                "cost": puzzle.total_cost,
                "expanded": puzzle.nodes_expanded,
                "time": puzzle.execution_time,
                "graph": puzzle.graph,
                "heuristic": puzzle.heuristic
            })

            self.log.append(f"Puzzle resuelto. Nodo {node_name} desbloqueado.")
            return True
        else:
            self.log.append(f"No se pudo desbloquear el nodo {node_name}.")
            return False

    def search(self):
        start_node = self.graph.get_start_node()
        goal_node = self.graph.get_goal_node()

        if start_node is None or goal_node is None:
            raise ValueError("El grafo debe tener un nodo inicial y un nodo meta")

        start_time = time.time()

        queue = deque()
        queue.append((start_node.name, 0))

        visited = set()
        visited.add(start_node.name)

        parent = {start_node.name: None}

        while queue:
            current_name, depth = queue.popleft()

            self.nodes_expanded += 1
            self.max_depth = max(self.max_depth, depth)
            self.log.append(f"Expandiendo nodo {current_name}")

            if current_name == goal_node.name:
                self.execution_time = time.time() - start_time
                self.solution_path = self.reconstruct_path(parent, current_name)
                self.log.append(f"Meta encontrada: {current_name}")
                return True

            for neighbor_name in self.graph.get_neighbors(current_name):
                neighbor_node = self.graph.get_node(neighbor_name)

                if neighbor_name not in visited:
                    if neighbor_node.blocked and not neighbor_node.unlocked:
                        solved = self.solve_locked_node(neighbor_name)

                        if solved:
                            visited.add(neighbor_name)
                            parent[neighbor_name] = current_name
                            queue.append((neighbor_name, depth + 1))
                            self.log.append(f"Agregando nodo desbloqueado a la cola: {neighbor_name}")
                        continue

                    visited.add(neighbor_name)
                    parent[neighbor_name] = current_name
                    queue.append((neighbor_name, depth + 1))
                    self.log.append(f"Agregando nodo a la cola: {neighbor_name}")

        self.execution_time = time.time() - start_time
        self.log.append("No se encontró solución en el grafo global")
        return False

    def show_results(self):
        print("\n--- RESULTADOS DE LA BÚSQUEDA GLOBAL ---")
        print(f"Nodos expandidos: {self.nodes_expanded}")
        print(f"Profundidad máxima alcanzada: {self.max_depth}")
        print(f"Tiempo de ejecución global: {self.execution_time:.6f} segundos")
        print(f"Camino solución global: {self.solution_path}")

        print("\n--- RESULTADOS DE LOS PUZZLES ---")
        print(f"Puzzles resueltos: {self.puzzles_solved}")
        print(f"Nodos expandidos en puzzles: {self.local_nodes_expanded}")
        print(f"Costo total de puzzles: {self.local_total_cost}")
        print(f"Tiempo total en puzzles: {self.local_execution_time:.6f} segundos")

        if self.puzzle_details:
            print("\n--- DETALLE DE CADA PUZZLE ---")
            for detail in self.puzzle_details:
                print(
                    f"Nodo {detail['node']} -> camino {detail['path']}, "
                    f"costo {detail['cost']}, "
                    f"expandidos {detail['expanded']}, "
                    f"tiempo {detail['time']:.6f} s"
                )

    def show_log(self):
        print("\n--- LOG DE EJECUCIÓN HÍBRIDA ---")
        for line in self.log:
            print(line)