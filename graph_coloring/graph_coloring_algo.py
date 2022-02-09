from graph_coloring import graph_coloring_ds as gcds
import random
import matplotlib.pyplot as plt
from collections import OrderedDict
from typing import tuple

def plot_group(schedule_group: OrderedDict) -> None:
    """
    Bar Graph of the group created
    """
    
    fig = plt.figure(figsize=(7, 7))
    axes = fig.add_subplot(111)
    axes.bar(schedule_group.keys(), schedule_group.values())
    axes.set_xlabel('Group')
    axes.set_ylabel('Count')
    axes.set_title('group counts')
    plt.show();

def solution() -> tuple[dict, int]:
    """
    Run the constructive heuristics Algorithm
    """

    ans = dict()

    nodes = input().split(',')
    connections = [input() for _ in range(int(input()))]

    for _ in range(100):
        # list of color to pick from
        random_list = [
            'green', 'rainbow', 'red', 'blue', 'yellow', 'black', 
            'white', 'brown', 'peach', 'indigoes', 'purple', 'grey'
        ]

        used_colors = set()
        nodes_col = {sub.strip(): gcds.Node(sub.strip()) for sub in nodes}
        for con in connections:
            temp = {nodes_col[s.strip()] for s in con.split(',')}
            for s in [t.data for t in temp]:
                nodes_col[s].add_connected_nodes(temp.copy())

        while sum([1 for n in nodes_col.values() if n.color is not None]) != len(nodes_col):
            i = random.randint(0, len([1 for n in nodes_col.values() if not n.color]) - 1)
            tmp = [val for val in nodes_col.values() if not val.color]
            selNode = tmp[i]

            connCol = {node.color for node in selNode.connected_nodes if node.color}
            diffCol = used_colors.difference(connCol)

            if diffCol:
                col = diffCol.pop()
                used_colors.add(col)
                selNode.color = col
            else:
                col = random_list[random.randint(0, len(random_list) - 1)]
                used_colors.add(col)
                selNode.color = col
                random_list.remove(col)

        len_colors = len({n.color for n in nodes_col.values()})
        if len_colors in ans.keys():
            continue
        else:
            ans[len_colors] = {k: n.color for k, n in nodes_col.items()}

    best = min(ans.keys())
    chosen = ans[best]

    schedule_group = OrderedDict()
    for k, v in chosen.items():
        if v in schedule_group.keys():
            schedule_group[v] += 1
        else:
            schedule_group[v] = 1

    plot_group(schedule_group)

    return chosen, best