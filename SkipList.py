# Implementation of a Skip List
# operations:
# search_node(key), insert_node(key), predecessor_of_node(key), successor_of_node(key), print_sorted_elements

from random import randint

def flip_coin():
    return randint(0, 1)


class SkipNode:
    def __init__(self, key, levels):
        self.key = key
        self.next = [None] * levels   # will store the nodes it connects to at each level (levels start from 0)


class SkipList:
    def __init__(self, levels):
        self.head = SkipNode(-1, levels + 1)
        self.levels = levels   # height of Skiplist (levels start from 0)

    def print(self):
        print()
        lvl = self.levels - 1
        while lvl > -1:
            current = self.head
            print(f'level {lvl}', end=' ')
            while current:
                print("sentinel" if current.key == -1 else current.key, end='->')
                current = current.next[lvl]
            print()
            lvl -= 1
        print()

    def print_sorted_elemets(self):
        print()
        current = self.head.next[0]
        print(f'Sorted elements of SkipList are:', end=' ')
        while current:
            print(current.key, end=' ')
            current = current.next[0]
        print()

    # complexity: average O(log n), worst O(n)
    def search_node(self, key):
        # start from top level
        lvl = self.levels
        current = self.head
        # while we haven't reached bottom level
        while lvl > -1:
            # start node is sentinel of current level
            while current.next[lvl] and current.next[lvl].key < key:
                current = current.next[lvl]
            # go down a level
            lvl -= 1

        # current node is predecessor of key
        if current.next[0].key == key:
            print(f"Node {key} found")
            # for insertion / deletion we need to know the predecessor of the searched_node so we return its predecessor
            return current
        else:
            # if we reached bottom level and haven't found the key we return None
            print(f'Node {key} not found in SkipList')
            return None

    def predecessor_of_node(self, key):
        # start from top level
        lvl = self.levels
        current = self.head
        # while we haven't reached bottom level
        while lvl > -1:
            # start node is sentinel of current level
            while current.next[lvl] and current.next[lvl].key < key:
                current = current.next[lvl]
            # go down a level
            lvl -= 1

        # current node is predecessor of key
        print(f"Predecessor of {key} is {current.key}")
        return current

    def successor_of_node(self, key):
        # start from top level
        lvl = self.levels
        current = self.head
        # while we haven't reached bottom level
        while lvl > -1:
            # start node is sentinel of current level
            while current.next[lvl] and current.next[lvl].key < key:
                current = current.next[lvl]
            # go down a level
            lvl -= 1

        # current node is predecessor of key. To find successor we need to go 2 elements to the right
        if current.next[0].next[0]:
            # print(f"Successor of {key} is {current.next[0].next[0].key}")
            if current.next[0].key != key:
                print(f"Successor of {key} is {current.next[0].key}")
                return current.next[0]
            else:
                print(f"Successor of {key} is {current.next[0].next[0].key}")
            return current.next[0].next[0]
        else:
            # if we reached bottom level and haven't found the key we return None
            print(f"Successor of {key} is None")
            return None

    # complexity: average O(log n), worst O(n)
    def insert_node(self, key):
        # each inserted node will have at least level 0
        coin_flips = 1

        # randomly assign a level to the inserted node
        while flip_coin() and coin_flips < self.levels:
            coin_flips += 1
        inserted_node = SkipNode(key, coin_flips)

        # will store predecessors for inserted node on each level
        predecessor = [None] * (coin_flips + 1)

        lvl = coin_flips
        # print(f"Highest level for node {key} will be {coin_flips - 1}")

        current = self.head
        # search for inserted_node in list
        while lvl > -1:
            while current.next[lvl] and current.next[lvl].key < key:
                current = current.next[lvl]
            predecessor[lvl] = current
            # go down a level
            lvl -= 1

            # Skip List has no duplicates (we do not insert the node if it is already in the Skip List)
            if current.next[lvl] and current.next[lvl].key == key:
                print(f"Node {key} already in SkipList")
                return

        # reconnect nodes so that the list remains sorted
        for i in range(len(predecessor) - 1):
            temporary_node = predecessor[i].next[i]
            predecessor[i].next[i] = inserted_node
            inserted_node.next[i] = temporary_node

    # complexity: average O(log n), worst O(n)
    def remove_node(self, key):
            lvl = self.levels
            current = self.head

            predecessor = [None] * (lvl + 1)
            successor = [None] * (lvl + 1)

            # search for removed_node in list
            while lvl > -1:
                while current.next[lvl] and current.next[lvl].key < key:
                    current = current.next[lvl]
                predecessor[lvl] = current
                successor[lvl] = current.next[lvl].next[lvl] if current.next[lvl] else None
                # go down a level
                lvl -= 1

            # current node is predecessor of key
            if current.next[0].key == key:
                print(f"Node {key} found and will be deleted")
                for i in range(len(predecessor)):
                    predecessor[i].next[i] = successor[i]
            else:
                # if we reached bottom level and haven't found the key we return None
                print(f'Node {key} not found in SkipList')
                return


xs = [1, 23, 4, 3, 5, 6, 12]
skip_list = SkipList(4)
for x in xs:
    skip_list.insert_node(x)

skip_list.print()

skip_list.remove_node(23)
skip_list.remove_node(5)
skip_list.print()
print()

skip_list.successor_of_node(5)
skip_list.successor_of_node(12)

skip_list.print_sorted_elemets()



