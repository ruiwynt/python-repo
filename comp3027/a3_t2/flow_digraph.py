from digraph import Digraph

class FlowDigraph(Digraph):
    def __init__(self):
        self.graph = {}
        self.capacities = {}        
        self.flows = {} # (u, v): f((u, v))
    
    def add_edge(self, v1: str, v2: str, c: int):
        if not v1 in self.graph.keys():
            raise KeyError(f"vertex {v1} not in graph")
        elif not v2 in self.graph.keys():
            raise KeyError(f"vertex {v2} not in graph")
        self.graph[v1].append(v2)
        self.capacities[(v1, v2)] = c
        self.flows[(v1, v2)] = 0

    def capacity(self, edge):
        if not edge in self.capacities.keys():
            return
        return self.capacities[edge]

    def get_flow(self):
        source_edges = [("s", x) for x in self.graph["s"]]
        return sum(list(map(lambda x: self.flows[x], source_edges)))

    def read_flow_digraph(self, file_path):
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
                line = lines[i].strip().split()
                self.add_edge(line[0], line[1], int(line[2]))
                self.flows[(line[0], line[1])] = 0
                i += 1

    def residual_network(self):
        G_residual = FlowDigraph()
        for v in self.graph.keys():
            G_residual.add_vertex(v)
        for u in self.graph.keys():
            for v in self.graph[u]:
                edge = (u, v)
                c_minus_f = self.capacities[edge] - self.flows[edge]
                if c_minus_f > 0:
                    G_residual.add_edge(u, v, c_minus_f)
                if self.flows[edge] > 0:
                    G_residual.add_edge(v, u, self.flows[edge])
        return G_residual

    def max_flow(self):
        """Ford-Fulkerson implementation"""
        residual = self.residual_network()
        path = residual.find_path("s", "t")
        while path != None:
            self._augment(path)
            residual = self.residual_network()
            path = residual.find_path("s", "t")
        return self.get_flow()

    def _format_path(self, P):
        formatted = []
        for i in range(len(P)-1):
            formatted.append((P[i], P[i+1]))
        return formatted

    def _get_capacities(self, P, G):
        capacities = []
        edges = G.edges()
        for edge in P:
            if edge in edges:
                capacities.append(G.capacities[edge])
            elif tuple(reversed(edge)) in edges:
                capacities.append(G.capacities[tuple(reversed(edge))])
            else:
                raise KeyError(f"edge {edge} not in graph")
        return capacities

    def _augment(self, P):
        if P is None or len(P) == 0:
            return
        if not isinstance(P[0], tuple):
            P = self._format_path(P)
        path_capacities = self._get_capacities(P, self.residual_network())
        bottleneck = min(path_capacities)
        original_edges = self.edges() # Checking if edge forwards/backwards
        for edge in P:
            if edge in original_edges:
                self.flows[edge] += bottleneck
            if tuple(reversed(edge)) in original_edges:
                self.flows[tuple(reversed(edge))] -= bottleneck
