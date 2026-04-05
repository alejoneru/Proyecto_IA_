print("UI cargando...")

import tkinter as tk
from tkinter import scrolledtext
print("Antes de imports internos")
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from global_graph import EscapeRoomGraph
print("Import graph OK")
from global_search import GlobalSearchBFS
print("Import search OK")


class EscapeRoomUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Escape Room IA - Sistema Híbrido")
        self.root.geometry("1350x780")
        self.root.configure(bg="#f2f2f2")

        self.graph = self.build_sample_escape_room()
        self.search_engine = None
        self.selected_puzzle = tk.StringVar(value="")

        # Panel izquierdo y derecho
        self.left_frame = tk.Frame(root, width=760, height=780, bg="#f2f2f2")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.right_frame = tk.Frame(root, width=560, height=780, bg="#f2f2f2")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=8, pady=8)

        # ======================
        # PANEL IZQUIERDO
        # ======================
        self.graph_container = tk.Frame(self.left_frame, bg="white", bd=1, relief="solid")
        self.graph_container.pack(fill=tk.BOTH, expand=True)

        self.graph_title = tk.Label(
            self.graph_container,
            text="Grafo Global del Escape Room",
            font=("Arial", 18, "bold"),
            bg="white"
        )
        self.graph_title.pack(pady=(15, 8))

        # Leyenda
        self.legend_frame = tk.Frame(self.graph_container, bg="white")
        self.legend_frame.pack(pady=(0, 8))

        self.add_legend_item(self.legend_frame, "green", "Inicio")
        self.add_legend_item(self.legend_frame, "red", "Meta")
        self.add_legend_item(self.legend_frame, "gray", "Bloqueado")
        self.add_legend_item(self.legend_frame, "skyblue", "Disponible")
        self.add_legend_item(self.legend_frame, "gold", "Camino solución")

        self.graph_canvas_frame = tk.Frame(self.graph_container, bg="white")
        self.graph_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # ======================
        # PANEL DERECHO
        # ======================
        self.header_card = tk.Frame(self.right_frame, bg="white", bd=1, relief="solid")
        self.header_card.pack(fill=tk.X, pady=(0, 8))

        self.title_label = tk.Label(
            self.header_card,
            text="Escape Room IA",
            font=("Arial", 20, "bold"),
            bg="white"
        )
        self.title_label.pack(pady=(15, 10))

        self.button_frame = tk.Frame(self.header_card, bg="white")
        self.button_frame.pack(pady=(0, 15))

        self.run_button = tk.Button(
            self.button_frame,
            text="Ejecutar sistema híbrido",
            font=("Arial", 12, "bold"),
            bg="#1f77b4",
            fg="white",
            padx=12,
            pady=6,
            command=self.run_search
        )
        self.run_button.pack(side=tk.LEFT, padx=8)

        self.reset_button = tk.Button(
            self.button_frame,
            text="Reiniciar",
            font=("Arial", 12, "bold"),
            bg="#6c757d",
            fg="white",
            padx=12,
            pady=6,
            command=self.reset_ui
        )
        self.reset_button.pack(side=tk.LEFT, padx=8)

        self.metrics_card = tk.Frame(self.right_frame, bg="white", bd=1, relief="solid")
        self.metrics_card.pack(fill=tk.X, pady=(0, 8))

        self.metrics_title = tk.Label(
            self.metrics_card,
            text="Métricas del sistema",
            font=("Arial", 13, "bold"),
            bg="white"
        )
        self.metrics_title.pack(pady=(10, 5))

        self.metrics_label = tk.Label(
            self.metrics_card,
            text="Métricas aparecerán aquí",
            justify="left",
            anchor="w",
            font=("Arial", 11),
            bg="white"
        )
        self.metrics_label.pack(fill=tk.X, padx=15, pady=(0, 12))

        self.puzzle_card = tk.Frame(self.right_frame, bg="white", bd=1, relief="solid", height=320)
        self.puzzle_card.pack(fill=tk.X, pady=(0, 8))
        self.puzzle_card.pack_propagate(False)

        self.puzzle_title = tk.Label(
            self.puzzle_card,
            text="Puzzle actual / resuelto",
            font=("Arial", 13, "bold"),
            bg="white"
        )
        self.puzzle_title.pack(pady=(10, 5))

        self.selector_frame = tk.Frame(self.puzzle_card, bg="white")
        self.selector_frame.pack(pady=(0, 8))

        self.selector_label = tk.Label(
            self.selector_frame,
            text="Seleccionar puzzle:",
            font=("Arial", 10),
            bg="white"
        )
        self.selector_label.pack(side=tk.LEFT, padx=(0, 8))

        self.puzzle_selector = tk.OptionMenu(
            self.selector_frame,
            self.selected_puzzle,
            ""
        )
        self.puzzle_selector.config(font=("Arial", 10), width=8)
        self.puzzle_selector.pack(side=tk.LEFT)

        self.selected_puzzle.trace_add("write", self.on_puzzle_selected)

        self.puzzle_frame = tk.Frame(self.puzzle_card, bg="white", height=230)
        self.puzzle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.puzzle_frame.pack_propagate(False)

        self.log_card = tk.Frame(self.right_frame, bg="white", bd=1, relief="solid")
        self.log_card.pack(fill=tk.BOTH, expand=True)

        self.log_title = tk.Label(
            self.log_card,
            text="Log de ejecución",
            font=("Arial", 13, "bold"),
            bg="white"
        )
        self.log_title.pack(pady=(10, 5))

        self.log_area = scrolledtext.ScrolledText(
            self.log_card,
            width=60,
            height=11,
            font=("Consolas", 10),
            bd=0
        )
        self.log_area.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

        self.draw_graph()

    def add_legend_item(self, parent, color, text):
        item = tk.Frame(parent, bg="white")
        item.pack(side=tk.LEFT, padx=8)

        canvas = tk.Canvas(item, width=16, height=16, bg="white", highlightthickness=0)
        canvas.create_oval(2, 2, 14, 14, fill=color, outline=color)
        canvas.pack(side=tk.LEFT)

        label = tk.Label(item, text=text, bg="white", font=("Arial", 9))
        label.pack(side=tk.LEFT, padx=(4, 0))

    def build_sample_escape_room(self):
        graph = EscapeRoomGraph()

        graph.add_node("A", is_start=True)
        graph.add_node("B")
        graph.add_node("C", blocked=True)
        graph.add_node("E")
        graph.add_node("G")
        graph.add_node("I", blocked=True)
        graph.add_node("M", is_goal=True)

        graph.add_edge("A", "B")
        graph.add_edge("A", "E")
        graph.add_edge("B", "C")
        graph.add_edge("E", "G")
        graph.add_edge("G", "C")
        graph.add_edge("C", "I")
        graph.add_edge("I", "M")

        return graph

    def get_node_color(self, node):
        if node.is_start:
            return "green"
        if node.is_goal:
            return "red"
        if node.blocked and not node.unlocked:
            return "gray"
        return "skyblue"

    def draw_graph(self):
        for widget in self.graph_canvas_frame.winfo_children():
            widget.destroy()

        G = nx.DiGraph()

        for node_name in self.graph.nodes:
            G.add_node(node_name)

        for source, targets in self.graph.edges.items():
            for target in targets:
                G.add_edge(source, target)

        pos = {
            "A": (0, 0),
            "B": (1.2, -0.1),
            "E": (-0.7, 0),
            "G": (0.3, 0.3),
            "C": (1.0, 0.45),
            "I": (1.7, -1.0),
            "M": (2.8, -2.2)
        }

        path_list = self.search_engine.solution_path if self.search_engine else []
        path_nodes = set(path_list)
        path_edges = set()

        for i in range(len(path_list) - 1):
            path_edges.add((path_list[i], path_list[i + 1]))

        colors = []
        edge_colors = []
        widths = []

        for node_name in G.nodes():
            node = self.graph.get_node(node_name)

            if node.is_start:
                colors.append("green")
            elif node.is_goal:
                colors.append("red")
            elif node_name in path_nodes:
                colors.append("gold")
            else:
                colors.append(self.get_node_color(node))

        for edge in G.edges():
            if edge in path_edges:
                edge_colors.append("orange")
                widths.append(3)
            else:
                edge_colors.append("black")
                widths.append(1.2)

        fig, ax = plt.subplots(figsize=(7.6, 6.6))
        fig.patch.set_facecolor("white")

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=colors,
            node_size=2300,
            font_size=12,
            font_weight="bold",
            arrows=True,
            edge_color=edge_colors,
            width=widths,
            ax=ax
        )

        ax.set_axis_off()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def draw_puzzle(self, puzzle_detail):
        for widget in self.puzzle_frame.winfo_children():
            widget.destroy()

        G = nx.DiGraph()

        for source, targets in puzzle_detail["graph"].items():
            G.add_node(source)
            for target, cost in targets:
                G.add_node(target)
                G.add_edge(source, target, weight=cost)

        pos = nx.spring_layout(G, seed=20)

        path_nodes = set(puzzle_detail["path"])
        path_edges = set()

        for i in range(len(puzzle_detail["path"]) - 1):
            path_edges.add((puzzle_detail["path"][i], puzzle_detail["path"][i + 1]))

        colors = []
        edge_colors = []
        widths = []

        for node in G.nodes():
            if node == puzzle_detail["path"][0]:
                colors.append("lightgreen")
            elif node == puzzle_detail["path"][-1]:
                colors.append("tomato")
            elif node in path_nodes:
                colors.append("khaki")
            else:
                colors.append("lightgray")

        for edge in G.edges():
            if edge in path_edges:
                edge_colors.append("orange")
                widths.append(2.5)
            else:
                edge_colors.append("black")
                widths.append(1.1)

        fig, ax = plt.subplots(figsize=(5.4, 2.8))
        fig.patch.set_facecolor("white")

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=colors,
            node_size=1350,
            font_size=11,
            font_weight="bold",
            arrows=True,
            edge_color=edge_colors,
            width=widths,
            ax=ax
        )

        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=edge_labels,
            ax=ax,
            font_size=9
        )

        ax.set_title(f"Puzzle del nodo {puzzle_detail['node']}", fontsize=14, fontweight="bold")
        ax.set_axis_off()

        canvas = FigureCanvasTkAgg(fig, master=self.puzzle_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_puzzle_selector(self):
        menu = self.puzzle_selector["menu"]
        menu.delete(0, "end")

        if self.search_engine and self.search_engine.puzzle_details:
            for detail in self.search_engine.puzzle_details:
                node_name = detail["node"]
                menu.add_command(
                    label=node_name,
                    command=lambda value=node_name: self.selected_puzzle.set(value)
                )

            self.selected_puzzle.set(self.search_engine.puzzle_details[0]["node"])
        else:
            menu.add_command(label="", command=lambda: self.selected_puzzle.set(""))

    def on_puzzle_selected(self, *args):
        if not self.search_engine:
            return

        selected = self.selected_puzzle.get()
        for detail in self.search_engine.puzzle_details:
            if detail["node"] == selected:
                self.draw_puzzle(detail)
                break

    def run_search(self):
        self.search_engine = GlobalSearchBFS(self.graph)
        found = self.search_engine.search()

        self.log_area.delete("1.0", tk.END)

        for line in self.search_engine.log:
            self.log_area.insert(tk.END, line + "\n")

        self.log_area.see(tk.END)

        metrics_text = (
            f"Nodos expandidos globalmente: {self.search_engine.nodes_expanded}\n"
            f"Profundidad máxima: {self.search_engine.max_depth}\n"
            f"Tiempo global: {self.search_engine.execution_time:.6f} s\n"
            f"Camino global: {' → '.join(self.search_engine.solution_path)}\n\n"
            f"Puzzles resueltos: {self.search_engine.puzzles_solved}\n"
            f"Nodos expandidos en puzzles: {self.search_engine.local_nodes_expanded}\n"
            f"Costo total de puzzles: {self.search_engine.local_total_cost}\n"
            f"Tiempo total en puzzles: {self.search_engine.local_execution_time:.6f} s\n\n"
        )

        if found:
            metrics_text += "Resultado: Se encontró la salida."
        else:
            metrics_text += "Resultado: No se encontró solución."

        self.metrics_label.config(text=metrics_text)

        self.draw_graph()
        self.update_puzzle_selector()

    def reset_ui(self):
        self.graph = self.build_sample_escape_room()
        self.search_engine = None
        self.selected_puzzle.set("")
        self.metrics_label.config(text="Métricas aparecerán aquí")
        self.log_area.delete("1.0", tk.END)

        for widget in self.puzzle_frame.winfo_children():
            widget.destroy()

        menu = self.puzzle_selector["menu"]
        menu.delete(0, "end")
        menu.add_command(label="", command=lambda: self.selected_puzzle.set(""))

        self.draw_graph()