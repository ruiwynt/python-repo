import sys 

class Digraph():
    def __init__(self):
        self.graph = {}

    def add_vertex(self, v: str):
        if v in self.graph.keys():
            raise KeyError(f"vertex {v} already in graph")
        self.graph[v] = []

    def add_edge(self, v1: str, v2: str):
        if not v1 in self.graph.keys():
            raise KeyError(f"vertex {v1} not in graph")
        elif not v2 in self.graph.keys():
            raise KeyError(f"vertex {v2} not in graph")
        self.graph[v1].append(v2)

    def edges(self):
        edges = []
        for u in self.graph.keys():
            for v in self.graph[u]:
                edges.append((u, v))
        return edges
    
    def vertices(self):
        return list(self.graph.keys())

    def find_path(self, v1, v2):
        def find_path_recurse(node, target, path, visited):
            if node in visited:
                return None
            path = path.copy() + [node]
            visited.add(node)
            if node == target:
                return path
            for child in self.graph[node]:
                new_path = find_path_recurse(child, target, path, visited)
                if new_path is not None:
                    return new_path
            return None
        return find_path_recurse(v1, v2, [], set())

    def read_digraph(self, file_path):
        i = 0
        with open(file_path, "r") as f:
            lines = f.readlines()
            n_vertices = int(lines[i])
            i += 1
            current_i = i
            while i < n_vertices + current_i:
                self.add_vertex(lines[i].strip())
                i += 1
            n_edges = int(lines[i])
            i += 1 
            current_i = i
            while i < n_edges + current_i:
                vertices = lines[i].strip().split()
                self.add_edge(vertices[0], vertices[1])
                i += 1
