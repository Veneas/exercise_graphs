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


# =-=-=-=-=-=-=-=-=-=-=-= Task 3 =-=-=-=-=-=-=-=-=-=-=-=
def dfs(graph, start):
    """
    A depth-first search starting from a given vertex.
    Return a list of vertices in the exact order they were first visited.
    :param graph:
    :param start:
    :return:
    """

    visited = set()     # Lookup to check if the vertex was seen
    order = []          # Keeping track of the exact visitation seq

    # Defining recursive helper func to do the walking
    def explore(vertex):
        visited.add(vertex)
        order.append(vertex)

        # Tie-break rule: sorting neighbours alphabetically
        for neighbour in sorted(graph[vertex]):
            # Only visiting if havent been there yet
            if neighbour not in visited:
                explore(neighbour)

    # Kicking off the recursion from the start vertex
    explore(start)

    return order


def connected_components(graph):
    """
    Finds all maximal connected components in an undirected graph.
    Returns a list of sets, where each set contains the vertices of one component.
    :param graph:
    :return:
    """

    visited_global = set()
    components = []

    # Checking every vertex in the graph
    for vertex in graph:
        # If havents visited this vettex in any previous DFS run
        if vertex not in visited_global:
            # start a new DFS to find everything connected to it
            reachable = dfs(graph, vertex)

            # Adding all newly found vertices to global visited list
            visited_global.update(reachable)

            # Storing this components as a set
            components.append(set(reachable))

    return components


def is_weakly_connected(graph):
    """
    Checks if a directed graph is weakly connected.
    It does this by "undirected shadow" of the graph and checking if that shadow has
    exactly 1 connected component.
    :param graph:
    :return:
    """
    if not graph:
        return True

    # Inizialising a new shadow graph with empty lists of all vertices
    shadow = {vertex: [] for vertex in graph}

    #Populating the shadow graph with undirected edges
    for u, neighbours in graph.items():
        for v in neighbours:
            shadow[u].append(v)
            shadow[v].append(u) # Adding reverse edge to get undirected


     # Checking the connected components of shadow graph
    components = connected_components(shadow)

    # its weakly connected if all vertices from exactly one large group
    return len(components) == 1

# =-=-=-=-=-=-=-=-=-=-=-= Task 4 =-=-=-=-=-=-=-=-=-=-=-=

def eulerian_type(graph, directed=False):
    """
    Determines if a graph has an Eulerian circuit, path, or none.
    :param graph:
    :param directed:
    :return:
    """

    if not directed:
        # Undirected graph logic
        # Checking connectivity
        comps = connected_components(graph)
        degs = degrees(graph)

        # Caring only about components that actually have edges.
        # Isolated vertices dont break Eulerian paths
        active_comps = [c for c in comps if any(degs[v] > 0 for v in c)]
        if len(active_comps) > 1:
            return "none"

        # Counting vertices with an odd degree
        odd_count = sum(1 for v, d in degs.items() if d % 2 != 0)

        # Applying eulerian rules
        if odd_count == 0:
            return "circuit"
        elif odd_count == 2:
            return "path"
        else:
            return "none"
    else:
        # Directed graph logic

        # Checking weak connectivity
        in_deg, out_deg = in_out_degree(graph)

        # Similarly to undirectred, ensuring all edges from a signle connected component
        # builing a shawdow to check active components
        shadow = {v: [] for v in graph}
        for u, neighs in graph.items():
            for v in neighs:
                shadow[u].append(v)
                shadow[v].append(u)

        comps = connected_components(shadow)
        active_comps = [c for c in comps if any(len(shadow[v]) > 0 for v in c)]
        if len(active_comps) > 1:
            return "none"

        # COunting degree imbalances
        start_nodes = 0
        end_nodes = 0

        for v in graph:
            diff = out_deg[v] - in_deg[v]

            if diff == 0:
                continue
            elif diff == 1:
                start_nodes += 1
            elif diff == -1:
                end_nodes += 1
            else:
                # If any vertex has an excess, an eulerian path is impossible
                return "none"
        # Applying eulerian rules
        if start_nodes == 0 and end_nodes == 0:
            return "circuit"
        elif start_nodes == 1 and end_nodes == 1:
            return "path"
        else:
            return "None"



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

    # =-=-=-=-=-=-=-=-=-=-=-= Task 3 =-=-=-=-=-=-=-=-=-=-=-=
    print("\nDFS starting from P1: ", dfs(undirected_graph, "P1"))
    # Adding a disconnected component to test connected_components
    disconnected_edges = [("A", "B"), ("C", "D")]
    disc_graph = build_adjacency_list(disconnected_edges, directed=False)

    print("\nConnected components: (2 sets!)", connected_components(disc_graph))
    print("\nIs the directed PPI graph weakly connected?", is_weakly_connected(disc_graph))

    # =-=-=-=-=-=-=-=-=-=-=-= Task 4 =-=-=-=-=-=-=-=-=-=-=-=
    print("\n Undirected PPI eulerian type:", eulerian_type(undirected_graph, directed=False))
    print("\n Directed PPI eulerian type:", eulerian_type(disc_graph, directed=True))