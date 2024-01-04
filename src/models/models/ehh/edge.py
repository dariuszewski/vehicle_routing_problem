# from decimal import Decimal
# from math import radians, sin, cos, asin, sqrt
# from itertools import pairwise
# from typing import Any, List
# from node import Node, NodeList
# from iterable import Iterable

# def haversine(lon1, lat1, lon2, lat2):
#     # Convert decimal degrees to radians
#     lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

#     # Haversine formula
#     dlon = lon2 - lon1
#     dlat = lat2 - lat1
#     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
#     c = 2 * asin(sqrt(a))
#     r = 6371 # Radius of Earth in kilometers
#     return c * r


# class Edge:
#     def __init__(self, start: Node, end: Node) -> None:
#         """
#         An Edge representing 2 connected nodes.
#         Args:
#             start    : Start node.
#             end      : End node.
#         """
#         self.start = start
#         self.end = end

#     @property
#     def length(self):
#         """
#         The length of the node in kilometers. 
#         Calculated using haversine formula.
#         """
#         dist = haversine(
#             self.start.lon, self.start.lat, self.end.lon, self.end.lat
#             )
#         return round(dist, 2)
    
#     def __contains__(self, node_name):
#         if self.start.name == node_name or self.end.name == node_name:
#             return True
#         return False
    
#     def __str__(self) -> str:
#         return f"{str(self.start)} -({self.length})> {str(self.end)})"

#     def __repr__(self) -> str:
#         return f"<Edge {str(self.start)} -({self.length})> {str(self.end)}>"
    

# class EdgeList(Iterable):
#     def __init__(self, items: List[Any] = []):
#         super().__init__(items)
    
#     @classmethod
#     def from_nodes(cls, nodes):
#         non_depots = [node for node in nodes if not node.is_depot]
#         edges = [Edge(start, end) for start, end in pairwise(non_depots)]
#         return cls(edges)

# class Vehicle:
#     def __init__(self, capacity) -> None:
#         self.capacity = capacity

# class Graph():
#     def __init__(self, start: Node, max_cap: int) -> None:
#         self.start = start
#         self.max_cap = max_cap
    
#     @property
#     def last(self):
#         current_node = self.start
#         while current_node.next:
#             current_node = current_node.next
#         return current_node

#     @property
#     def weight(self):
#         weight = 0
#         current_node = self.start
#         while current_node.next:
#             current_node = current_node.next
#             weight += current_node.weight
#         return weight
    
#     def __repr__(self) -> str:
#         string = ""
#         current_node = self.start
#         while current_node.next:
#             string = string + current_node + ' -> '
#             current_node = current_node.next
#         string = string + current_node
#         return string

# class GraphList(Iterable):
#     def __init__(self, items: List[Any] = []):
#         super().__init__(items)

#     @classmethod
#     def from_nodes(cls, all_nodes):
#         nodes = [node for node in all_nodes if not node.is_depot]
#         depot = all_nodes.get_closest_depot(nodes[0])
#         graphs = []
#         cur_graph = Graph(start=depot, max_cap=1000)
#         i = 0
#         # for i in range(len(nodes)-1):
#         while i < len(nodes)-1:
#             print(i)
#             while cur_graph.weight + nodes[i].weight <= cur_graph.max_cap:
#                 nodes[i].prev = cur_graph.last
#                 cur_graph.last.next = nodes[i]
#                 i += 1
#             cur_graph.last.next = depot
#             graphs.append(cur_graph)
#             cur_graph = Graph(start=depot, max_cap=1000)
#         print(graphs)
#         cls(graphs)
                
            




    

# class RouteList(Iterable):
#     def __init__(self, items: List[Any] = []):
#         super().__init__(items)
        
#     @staticmethod
#     def create_edges(nodes, capacity, num_vehicles):
#         """
#         This method ensures that the edges are split into minimum of 
#         num_vehicles groups.
#         Args:
#             Default args are a ready TSP problem
#         """
#         vehicles = [[] for _ in range(num_vehicles)]
#         cur_veh_idx = 0
#         for item in nodes:
#             vehicle = vehicles[cur_veh_idx]
#             if item.is_depot:
#                 continue
#             elif not vehicle:
#                 vehicle.append([item])
#             else:
#                 edge_cap = sum([n.weight for n in vehicle[-1]]) + item.weight
#                 if edge_cap <= capacity:
#                     vehicle[-1].append(item)
#                 else:
#                     vehicle.append([item])
#             if cur_veh_idx < num_vehicles-1:
#                 cur_veh_idx += 1
#             else:
#                 cur_veh_idx = 0
#         result = [item for sublist in vehicles for item in sublist]
#         return result
    
#     @classmethod
#     def from_nodes(cls, nodes, capacity=Decimal("Infinity"), vehicles=1):
#         """
#         List of routes. Minimum of vechicles.
#         """
#         raw_edges = RouteList.create_edges(nodes, capacity, vehicles)
#         real_edges = []
#         for edge_list in raw_edges:
#             start = nodes.get_closest_depot(edge_list[0])
#             end = nodes.get_closest_depot(edge_list[-1])
#             edge_list_with_depots = [start, *edge_list, end]
#             edges = [Edge(start, end) for start, end in pairwise(edge_list_with_depots)]
#             real_edges.append(edges)
#         return cls(real_edges)