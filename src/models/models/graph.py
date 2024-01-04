from decimal import Decimal
from math import radians, sin, cos, asin, sqrt
from itertools import pairwise
from typing import Any, List
from node import Node, NodeList
from iterable import Iterable
import copy

from utils import haversine

class Graph():
    def __init__(self, start: Node, max_cap: int) -> None:
        self.start = start
        self.max_cap = max_cap
        self.vehicle = None
    
    @property
    def last(self):
        current_node = self.start
        while current_node.next:
            current_node = current_node.next
        return current_node

    @property
    def length(self):
        length = 0
        current_node = self.start
        while current_node.next:
            lon1 = current_node.lon
            lat1 = current_node.lat
            lon2 = current_node.next.lon
            lat2 = current_node.next.lat
            length += haversine(lon1, lat1, lon2, lat2)
            current_node = current_node.next
        return round(length, 2)

    @property
    def weight(self):
        weight = 0
        current_node = self.start
        while current_node.next:
            current_node = current_node.next
            weight += current_node.weight
        return weight

    @property
    def is_empty(self):
        current_node = self.start
        while current_node.next:
            current_node = current_node.next
            if not current_node.is_depot:
                return False      
        return True
    
    def add_node(self, node):
        node.prev = self.last
        self.last.next = node
    
    def swap_nodes(self, node1, node2):
        """
        Bug: This may not change the order if node1 is after node2 in the list
        """
        node1.prev.next, node2.prev.next = node2.prev.next, node1.prev.next 
        node1.next.prev, node2.next.prev = node2.next.prev, node1.next.prev
        node1.next, node2.next = node2.next, node1.next
        node1.prev, node2.prev = node2.prev, node1.prev
    
    def split(self):     
        nodes = []
        current_node = self.start
        while current_node.next:
            nodes.append(current_node)
            next_node = current_node.next
            current_node.next, current_node.prev = None, None
            current_node = next_node
        if not current_node.is_depot:
            nodes.append(current_node)

        node_list = NodeList(nodes)
        graph_list = GraphList.from_nodes(node_list)
        return graph_list
    
    def to_list(self):
        nodes = []
        current_node = self.start
        while current_node.next:
            if not current_node.is_depot:
                nodes.append(current_node)
            next_node = current_node.next
            current_node.next, current_node.prev = None, None
            current_node = next_node
        if not current_node.is_depot:
            nodes.append(current_node)
        return nodes
    
    def __len__(self):
        length = 0
        current_node = self.start
        while current_node.next:
            if not current_node.is_depot:
                length += 1
            current_node = current_node.next
        return length

    def __contains__(self, node):
        if isinstance(node, Node):
            node_name = node.name
        else:
            node_name = node
        current_node = self.start
        while current_node.next:
            if current_node.name == node_name:
                return True
            else:
                current_node = current_node.next
        return False

    def __repr__(self) -> str:
        string = "<Graph "
        current_node = self.start
        while current_node.next:
            string = string + current_node.name + ' -> '
            current_node = current_node.next
        string = string + current_node.name + ' >'
        return string

    def __str__(self) -> str:
        string = "<Graph "
        current_node = self.start
        while current_node.next:
            string = string + current_node.name + ' -> '
            current_node = current_node.next
        string = string + current_node.name + ' >'
        return string

class GraphList(Iterable):
    def __init__(self, items: List[Any] = []):
        super().__init__(items)
    
    def get_all_non_depots(self):
        nodes = []
        for graph in self._items:
            for node in graph.to_list():
                if not node.is_depot:
                    nodes.append(node)
        return nodes

    @classmethod
    def from_nodes(cls, all_nodes):
        nodes = [node for node in all_nodes if not node.is_depot]
        print(len(nodes))
        depot = all_nodes.get_closest_depot(nodes[0])
        print(depot)
        graphs = []
        cur_graph = Graph(start=depot, max_cap=1000)
        i = 0
        while i < len(nodes)-1:
            if cur_graph.weight + nodes[i].weight <= cur_graph.max_cap:
                # Graph is capable of the new node
                cur_graph.add_node(nodes[i])
                i += 1
                print(cur_graph)
            else:
                # Graph is not capable of accepting the new node
                # 1. Close the graph
                new_depot = all_nodes.get_closest_depot(nodes[i])
                new_graph_start = copy.deepcopy(new_depot)
                cur_graph.add_node(new_depot)
                graphs.append(cur_graph)
                # 2. Open new graph
                cur_graph = Graph(start=new_graph_start, max_cap=1000)
                print(cur_graph)

        if cur_graph.weight + nodes[i].weight <= cur_graph.max_cap:
            # Last node, if cur_graph can accept
            new_depot = all_nodes.get_closest_depot(nodes[i])
            cur_graph.add_node(nodes[i])
            cur_graph.add_node(new_depot)
            graphs.append(cur_graph) 
            print(cur_graph)
        else:
            # Last node if new graph is needed.
            # 1. Prepare all needed depots
            new_depot = all_nodes.get_closest_depot(nodes[i-1])
            new_graph_start = copy.deepcopy(new_depot)
            new_graph_end = copy.deepcopy(new_depot)
            # 2. Close the old graph
            cur_graph.add_node(new_depot)
            graphs.append(cur_graph)
            print(cur_graph)
            # 3. Open a new graph, starting from the same depot
            cur_graph = Graph(start=new_graph_start, max_cap=1000)
            print(cur_graph)
            # 4. Add the node
            cur_graph.add_node(nodes[i])
            print(cur_graph)
            # 5. Close the new graph
            cur_graph.add_node(new_graph_end)
            print(cur_graph)
            graphs.append(cur_graph)
            
        return cls(graphs)
    
if __name__ == "__main__":
    # Load nodes from a file
    file_path = './temp/orders_with_depots.csv'  # Replace with your actual file path
    nodes_list = NodeList.from_flie(file_path)

    # Print all nodes
    print("All Nodes:")
    print(nodes_list)

    # Create a GraphList from nodes
    graph_list = GraphList.from_nodes(nodes_list)
    
    # Print each graph in the graph list
    print("\nGraphs Created:")
    for graph in graph_list:
        print(graph)

    # Check how many non-depots are in all graphs
    print('Non-Depots from graphs', str(len(graph_list.get_all_non_depots())))
    print('Non-Depots from nodes:', len([node for node in nodes_list if not node.is_depot]))

    # Demonstrate adding, swapping, and splitting nodes
    if len(graph_list) > 0:
        first_graph = graph_list[0]
        print(f"\nFirst Graph: {first_graph}")

        # Assuming nodes_list has more than two nodes for swapping
        if len(nodes_list) > 2:
            node1, node2 = nodes_list[0], nodes_list[1]
            print(f"\nSwapping nodes: {node1} and {node2}")
            first_graph.swap_nodes(node1, node2)
            print(f"Graph after swapping: {first_graph}")

        # Split the graph
        print("\nSplitting the first graph:")
        new_graph_list = first_graph.split()
        for new_graph in new_graph_list:
            print(new_graph)

