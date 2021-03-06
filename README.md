# rkd-topology

This repository contains helpful functions to support topology and find paths
 between different parts of this topology.

![topology](./kolejiste.svg)

## Introduction

To find a path from A block to B block we build a graph. Nodes of this graph contains blocks of three types:
 - usek;
 - tratUsek;
 - vyhybka.

We manipulate 2 files - kolejiste.svg and vztahy.json.

kolejiste.svg is a SVG-visualization of all presented sections for now. From 
kolejiste.svg we can get vztahy.json which is a special file to have 
relationships between all sections. It has the next structure:

```json
{
    "relations": {
        "1": [
            "2",
            "3"
        ]
    },
    "data": {
        "1": {
            "type": "usek"
        },
        "3": {
            "type": "tratUsek"
        },
        "2": {
            "type": "vyhybka",
            "relations": {
                "3": "start",
                "4": "S+",
                "5": "S-"
            }
        },
        "7": {
            "type": "vyhybka",
            "relations": {
                "10": "start",
                "11": {
                    "12": "S+",
                    "13": "S-"
                }
            }
        }
    }
}
```

"relations" key contains section-neighbors to build a graph, "data" - details
about every section. For now, blocks with type "vyhybka" have "relations" 
part, where placed nodes of three types:
- start (input block)
- S+ (direct)
- S- (branch)

kolejiste.svg has the same data as vztahy.json, but stores it in another way.
Every section has text label and information about it are placed as 
attributes of this label tspan tag. Every such tspan element (by design) 
must have the next structure:
 
```xml
<tspan additional-data="{'relations': {'315': 'start', '311': 'S+', '316': 
'S-'}}" id="..." relations="[315, 316, 311]" style="..." type="vyhybka"
x="..." y="...">302</tspan>    
```

## Scripts

### Convert data between kolejiste.svg and vztahy.json 
 
You need to use `topology_converter.py` in the next cases:
 - generate vztahy.json from kolejiste.svg;
 - update kolejiste.svg from vztahy.json, where you did some updates.
 
 ```text
$ python topology_converter.py --help

usage: topology_converter.py [-h] [--to-json] [--to-svg]

It's a script to convert data between topology file and relations file.

optional arguments:
  -h, --help  show this help message and exit
  --to-json   Extract data from SVG file to JSON
  --to-svg    Extract data from JSON file to SVG
```

### Find path from section A to section B

To do it you need to use topology.py:

```text
$ python topology.py --help

usage: topology.py [-h] --start START --end END [--show-graph]

Find path between start and stop sections. This script will print list of
sections IDs and list of switch sections IDs with their states ("S+" state
means direct direction, "S-" is a branch). E.g. ["1", "2", "3"], [("4", "S+"),
("5", "S-")

optional arguments:
  -h, --help     show this help message and exit
  --start START  Start path section
  --end END      End path section
  --show-graph   Show built graph for debugging purposes

```

### Check built graph visually

Sometimes will be faster to check the built graph visually for issue fixing. You 
need to add --show-graph parameter to do it. Pay attention that before this you 
need to install matplotlib dependency.

```text
$ python topology.py --start 521 --end 534 --show-graph
```
 

### Complex cases explanation

#### 1. Section "Okh UV1-2 529"

![topology](images/case_529.png)

It's an example of a section that contains 2 parts (were colored as red). In 
this case we have other structure for details of the 501 section as below. 
Since we have the same block for both branches, we make a nested block. In 
the topology.py was added the additional check for such nested structure.

```text
# file vztahy.json

"501": {
    "type": "vyhybka",
    "relations": {
        "500": "start",
        "529": {
            "520": "S+",
            "524": "S-"
        }
    }
},
```

#### 2. Section "Okh UV5-6 318"

![topology](images/case_318.png)

In the case of section "Okh UV5-6 318" we ignore part from the right side of 
section "Ku V6 305" in vztahy.json to save consistency of final results.

#### 3. Section "Ku UVA 319"

![topology](images/case_319.png)

In the case of section "Okh UV5-6 318" we ignore part from the right side of 
section "Ku VA 306" in vztahy.json to save consistency of final results.

#### 3. Section "Okh UV3-4-5 530"

![topology](images/case_530.png)

In the case of section "Okh UV3-4-5 530" we ignore part from the left side of 
section "Okh V3 502" and the right side of section "Okh V5 504" in vztahy.json
 to save consistency of final results.

#### 3. Section "Okh UV6-7 531"

![topology](images/case_531.png)

In the case of section "Okh UV6-7 531" we ignore part from the left side of 
section "Okh V6 505" and the right side of section "Okh V7 506" in vztahy.json
 to save consistency of final results.
