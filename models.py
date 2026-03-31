class Node:
    def __init__(self, name, blocked=False, is_start=False, is_goal=False):
        self.name = name
        self.blocked = blocked
        self.unlocked = not blocked
        self.is_start = is_start
        self.is_goal = is_goal

    def unlock(self):
        self.unlocked = True

    def __repr__(self):
        estado = "bloqueado" if self.blocked and not self.unlocked else "disponible"
        if self.is_start:
            estado = "inicio"
        if self.is_goal:
            estado = "meta"
        return f"Node({self.name}, {estado})"