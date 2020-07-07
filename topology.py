import json

import networkx as nx


def build_topology_graph(data):
    return nx.Graph(data)


def _convert_block_id_to_internal_id(block_id, mapping):
    for internal_id, id in mapping.items():
        if block_id == id:
            return internal_id


def find_all_path(graph, source, target, mapping):
    source_internal_id = _convert_block_id_to_internal_id(source, mapping)
    target_internal_id = _convert_block_id_to_internal_id(target, mapping)

    if not source_internal_id:
        raise ValueError("Source ID can't be converted into internal ID")
    if not target_internal_id:
        raise ValueError("Target ID can't be converted into internal ID")

    return (
        [mapping[internal_id] for internal_id in path]
        for path in nx.all_simple_paths(
            graph, source_internal_id, target_internal_id
        )
    )


def main():
    with open("blocks.json") as fp:
        data = json.load(fp)

    ids_mapping = data["ids"]
    graph = build_topology_graph(data["relations"])

    for path in find_all_path(graph, "321", "319", mapping=ids_mapping):
        print(path)


if __name__ == '__main__':
    main()
