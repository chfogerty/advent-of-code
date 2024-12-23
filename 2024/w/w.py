def find_cycles(graph):
    cycles = set()
    for root in graph:
        for node_1 in graph[root]:
            for node_2 in graph[node_1]:
                if root in graph[node_2]:
                    cycles.add(tuple(sorted([root, node_1, node_2])))
    return cycles

def find_t_cycles(graph):
    cycles = find_cycles(graph)
    t_cycles = set()
    for a, b, c in cycles:
        if 't' == a[0] or 't' == b[0] or 't' == c[0]:
            t_cycles.add((a, b, c))
    return t_cycles

def BronKerbosch(R, P, X, graph):
    in_lan = R.copy()
    potential_iter = P.copy()
    potential = P.copy()
    excluded = X.copy()
    cliques = []
    if len(potential_iter) == 0 and len(excluded) == 0:
        return [in_lan]
    for node in potential_iter:
        cliques.extend(BronKerbosch(in_lan.union({node}), potential.intersection(graph[node]), excluded.intersection(graph[node]), graph))
        potential -= {node}
        excluded.add(node)
    return cliques

def find_LAN(graph):
    cliques = sorted(BronKerbosch(set(), set(graph.keys()), set(), graph), key=len, reverse=True)
    return sorted(list(cliques[0]))

def parse(filename):
    graph = dict()
    with open(filename, 'r') as file:
        for line in file:
            a, b = line.strip().split('-')
            if a not in graph:
                graph[a] = set()
            if b not in graph:
                graph[b] = set()
            graph[a].add(b)
            graph[b].add(a)
    return graph

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    network = parse(filename)
    print(len(find_t_cycles(network)))
    print(','.join(find_LAN(network)))
