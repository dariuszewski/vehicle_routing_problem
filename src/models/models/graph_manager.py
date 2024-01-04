# from graph_builder import GraphBuilder
from node import NodeList
from graph import GraphList

class GraphManager():
    """
    A composite of nodes and edges.
    """
    def __init__(self, file_path, num_vehicles, capacity) -> None:
        self.nodes = NodeList.from_flie(file_path)
        self.graphs = GraphList.from_nodes(self.nodes)
        # self.routes = EdgeList.from_nodes(self.nodes)
    
    @property
    def distance_covered(self):
        return sum([graph.length for graph in self.graphs])
    
    def get_node_by_name(self, node_name):
        for node in self.nodes:
            if node.name == node_name:
                return node
        
    def get_graph_by_node(self, node):
        for graph in self.graphs:
            if node in graph:
                return graph

    def swap_nodes(self, node1, node2):
        if node1 == node2:
            print('same node error')
            return 
        graph1 = self.get_graph_by_node(node1)
        graph2 = self.get_graph_by_node(node2)
        if graph1 == graph2:
            graph2 = graph1  
        node1.prev.next, node2.prev.next = node2.prev.next, node1.prev.next 
        node1.next.prev, node2.next.prev = node2.next.prev, node1.next.prev
        node1.next, node2.next = node2.next, node1.next
        node1.prev, node2.prev = node2.prev, node1.prev

    def exchange_edges(self, node1, node2):
        
        print(node1)
        print(node2)
        # Check if same node wasn't provided twice.
        if node1 == node2:
            print('same node error')
            return 
        # Check if same graph wasn't provided once
        graph1 = self.get_graph_by_node(node1)
        graph2 = self.get_graph_by_node(node2)
        print('graphs:', str(graph1), str(graph2))
        if graph1 == graph2:
            graph2 = graph1
            graph1.swap_nodes(node1, node2)
            return
        # Logic for 2 different graphs
        node1.next.prev, node2.next.prev = node2.next.prev, node1.next.prev
        node1.next, node2.next = node2.next, node1.next

        new_graph_list = graph1.split()
        self.graphs.remove(graph1)
        for graph in new_graph_list:
            self.graphs.append(graph)           
        new_graph_list = graph2.split()
        self.graphs.remove(graph2)
        for graph in new_graph_list:
            self.graphs.append(graph)
        
        
    def get_route_by_node(self, node_name):
        for route in self.routes:
            for edge in route:
                if node_name in edge:
                    return route 
    

if __name__ == '__main__':
    graph = GraphManager('./temp/orders_with_depots.csv', 5, 1000) # nodes
    # print(data)
    example_node = graph.get_node_by_name('Kraków') # node
    # print(example_node)
    graphs = graph.graphs # routes
    # print(graphs)
    # print(len(graphs))
    # print(graphs[0].length)
    node1 = graph.get_node_by_name('Gdynia')
    node2 = graph.get_node_by_name('Białystok')
    graph.exchange_edges(node1, node2)
    # print()
    # print(graphs)
    # print(len(graphs))


    # # print(edge1); print(edge2)
    # route1 = graph.get_route_by_node('Gdynia') # you can get a route by node name
    # route2 = graph.get_route_by_node('Malbork')
    # print(route1); print(route2)
    # graph.exchange_edges('Gdynia', 'Malbork')
    # new_r_1 = graph.get_route_by_node('Gdynia')