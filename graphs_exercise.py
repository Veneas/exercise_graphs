# =-=-=-=-=-=-=-=-=-=-=-= Task 1 =-=-=-=-=-=-=-=-=-=-=-=

def build_adjacency_list(edges, directed = False):
    """
    Builds an adjacency list representation of a graph from a list of edges.
    :param edges:
    :param directed:
    :return:
    """
    graph = {}
    # First pass -> ensuring every vertex is mentioned anywhere in the edges
    # initialised with an empty list in dict

    for u, v in edges:
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []

    # Second pass -> populating the neighbour lists based on the edges
    for u, v in edges:
        graph[u].append(v)
        # If the graph is undirected, adding a reverse edge as well
        if not directed:
            graph[v].append(u)

    return graph


def degrees(graph):
    """
    Calculating the degree of every vertex in a undirected graph.
    Number of connection vertex has.
    :param graph:
    :return:
    """

    # Dict comprehension to map each vertex to the length of its neighbour
    return {vertex: len(neighbours) for vertex, neighbours in graph.items()}


def in_out_degree(graph):
    """
    Calculating the in-degree and out-degree for every vertex in a directed graph.
    Returns a tuple of two dicts: (in_degree, out_degree)
    :param graph:
    :return:
    """
    # Initialising counts for all vertices to 0
    in_degree = {vertex: 0 for vertex in graph}

    # Out-degree is simply the outgoing edges a vertex has
    out_degree = {vertex: len(neighbours) for vertex, neighbours in graph.items()}

    # To find in-degrees, checking every edge in the graph and counting how
    # many items each vertex is a "target" (v)
    for u, neighbours in graph.items():
        for v in neighbours:
            in_degree[v] += 1

    return in_degree, out_degree





# =-=-=-=-=-=-=-=-=-=-=-=
#         MAIN
# =-=-=-=-=-=-=-=-=-=-=-=

if __name__ == '__main__':
# =-=-=-=-=-=-=-=-=-=-=-= Task 1 =-=-=-=-=-=-=-=-=-=-=-=
    V = {"P1", "P2", "P3", "P4", "P5"}
    E = {("P1", "P2"),
         ("P1", "P3"),
         ("P2", "P3"),
         ("P3", "P4"),
         ("P4", "P5")}
    # Undirected graph
    undirected_graph = build_adjacency_list(E, directed=False)
    print("Undirected adjacency list:")
    for node, edges_list in undirected_graph.items():
        print(f"{node} -> {edges_list}")

    print("\nUndirected degrees:")
    print(" ", degrees(undirected_graph))

    # Testing directed graph
    directed_graph = build_adjacency_list(E, directed=True)
    in_deg, out_deg = in_out_degree(directed_graph)

    print("\n Directed in/out degrees:")
    print(" In: ", in_deg)
    print(" Out: ", out_deg)

    # Self-check
    print("\nSelf-check passed (in == out == edges)?",
          sum(in_deg.values()) == sum(out_deg.values()) == len(E))