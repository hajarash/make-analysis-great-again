from .constants import NodeType


class Node:
    def __init__(self, type: NodeType, name: str):
        self.type = type
        self.name = name

    def __str__(self):
        return str(self.type) + ' ' + self.name

    @classmethod
    def get_node_by_name(cls, nodes, search_name):
        li = list(filter(lambda node: node.name == search_name, nodes))
        if len(li) == 1:
            return li[0]
        return None

class Edge:

    def __init__(self, src: Node, dst: Node, weight:int):
        self.src = src
        self.dst = dst
        self.weight = weight


