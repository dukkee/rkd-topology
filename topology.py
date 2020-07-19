import json

import networkx as nx


def build_topology_graph(data):
    return nx.Graph(data)


def find_all_path(graph, source, target):
    return nx.all_simple_paths(graph, source, target)


def main():
    with open("vztahy.json") as fp:
        data = json.load(fp)

    graph = build_topology_graph(data["relations"])

    for path in find_all_path(graph, "321", "319"):
        print(path)


if __name__ == '__main__':
    main()
