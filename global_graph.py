from models import Node


class EscapeRoomGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, name, blocked=False, is_start=False, is_goal=False):
        node = Node(name, blocked, is_start, is_goal)
        self.nodes[name] = node
        self.edges[name] = []

    def add_edge(self, source, target):
        if source in self.nodes and target in self.nodes:
            self.edges[source].append(target)
        else:
            raise ValueError("Uno o ambos nodos no existen en el grafo")

    def get_neighbors(self, node_name):
        return self.edges.get(node_name, [])

    def get_node(self, node_name):
        return self.nodes.get(node_name)

    def get_start_node(self):
        for node in self.nodes.values():
            if node.is_start:
                return node
        return None

    def get_goal_node(self):
        for node in self.nodes.values():
            if node.is_goal:
                return node
        return None

    def unlock_node(self, node_name):
        node = self.get_node(node_name)
        if node:
            node.unlock()

    def show_graph(self):
        print("\n--- GRAFO GLOBAL DEL ESCAPE ROOM ---")
        for node_name, neighbors in self.edges.items():
            print(f"{node_name} -> {neighbors}")

    def show_nodes(self):
        print("\n--- ESTADO DE LOS NODOS ---")
        for node in self.nodes.values():
            print(node)