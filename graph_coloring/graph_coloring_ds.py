
class Node(object):
    def __init__(self, data):
        self.data = data
        self.connected_nodes = set()
        self.color = None

    def add_connected_nodes(self, node_set):
        if not isinstance(node_set, set):
            raise Exception("Not a set class")

        node_set.discard(self.data)
        self.connected_nodes = self.connected_nodes.union(
            node_set
        )

    def set_color(self, color):
        self.color = color

