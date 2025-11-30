class Graph:
    def __init__(self):
        self.structure = {}
        self.dfs_order = []
        self.indx = 0

    def __iter__(self):
        if not self.structure:
            return iter([])

        start_vertex = next(iter(self.structure))
        self.dfs_order = self.dfs(start_vertex)
        self.indx = 0
        return self

    def __next__(self):
        if self.indx < len(self.dfs_order):
            vertex = self.dfs_order[self.indx]
            self.indx += 1
            return vertex
        raise StopIteration

    def add_vertex(self, vertex):
        if vertex not in self.structure:
            self.structure[vertex] = []

    def add_edge(self, vertex1, vertex2):
        if vertex1 not in self.structure:
            self.add_vertex(vertex1)
        if vertex2 not in self.structure:
            self.add_vertex(vertex2)

        self.structure[vertex1].append(vertex2)

    def dfs(self, start_vertex):
        if start_vertex not in self.structure:
            raise ValueError(f"Vertex {start_vertex} doesn't exist in graph")

        visited = []
        stack = [start_vertex]

        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.append(vertex)
                for neighbor in reversed(self.structure[vertex]):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return visited


def main():
    directed_graph = Graph()
    directed_graph.add_edge("A", "B")
    directed_graph.add_edge("A", "C")
    directed_graph.add_edge("B", "D")
    directed_graph.add_edge("B", "E")
    directed_graph.add_edge("C", "F")

    print("Directed graph:")
    for vertex, neighbors in sorted(directed_graph.structure.items()):
        print(f"{vertex}: {neighbors}")
    print()

    print("DFS from vertex 'A':")
    dfs_result_directed = directed_graph.dfs("A")
    print(dfs_result_directed)
    print()

    print("Iterating over directed graph:")
    for vertex in directed_graph:
        print(vertex, end=" ")


if __name__ == "__main__":
    main()
