try:
    from src.algorithms.models.doubly_linked_list import DoublyLinkedList
    from src.algorithms.models.node import Node, NodeList
except:
    from models.doubly_linked_list import DoublyLinkedList
    from models.node import Node, NodeList

class GraphManager():
    def __init__(self, node_list, max_cap, vehicles) -> None:
        self.node_list = self.create_node_list(node_list)
        self.max_cap = max_cap
        self.vehicles = vehicles
        self.cycles = self.create_cycles()
        self.graphs = self.cycles

    @property
    def total_length(self):
        return  sum([cycle.length for cycle in self.cycles])
    

    def create_node_list(self, node_list):
        if isinstance(node_list, NodeList):
            return node_list
        else:
            return NodeList.from_flie(node_list)

    def create_cycles(self):
        non_depots = [node for node in self.node_list if not node.is_depot]
        result = []
        cycles = []
        cur_cycle = []
        for node in non_depots:
            cur_cycle_weight = sum([i.weight for i in cur_cycle])
            if self.max_cap >= cur_cycle_weight + node.weight:
                cur_cycle.append(node)
            else:
                cycles.append(cur_cycle)
                cur_cycle = []
                cur_cycle.append(node)
        if cur_cycle:
            cycles.append(cur_cycle)
        for cycle in cycles:
            start = self.node_list.get_closest_depot(cycle[0])
            end = self.node_list.get_closest_depot(cycle[-1])
            dll = DoublyLinkedList(head=start, max_cap=self.max_cap,
                                   node_list=self.node_list)
            for node in cycle:
                dll.append(node)
            dll.append(end)
            result.append(dll)
        return result
    
    def get_cycle_by_node_name(self, node_name):
        for cycle in self.cycles:
            if node_name in cycle:
                return cycle
    
    def handle_swap(self, node1, node2):
        if node1.name == node2.name:
            cycle = self.get_cycle_by_node_name(node1.name)
            cycle.reverse()
        else:
            cycle1 = self.get_cycle_by_node_name(node1.name)
            cycle2 = self.get_cycle_by_node_name(node2.name)
            if cycle1 == cycle2:
                cycle1.swap_nodes_by_name(node1.name, node2.name)
            else:
                detached_1 = cycle1.remove(node1)
                detached_2 = cycle2.remove(node2)
                leftover_1 = cycle1.attach_sublist(detached_2)
                leftover_2 = cycle2.attach_sublist(detached_1)
                if leftover_1:
                    self.cycles.append(leftover_1)
                if leftover_2:
                    self.cycles.append(leftover_2)

    
    def __str__(self) -> str:
        result = f'*** CycleListManager ***\nCycles: {len(self.cycles)}\n'
        for cycle in self.cycles:
            result += str(cycle) + '\n'
        result += '************************'
        return result

if __name__ == '__main__':
    clm = GraphManager(
        node_list='./temp/orders_with_depots.csv',
        max_cap=1000,
        vehicles=5
    )
    print(clm)

    print('handle same node')
    node = clm.node_list[14]
    clm.handle_swap(node, node)
    print(clm)

    print('handle same cycle')
    node2 = clm.node_list.get_node_by_name('Poznań')
    clm.handle_swap(node, node2)
    print(clm)

    print('handle different cycles')
    node3 = clm.node_list.get_node_by_name('Warszawa')
    node4 = clm.node_list.get_node_by_name('Gdańsk')
    clm.handle_swap(node3, node4)
    print(clm)

    node5 = clm.node_list.get_node_by_name('Krosno')
    node6 = clm.node_list.get_node_by_name('Puławy')
    clm.handle_swap(node5, node6)
    print(clm)