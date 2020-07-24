"""
Information about graph nodes was stored in the tspan elements, which are
parts of topology blocks labels.

Every such tspan element (by design) must have the next structure:
    <tspan type="usek" relations="[1, 2, 3]" additional-data="{}" ...>
where:
    type - [vyhybka|usek|tratUsek] - block type
    relations - list[int] - list of incident block IDs of the graph
    additional-data - dict - more details about blocks (here is an example
    for "vyhybka" type:
        {
            "120": "start",
            "150": "S+",
            "158": "S-"
        }
"""
import os
import json
from xml.dom import minidom

TOPOLOGY_FILENAME = "kolejiste.svg"
RELATIONS_FILENAME = 'vztahy.json'

SWITCH_TYPE = "vyhybka"
SECTION_TYPE = "usek"

RELATIONS_KEY = "relations"
ADDITIONAL_DATA_KEY = 'additional-data'


def get_block_id(node):
    try:
        return int(node.childNodes[0].data)
    except ValueError:
        raise ValueError("Block {} has incorrect structure".format(str(node)))


def convert_svg_to_dict():
    """Extract graph information from the topology in SVG format

    """

    def _convert_block_data(node):
        relations = list(map(str, json.loads(node.getAttribute(RELATIONS_KEY))))
        data = {
            "type": node.getAttribute('type'),
            **eval(node.getAttribute(ADDITIONAL_DATA_KEY)),
        }

        return relations, data

    doc = minidom.parse(TOPOLOGY_FILENAME)
    relations, additional_data = {}, {}

    for node in doc.getElementsByTagName("tspan"):
        if not node.hasAttribute(RELATIONS_KEY):
            continue

        b_id = get_block_id(node)
        relations[b_id], additional_data[b_id] = _convert_block_data(node)

    topology = {
        "relations": relations,
        "data": additional_data,
    }

    with open(RELATIONS_FILENAME, 'w') as fp:
        json.dump(topology, fp, indent=4)


def update_svg_from_dict():
    """Store information from the saved JSON file in the SVG-topology

    """
    doc = minidom.parse(TOPOLOGY_FILENAME)
    with open(RELATIONS_FILENAME) as fp:
        content = json.load(fp)
        relations, data = content["relations"], content["data"]

    for node in doc.getElementsByTagName("tspan"):
        if not node.hasAttribute(RELATIONS_KEY):
            continue

        b_id = str(get_block_id(node))
        node.setAttribute("type", data[b_id]["type"])
        node.setAttribute(RELATIONS_KEY, str(list(map(int, relations[b_id]))))
        node.setAttribute(ADDITIONAL_DATA_KEY, str({
            k: v for k, v in data[b_id].items() if k != "type"
        }))

    with open(TOPOLOGY_FILENAME, "w") as fp:
        doc.writexml(fp, indent="   ")


def test_conversions():
    """Make test conversion to topology in SVG format into JSON and vice versa

    """
    global RELATIONS_FILENAME

    convert_svg_to_dict()

    original_relations_filename = RELATIONS_FILENAME
    update_svg_from_dict()

    RELATIONS_FILENAME = "vztahy1.json"
    convert_svg_to_dict()

    with open(original_relations_filename) as fp:
        data1 = json.load(fp)

    with open(RELATIONS_FILENAME) as fp:
        data2 = json.load(fp)

    assert data1 == data2

    os.remove(RELATIONS_FILENAME)


if __name__ == '__main__':
    convert_svg_to_dict()
    # update_svg_from_dict()
    # test_conversations()
