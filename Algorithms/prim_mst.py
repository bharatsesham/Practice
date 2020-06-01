import sys
from heapq import heappop, heappush, heapify
from collections import defaultdict


def prim_mst(graph, source_vertex='1'):
    total_weight = 0
    mst = defaultdict(set)
    visited = set(source_vertex)
    edges = [(weight, source_vertex, sv_child) for sv_child, weight in graph[source_vertex].items()]
    heapify(edges)
    while edges:
        weight, v_parent, v_child = heappop(edges)
        if v_child not in visited:
            visited.add(v_child)
            mst[v_parent].add(v_child)
            total_weight += weight
            for vv_child, weight in graph[v_child].items():
                if vv_child not in visited:
                    heappush(edges, (weight, v_child, vv_child))
    return total_weight, mst


if __name__ == '__main__':
    node = sys.stdin.readline().rstrip()
    input_text = sys.stdin.readlines()
    input_graph = defaultdict(dict)
    for line in input_text:
        data = line.strip().split(' ')
        input_graph[data[0]][data[1]] = int(data[2])
        input_graph[data[1]][data[0]] = int(data[2])
    f_mst = prim_mst(input_graph)
    print(f_mst[0])
    for u_edge, v_edges in f_mst[1].items():
        for v_edge in v_edges:
            print(u_edge, v_edge)

