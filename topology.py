import json

import networkx as nx


SWITCH_TYPE = "vyhybka"
SECTION_TYPE = "usek"
TRACK_SECTION_TYPE = "tratUsek"


def build_topology_graph(data):
    return nx.Graph(data)


def find_path(graph, source, target, data):
    """Function to get sections way from start to end blocks

    :param graph: nx.Graph object
    :param source: str - source block, must be only section
    :param target: str - target block, must be only section
    :param data: dict - additional information about blocks
    :return: tuple[list, list] - sections list and switches list with states
    """
    if source not in data:
        raise ValueError("Data object doesn't have information about "
                         "block with ID {}".format(source))
    if target not in data:
        raise ValueError("Data object doesn't have information about "
                         "block with ID {}".format(target))
    if data[source]["type"] != data[target]["type"] \
            and data[source]["type"] not in (SECTION_TYPE, TRACK_SECTION_TYPE):
        accepted_blocks = "|".join([SECTION_TYPE, TRACK_SECTION_TYPE])
        raise ValueError("Source and target parameters must have '{}' "
                         "type".format(accepted_blocks))

    path = nx.shortest_path(graph, source, target)
    sections_path = []
    switch_list = []

    for i, item_id in enumerate(path):
        if item_id not in data:
            raise ValueError("Data object doesn't have information about "
                             "block with ID {}".format(item_id))

        block = data[item_id]

        if block["type"] == SECTION_TYPE:
            sections_path.append(item_id)
        elif block["type"] == SWITCH_TYPE:
            if str(path[i + 1]) not in block["relations"]:
                raise Exception(
                    "Incorrect data in block {} about related blocks: "
                    "{}. Next block for current way is {}".format(
                        item_id, block, path[i + 1]
                    )
                )

            switch_list.append((item_id, block["relations"][str(path[i + 1])]))

    return sections_path, switch_list


if __name__ == '__main__':
    with open("vztahy.json") as fp:
        data = json.load(fp)

    graph = build_topology_graph(data["relations"])

    print(find_path(graph, "323", "313", data["data"]))
