from xml.dom.minicompat import NodeList
from Utils import graph
from collections import OrderedDict
from typing import Tuple
import numpy as np
import random
import copy


class Constructive_Heuristics(object):
    """
    Constructive Heuristics to schedule a timetable
    """

    def __init__(self, nodes, edges, pick_random=True):
        super().__init__()
        self.nodes = nodes
        self.edges = edges 
        self.pick_random = pick_random
        self.best_solution_stud = None 
        self.best_solution_pans = None
        self.best_cost = None

    def cost(self, schedule: dict) -> list:
        """
        Get the cost of the given solution
        """

        # initialized cost
        cost_list = [0] * 18

        # initalized for penalty 3 prob
        group_sch = {}
        for sch in schedule.items():
            if sch[1].color_class in group_sch.keys():
                group_sch[sch[1].color_class].append(sch[1])
            else:
                group_sch[sch[1].color_class] = [sch[1]]
        
        # initalized for penalty 2 prob
        group_pan = {}
        for sch in schedule.items():
            temp = {sch[1].supervisor}
            for pan in sch[1].panels:
                temp.add(pan)
            for pan in temp:
                if pan in group_pan.keys():
                    group_pan[pan].append(sch[1])
                else:
                    group_pan[pan] = [sch[1]]

        # get the cost for penalty 3
        for sch in schedule.items():
            if sch[1].color == None:
                continue

            cost = 0
            # penalty 3
            temp = set()
            for neigh in group_sch[sch[1].color_class]:
                temp = temp.union(set(neigh.panels))
            if sch[1].supervisor in temp:
                cost += 3
            # penalty 2
            temp = {sch[1].supervisor}
            for pan in sch[1].panels:
                temp.add(pan)
            for pan in temp:
                index_sch = np.array([t.color for t in group_pan[pan] if t.color])
                index_sch = index_sch % 9
                if (0 in index_sch and 2 in index_sch) or \
                    (3 in index_sch and 5 in index_sch) or \
                        (6 in index_sch and 8 in index_sch):
                    cost += 2
            # penalty 1
            temp = {sch[1].supervisor}
            for pan in sch[1].panels:
                temp.add(pan)
            for pan in temp:
                index_sch = np.array([t.color for t in group_pan[pan] if t.color])
                index_sch = index_sch % 9
                tmp_count = index_sch // 3
                if len(tmp_count) == len(set(tmp_count)):
                    cost += 1

            cost_list[sch[1].color] = cost

        return cost_list       

    def roulette_wheel_selection(self, avai_class: set, schedule: dict, node: graph.Node, slots_init: dict) -> int:
        """
        Pick a class using Probability effected by the cost incurred
        """

        # setup the class
        avai_class = list(avai_class)

        # set default value for the roulette
        roulette = [0] * len(avai_class)
        for i, cl in enumerate(avai_class):
            tmp_schedule = copy.deepcopy(schedule)
            tmp_schedule[node.label].set_color(cl, slots_init[cl])

            # get the cost incurred
            inc_cost = sum(self.cost(tmp_schedule))

            # assign the cost 
            roulette[i] = inc_cost
        
        # get the effected cost and create probability
        max_cost = max(roulette) + 0.001
        roulette = [max_cost - rou for rou in roulette]
        tot_cost = sum(roulette)
        probs = [rou/tot_cost for rou in roulette]

        return avai_class[np.random.choice(len(avai_class), p=probs)]
        

    def solution(self) -> Tuple[dict, int]:
        """
        Run the constructive heuristics Algorithm using Largest degree heuristics 
        """

        nodes = self.nodes
        edges = self.edges

        # list of schedule to pick from
        slots_init = {
            0: 'D1 S1', 1: 'D1 S2', 2: 'D1 S3', 3: 'D2 S1', 4: 'D2 S2', 5: 'D2 S3', 6: 'D3 S1', 7: 'D3 S2', 8: 'D3 S3', 
            9: 'D1 S1', 10: 'D1 S2', 11: 'D1 S3', 12: 'D2 S1', 13: 'D2 S2', 14: 'D2 S3', 15: 'D3 S1', 16: 'D3 S2', 17: 'D3 S3'
        }
        
        # maintain set of avai class
        avai_colors = set(slots_init.keys())

        # initialized the graph node
        nodes_col = {props[0]: graph.Node(props[0], props[1], props[2].split(',')) 
            for props in nodes}
        for con in edges:
            node1, node2 = [t.strip() for t in con.split(',')]
            nodes_col[node1].add_connected_nodes(nodes_col[node2])
            nodes_col[node2].add_connected_nodes(nodes_col[node1])

        # order the nodes for largest degree heuristics implementation
        ordered_nodes = [[k, len(v.connected_nodes)] for k, v in nodes_col.items()]
        ordered_nodes.sort(key=lambda x: x[1])
        
        # run loops until all node have color
        while len(ordered_nodes):
            # pick vertex with the highest conflicted edges
            tmp = ordered_nodes.pop()
            selNode = nodes_col[tmp[0]]

            # get the lists of color that yet to be used and not match with neighbors
            connCol = {node.color for node in selNode.connected_nodes if node.color}
            diffCol = avai_colors.difference(connCol)

            # pick class
            if self.pick_random:
                col = np.random.choice(list(diffCol), 1)[0]
            else:
                col = self.roulette_wheel_selection(diffCol, nodes_col, selNode, slots_init)
            
            avai_colors.remove(col)
            selNode.set_color(col, slots_init[col])

        # get the result
        optimal_sol_stud = {k: v.color_class for k, v in nodes_col.items()}
        optimal_sol_pans = {}
        for stud in nodes_col.values():
            for pan in stud.panels:
                if pan in optimal_sol_pans.keys():
                    optimal_sol_pans[pan].append(stud.color_class)
                else:
                    optimal_sol_pans[pan] = [stud.color_class]
        optimal_cost = sum(self.cost(nodes_col))

        # save the better result
        if not self.best_cost or self.best_cost > optimal_cost:
            self.best_solution_stud = optimal_sol_stud
            self.best_solution_pans = optimal_sol_pans
            self.best_cost = optimal_cost
            
        # return the result
        return optimal_sol_stud, optimal_sol_pans, optimal_cost

    def sampling_result(self, n=100) -> Tuple[list, int, list]:
        """
        Get the mean and best result by the given count
        """

        results = []
        for _ in range(n):
            result = self.solution()
            results.append(result[2])

        return self.best_solution_stud, self.best_solution_pans, self.best_cost, results


