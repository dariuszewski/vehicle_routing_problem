try:
    from src.algorithms.models.node import Node, NodeList
    from src.utils.haversine import haversine
except:
    from node import Node, NodeList
    from haversine import haversine


class DoublyLinkedList:
    def __init__(self, head, max_cap, node_list=None) -> None:
        self.head = head
        self.max_cap = max_cap
        self.node_list = node_list
    

    @property
    def weight(self):
        return sum([node.weight for node in self])

    @property
    def length(self):
        length = 0
        cn = self.head
        while cn.next:
            length += haversine(cn.lon, cn.lat, cn.next.lon, cn.next.lat)
            cn = cn.next
        return round(length, 2)

    @property
    def last(self):
        cur_node = self.head
        while cur_node.next:
            cur_node = cur_node.next
        return cur_node

    def __contains__(self, node):
        if not isinstance(node, str):
            raise BaseException('Not implemented')
        else:
            names = [node.name for node in self.to_list()]
            return node in names

    def __len__(self):
        count = 0
        cur_node = self.head
        while cur_node:
            count += 1
            cur_node = cur_node.next
        return count
    
    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next

    def __str__(self) -> str:
        string = f"<DoublyLinkedList (weight: {self.weight}, length: {self.length}) "
        current_node = self.head
        while current_node.next:
            string = string + current_node.name + ' -> '
            current_node = current_node.next
        string = string + current_node.name + ' >'
        return string

    def get_node_by_name(self, name):
        current_node = self.head
        while current_node.next:
            if current_node.name == name:
                return current_node
            current_node = current_node.next
        return 
    
    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current)
            current = current.next
        return result

    def from_list(self, nodes):
        self.head = None
        for node in nodes:
            print(node)
            self.append(node)

    def swap_nodes_by_name(self, name1, name2):
        if name1 == name2:
            self.reverse()

        node1 = self.get_node_by_name(name1)
        node2 = self.get_node_by_name(name2)

        if node1 is None or node2 is None or node1 == node2:
            return  # One or both nodes not found or they are the same node

        # If the nodes are adjacent, handle it as a special case
        if node1.next is node2:  # Node1 is right before Node2
            self._swap_adjacent_nodes(node1, node2)
        elif node2.next is node1:  # Node2 is right before Node1
            self._swap_adjacent_nodes(node2, node1)
        else:
            # Non-adjacent nodes, swap normally
            self._swap_non_adjacent_nodes(node1, node2)

    def _swap_adjacent_nodes(self, node1, node2):
        # Assume node1 is right before node2
        if node1.prev:
            node1.prev.next = node2
        else:
            self.head = node2

        if node2.next:
            node2.next.prev = node1

        node1.next = node2.next
        node2.prev = node1.prev

        node2.next = node1
        node1.prev = node2

    def _swap_non_adjacent_nodes(self, node1, node2):
        # Swap the prev and next of both nodes
        node1.prev, node2.prev = node2.prev, node1.prev
        node1.next, node2.next = node2.next, node1.next

        # Fix the surrounding links
        if node1.prev:
            node1.prev.next = node1
        else:
            self.head = node1

        if node1.next:
            node1.next.prev = node1

        if node2.prev:
            node2.prev.next = node2
        else:
            self.head = node2

        if node2.next:
            node2.next.prev = node2
            
    def append(self, node):
        if self.max_cap < self.weight + node.weight:
            raise BaseException('Exceeded max weight. Implement split!')
        elif not self.head:
            self.head = node
        else:
            node.prev = self.last
            self.last.next = node

    def remove(self, node):
        if node.prev:
            node.prev.next = None
        else:
            self.head = None
        node.prev = None
        # Return the head of the detached sublist
        return node  
          
    def attach_sublist(self, node):
        item = node
        next_item = item.next
        new_ll = None
        while next_item:
            # print('Attaching sublist to', str(self.to_list()) if not new_ll  else str(new_ll.to_list()), 'cw:', self.weight if not new_ll else new_ll.weight)
            # print('Attaching', item)
            item.next = None
            try:
                if not new_ll:
                    self.append(item)
                else:
                    new_ll.append(item)
            except:
                self.append(self.node_list.get_closest_depot(item))
                new_ll = DoublyLinkedList(head=self.node_list.get_closest_depot(item), max_cap=self.max_cap, node_list=self.node_list) # node need to be able to find closest depot
                new_ll.append(item)
            item = next_item
            next_item = next_item.next

        if new_ll:
            new_ll.append(self.node_list.get_closest_depot(item))
        else:
            self.append(self.node_list.get_closest_depot(self.last))
        
        return new_ll

    def reverse(self):
        nodes = self.to_list()
        for node in nodes:
            node.next, node.prev = node.prev, node.next
        if nodes:
            self.head = nodes[-1]
    
    def swap_single_nodes(self, node1, node2):
        node1.prev.next, node2.prev.next = node2.prev.next, node1.prev.next
        node1.next.prev, node2.next.prev = node2.next.prev, node1.next.prev

        node1.prev, node2.prev = node2.prev, node1.prev
        node1.next, node2.next = node2.next, node1.next

            
if __name__ == "__main__":
    # Load nodes from a file
    file_path = './data/orders_with_depots.csv'  # Replace with your actual file path
    node_list = NodeList.from_flie(file_path)
    cl = node_list[1:5]
    # creating
    dll = DoublyLinkedList(head=node_list.get_closest_depot(node_list[4]), max_cap=1000, node_list=node_list)
    dll.append(node_list[1])
    dll.append(node_list[2])
    dll.append(node_list[3])
    dll.append(node_list.get_closest_depot(node_list[4]))
    # dll.append(node_list[4])
    # dll.append(node_list[5])
    print(dll) 
    # swapping within
    dll.swap_nodes_by_name('Białystok', 'Bielsko-Biała')
    print(dll)
    print(node_list[4])
    other = DoublyLinkedList(head=node_list.get_closest_depot(node_list[4]), max_cap=1000, node_list=node_list)
    print(other)
    other.append(node_list[4])
    other.append(node_list[5])
    other.append(node_list[6])
    other.append(node_list[7])
    print(other)

    # detaching and attaching
    print('* Detaching *')
    new = DoublyLinkedList(head=node_list.get_closest_depot(node_list[4]), max_cap=1000, node_list=node_list)
    new.append(node_list[8])
    new.append(node_list[9])
    new.append(node_list[10])
    new.append(node_list[11])
    new.append(node_list[12])
    new.append(node_list[13])
    new.append(node_list[14])
    new.append(node_list[15])
    new.append(node_list.get_closest_depot(node_list[4]))
    print(node_list.get_node_by_name('Chrzanów'))
    print(dll)
    print(new)
    detached = dll.remove(dll.get_node_by_name('Chrzanów'))
    detached2 = new.remove(new.get_node_by_name('Lublin'))
    print(dll)
    print(new)
    print(detached)
    print(detached2)
    print('* Attaching *')
    nd = dll.attach_sublist(detached2)
    nn = new.attach_sublist(detached)
    print(dll)
    print(new) 
    print(nd)
    print(nn)

    print('* Reversing *')
    print(dll)
    dll.reverse()
    print(dll)

    print('* Single Node Swap *')
    print(dll)
    print(new)
    one = dll.get_node_by_name('Malbork')
    two = new.get_node_by_name('Chrzanów')
    dll.swap_single_nodes(one, two)
    print(dll)
    print(new)

# class LinkedListsManager:
#     def __init__(self, max_cap):
#         self.lists = []
#         self.max_cap = max_cap

#     def add_list(self, dll):
#         self.lists.append(dll)

#     def find_list_with_node(self, node_name):
#         for dll in self.lists:
#             if dll.get_node_by_name(node_name) is not None:
#                 return dll
#         return None

#     def swap_node(self, node_name1, node_name2):
#         list1 = self.find_list_with_node(node_name1)
#         list2 = self.find_list_with_node(node_name2)

#         if list1 is None or list2 is None:
#             raise ValueError("One or both nodes not found in any lists")

#         node1 = list1.get_node_by_name(node_name1)
#         node2 = list2.get_node_by_name(node_name2)

#         # Detach nodes from their respective lists
#         list1.detach_node(node1)
#         list2.detach_node(node2)

#         # Check if attaching nodes exceeds max weight and handle accordingly
#         if not list1.attach_node(node2):
#             self.handle_overflow(list1, node2)
#         if not list2.attach_node(node1):
#             self.handle_overflow(list2, node1)

# # Example usage
# manager = LinkedListsManager(max_cap=1000)
# list1 = dll
# list2 = other
# # Assume lists are populated
# manager.add_list(list1)
# manager.add_list(list2)
# print(manager)
# # Perform a swap operation
# manager.swap_node(node_name1="Gdynia", node_name2="Białystok")

