class Node(object):
    """
    Node class for Vertex presentation
    """

    def __init__(self, label: str, sv: str, panels: list):
        super().__init__()
        self.label = label
        self.connected_nodes = set()
        self.supervisor = sv
        self.panels = panels
        self.color = None
        self.color_class = None

    def add_connected_nodes(self, node) -> None:
        if not isinstance(node, Node):
            raise Exception("Not a Node class")

        self.connected_nodes.add(node)

    def __len__(self) -> int:
        return len(self.connected_nodes)

    def set_color(self, color: str, color_class: str) -> None:
        self.color = color
        self.color_class = color_class

