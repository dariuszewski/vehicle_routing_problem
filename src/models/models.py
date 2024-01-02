# Amazingly enough, this is bin-packaging problem!
# MAIN MAIN MAIN
import csv 
import itertools
import random
import decimal
from utils.haversine import haversine

class Node:
    def __init__(self, name, lat, lon, weight, is_depot) -> None:
        self.name = name
        self.lat = lat
        self.lon = lon
        self.weight = weight
        self.is_depot = is_depot

    def __repr__(self):
        is_depot = '-Depot' if self.is_depot else '' 
        return f'<Node{is_depot} {self.name}, w: {self.weight}>'
    
    def __str__(self) -> str:
        return f"{self.name} ({self.weight})"

class Edge:
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end
    @property
    def length(self):
        return haversine(self.start.lon, self.start.lat, self.end.lon, 
                         self.end.lat)
    @property
    def weight(self):
        return self.start.weight + self.end.weight
    
    def __contains__(self, node_name):
        if self.start.name == node_name or self.end.name == node_name:
            return True
        return False
    
    def __str__(self) -> str:
        return f"{str(self.start)} -> {str(self.end)} ({self.length})"

    def __repr__(self) -> str:
        # start = self.start.name
        # end = self.end.name if self.end else None
        # return f"{str(self.start)} -> {str(end)} ({self.length})"
        return f"{str(self.start)} -> {str(self.end)} ({self.length})"
    
class Graph:
    def __init__(self, items) -> None:
        self._items = items
    
    @classmethod
    def from_edges(cls, edges):
        graph = [edge.start for edge in edges]
        return cls(graph)


class Route:
    def __init__(self, items = []) -> None:
        self._items = items
    
    def length(self):
        result = 0
        for i in range(0, len(self._items), 2):
            result += self._items[i].length
        return result

    def weight(self):
        return sum([item.start.weight for item in self._items])
    
    def exchange_edges(self):
        """
        Basically, i not only need to replace the edges if i keep edged as they are
        I need to change the previous edge end and the next edge end.
        Makes a bit no sense. The pairwise looks nice but it is not really useful. 

        Question is: should i keep edges as they are with parwise, or make them separate.
        """
        city1 = 'Gdynia'
        city2 = 'Malbork'

    def get_edges_by_node(self, node_name):
        edges = []
        for edge in self._items:
            if node_name in edge:
                edges.append(edge)
        return edges

    def __str__(self):
        result = ''
        for i in range(0, len(self._items), 2):
            if not result:
                result += f'{self._items[i].start} -> {self._items[i].end}'
            else: 
                result += f' -> {str(self._items[i].start)} -> {self._items[i].end}'
        return result        


class NodeFactory:
    def __init__(self, items = None) -> None:
        self._items = items
    
    @classmethod
    def from_flie(cls, file_path):
        nodes = []
        with open(file_path, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                node = Node(
                    name=row['city'],
                    weight=int(row['order']),
                    lat=float(row['latitude']),
                    lon=float(row['longitude']), 
                    is_depot=(True if row['is_depot'] == 'True' else False)
                )
                nodes.append(node)
        return cls(nodes)
    
    def get_node_by_name(self, node_name):
        for item in self._items:
            if item.name == node_name:
                return item
    
    def __str__(self) -> str:
        return ('\n').join([str(item) for item in self._items])

    def create_min_edges(self, capacity=decimal.Decimal("Infinity"), num_vehicles=1):
        # num_vehicles is actually min_routes
        vehicles = [[] for _ in range(num_vehicles)]
        cur_veh_idx = 0
        for item in self._items:
            vehicle = vehicles[cur_veh_idx]
            if item.is_depot:
                continue
            elif not vehicle:
                vehicle.append([item])
            else:
                edge_cap = sum([n.weight for n in vehicle[-1]]) + item.weight
                if edge_cap <= capacity:
                    vehicle[-1].append(item)
                else:
                    vehicle.append([item])
            if cur_veh_idx < num_vehicles-1:
                cur_veh_idx += 1
            else:
                cur_veh_idx = 0
        result = [item for sublist in vehicles for item in sublist]
        return result

    def create_edges(self, capacity, vehicles):
        # this needs vehicle constraint
        if vehicles:
            return self.create_min_edges(capacity, vehicles)
        edges = []
        edge = []
        for item in self._items:
            if item.is_depot:
                continue
            elif not edge:
                edge.append(item)
            else:
                edge_cap = sum([item.weight for item in edge]) + item.weight
                if edge_cap <= capacity:
                    edge.append(item)
                else:
                    edges.append(edge)
                    edge = [item]
        return edges

    def build_edges(self, capacity=decimal.Decimal("Infinity"), vehicles=1):
        raw_edges = self.create_edges(capacity, vehicles)
        real_edges = []
        for edge_list in raw_edges:
            edge_list_with_depots = [self.get_depot(), *edge_list, self.get_depot()]
            edges = [Edge(start, end) for start, end in itertools.pairwise(edge_list_with_depots)]
            real_edges.append(edges)
        return real_edges
    
    def get_route_by_node_name(self, node_name):
        for edge in self._items:
            if node_name in edge:
                return edge
                    
    def get_depot(self):
        for item in self._items:
            if item.is_depot:
                return item

class EdgeFactory:
    def __init__(self, items = []) -> None:
        self._items = items

    @classmethod
    def from_nodes(cls, nodes):
        non_depots = [node for node in nodes if not node.is_depot]
        raw = itertools.pairwise(non_depots)
        edges = [Edge(start, end) for start, end in raw]
        return edges

class GraphManager():
    def __init__(self, items, nodes) -> None:
        self._items = items
        self.nodes = nodes

    def get_edges_by_node(self, node):
        edges = []
        for route in self._items:
            for edge in route:
                if node in edge:
                    edges.append(edge)
        return edges 
    
    def exchange_edges(self, node_name1, node_name2):
        """
        need to check capacity
        """
        node1 = self.nodes.get_node_by_name(node_name1)
        node2 = self.nodes.get_node_by_name(node_name2)

        r1 = self.get_route_by_node(node_name=node_name1)
        r1_weight = sum(item.start.weight for item in r1)
        new_r1_weight = r1_weight - node1.weight + node2.weight
        r2 = self.get_route_by_node(node_name=node_name2)
        r2_weight = sum(item.start.weight for item in r2)
        new_r2_weight = r2_weight - node2.weight + node1.weight
        
        if new_r1_weight <= 1000 and new_r2_weight <= 1000:

            end1, start1 = self.get_edges_by_node(node1.name)
            end2, start2 = self.get_edges_by_node(node2.name)

            end1.end, start1.start = node2, node2
            end2.end, start2.start = node1, node1
        
        else:
            'Failed'
        
    def get_route_by_node(self, node_name):
        for route in self._items:
            for edge in route:
                if node_name in edge:
                    return route 

    
    def __str__(self) -> str:
        return f'Graph with {len(self._items)} routes'

if __name__ == '__main__':
    data = NodeFactory.from_flie('./temp/orders_with_depots.csv') # nodes
    # print(data)
    example_node = data.get_node_by_name('Kraków') # node
    # print(example_node)
    raw_edges = data.build_edges(1000, 10) # these are semi-random routes
    # print(raw_edges)
    graph = GraphManager(raw_edges, data) # graph state (fleet)
    # print(graph)

    edge1 = graph.get_edges_by_node('Gdynia') # you can get a specific pair of edges by node name
    edge2 = graph.get_edges_by_node('Malbork') # you can get a specific pair of edges by node name
    # print(edge1); print(edge2)
    route1 = graph.get_route_by_node('Gdynia') # you can get a route by node name
    route2 = graph.get_route_by_node('Malbork')
    print(route1); print(route2)
    graph.exchange_edges('Gdynia', 'Malbork')
    new_r_1 = graph.get_route_by_node('Gdynia')
    print()
    print(new_r_1)
    # for edge in raw_edges:
    #     print(edge)
    #     print()
    # first = raw_edges[0]
    # routes = [Route(item) for item in raw_edges]
    # r1 = routes[1]
    # r2 = routes[2]
    # print(r1)
    # print(r2)
    # city1 = 'Gdynia'
    # city2 = 'Malbork'

    # edges = r1.get_edges_by_node(city1)
    # print(edges)

    # ga = GraphManager(edges)
    # nodes = data._items
    # edges = EdgeFactory.from_nodes(nodes)
    # for edge in edges:
    #     print(edge)
    # graph = Graph.from_edges(edges)
    # print(len(graph._items))