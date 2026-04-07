import heapq
import time


class PuzzleSolverAStar:
    def __init__(self, puzzle_id):
        self.puzzle_id = puzzle_id

        self.puzzles = {
            "C": {
                "graph": {
                    "S": [("A", 1), ("B", 4)],
                    "A": [("C", 2)],
                    "B": [("C", 1)],
                    "C": [("G", 3)],
                    "G": []
                },
                "heuristic": {
                    "S": 4,
                    "A": 3,
                    "B": 2,
                    "C": 1,
                    "G": 0
                },
                "start": "S",
                "goal": "G"
            },
            "I": {
                "graph": {
                    "S": [("X", 2), ("Y", 5)],
                    "X": [("Z", 2)],
                    "Y": [("Z", 1)],
                    "Z": [("T", 2)],
                    "T": []
                },
                "heuristic": {
                    "S": 4,
                    "X": 2,
                    "Y": 3,
                    "Z": 1,
                    "T": 0
                },
                "start": "S",
                "goal": "T"
            }
        }

        if puzzle_id not in self.puzzles:
            raise ValueError(f"No existe puzzle configurado para el nodo {puzzle_id}")

        self.graph = self.puzzles[puzzle_id]["graph"]
        self.heuristic = self.puzzles[puzzle_id]["heuristic"]
        self.start = self.puzzles[puzzle_id]["start"]
        self.goal = self.puzzles[puzzle_id]["goal"]

        self.nodes_expanded = 0
        self.total_cost = 0
        self.execution_time = 0
        self.solution_path = []
        self.log = []

    def reconstruct_path(self, parent, goal):
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path

    def search(self):
        start_time = time.time()

        open_list = []
        heapq.heappush(open_list, (self.heuristic[self.start], 0, self.start))

        parent = {self.start: None}
        g_cost = {self.start: 0}
        closed_set = set()

        while open_list:
            f_current, current_cost, current = heapq.heappop(open_list)

            if current in closed_set:
                continue

            closed_set.add(current)
            self.nodes_expanded += 1
            self.log.append(
                f"Expandiendo {current} con g={current_cost}, h={self.heuristic[current]}, f={f_current}"
            )

            if current == self.goal:
                self.execution_time = time.time() - start_time
                self.total_cost = g_cost[current]
                self.solution_path = self.reconstruct_path(parent, current)
                self.log.append(f"Meta del puzzle encontrada: {current}")
                return True

            for neighbor, cost in self.graph[current]:
                tentative_g = g_cost[current] + cost
                f_neighbor = tentative_g + self.heuristic[neighbor]

                if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                    g_cost[neighbor] = tentative_g
                    parent[neighbor] = current
                    heapq.heappush(open_list, (f_neighbor, tentative_g, neighbor))
                    self.log.append(
                        f"Agregando {neighbor} a abiertos con g={tentative_g}, h={self.heuristic[neighbor]}, f={f_neighbor}"
                    )

        self.execution_time = time.time() - start_time
        self.log.append("No se encontró solución para el puzzle")
        return False

    def show_log(self):
        print(f"\n--- LOG DEL PUZZLE {self.puzzle_id} ---")
        for line in self.log:
            print(line)

    def show_results(self):
        print(f"\n--- RESULTADOS DEL PUZZLE {self.puzzle_id} ---")
        print(f"Nodos expandidos: {self.nodes_expanded}")
        print(f"Costo total: {self.total_cost}")
        print(f"Tiempo de ejecución: {self.execution_time:.6f} segundos")
        print(f"Camino solución: {self.solution_path}")