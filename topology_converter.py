import json
from pprint import pprint
from xml.dom import minidom

TOPOLOGY_FILENAME = "topology.svg"


def main():
    doc = minidom.parse(TOPOLOGY_FILENAME)

    data = {
        int(node.childNodes[0].data): json.loads(
            node.getAttribute('relations')
        )
        for node in doc.getElementsByTagName("tspan")
        if node.hasAttribute('relations')
    }

    pprint(data)
    with open('vztahy.json', 'w') as fp:
        json.dump(data, fp, indent=4)


if __name__ == '__main__':
    main()
