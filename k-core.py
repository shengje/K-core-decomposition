import sys
import time
from collections import defaultdict

def addEdge(graph, u, v):
    graph[u].append(v)
    graph[v].append(u)
    return graph

def get_degree(G):
    degree = {}
    for i in G:
        degree[i] = len(G[i])
    return degree

def core_number(G):
    degrees = get_degree(G)
    # Sort nodes by degree.
    nodes = sorted(degrees, key=degrees.get)
    bin_boundaries = [0]
    curr_degree = 0
    for i, v in enumerate(nodes):
        if degrees[v] > curr_degree:
            bin_boundaries.extend([i] * (degrees[v] - curr_degree))
            curr_degree = degrees[v]
    node_pos = {v: pos for pos, v in enumerate(nodes)}
    # The initial guess for the core number of a node is its degree.
    core = degrees
    #nbrs = {v: list(nx.all_neighbors(G, v)) for v in G}
    for v in nodes:
        for u in G[v]:
            if core[u] > core[v]:
                G[u].remove(v)
                pos = node_pos[u]
                bin_start = bin_boundaries[core[u]]
                node_pos[u] = bin_start
                node_pos[nodes[bin_start]] = pos
                nodes[bin_start], nodes[pos] = nodes[pos], nodes[bin_start]
                bin_boundaries[core[u]] += 1
                core[u] -= 1
    return core

def find_kcores(G):

    k_cores = {}          #dictionary to hold proteins and the highest k-core they belong to
    highest_kcore =0    #keep track of the hightest recored k-core
    core_n = core_number(G)

    for node, k_core in core_n.items():

        if highest_kcore < k_core: #keep track of the highest k-core
            highest_kcore = k_core
        if k_core in k_cores:
            k_cores[k_core].append(node)
        else:
            k_cores[k_core]=[node]

    return highest_kcore, k_cores

if __name__ == "__main__":
    t = time.time()
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    graph = defaultdict(list)
    with open(input_file, "r") as file:
        for edge in file:
            nodes = edge.rstrip("\n").split(" ")
            graph = addEdge(graph, nodes[0], nodes[1])
    
    highest_k, k_cores = find_kcores(graph)

    with open(output_file, "w") as fout:
        for i in sorted(k_cores[highest_k]):
            fout.write(str(i)+"\n")

    print(highest_k)
    print(time.time() - t, 's')