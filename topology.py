import json
import argparse

import networkx as nx


SWITCH_TYPE = "vyhybka"
SECTION_TYPE = "usek"
TRACK_SECTION_TYPE = "tratUsek"

SWITCH_START_TYPE = "start"


PARSER_DESCRIPTION = """
Find path between start and stop sections.
This script will print list of sections IDs and list of switch sections IDs 
with their states ("S+" state means direct direction, "S-" is a branch).

E.g. ["1", "2", "3"], [("4", "S+"), ("5", "S-")
"""


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

        if block["type"] in (SECTION_TYPE, TRACK_SECTION_TYPE):
            sections_path.append(item_id)
        elif block["type"] == SWITCH_TYPE:
            if str(path[i + 1]) not in block["relations"]:
                raise Exception(
                    "Incorrect data in block {} about related blocks: "
                    "{}. Next block for current way is {}".format(
                        item_id, block, path[i + 1]
                    )
                )
            switch_state = block["relations"][str(path[i + 1])]
            if switch_state == SWITCH_START_TYPE:
                switch_state = block["relations"][str(path[i - 1])]
            if isinstance(switch_state, dict):
                # {
                #     "500": "start",
                #     "529": {
                #         "520": "S+",
                #         "524": "S-"
                #     }
                # }
                # due to a situation of uncertainty like on the example above
                #  we must check one more element
                try:
                    switch_state = switch_state[str(path[i - 2])]
                except KeyError:
                    switch_state = switch_state[str(path[i + 2])]

            switch_list.append((item_id, switch_state))

    return sections_path, switch_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=PARSER_DESCRIPTION)
    parser.add_argument('--start', required=True, help="Start path section")
    parser.add_argument('--end', required=True, help="End path section")
    args = parser.parse_args()

    with open("vztahy.json") as fp:
        data = json.load(fp)

    graph = build_topology_graph(data["relations"])
    print(*find_path(graph, args.start, args.end, data["data"]), sep="\n")
