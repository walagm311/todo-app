class Node:
    def __init__(self, data):
        self.data = data  # data is now (task_id, description, priority, completed)
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert(self, data, index=-1):
        if self.head is None:
            self.head = Node(data)
            self.tail = self.head
            self.size += 1
        elif index == 0:
            new_node = Node(data)
            new_node.next = self.head
            self.head = new_node
            self.size += 1
        elif index == -1 or index == self.size:
            new_node = Node(data)
            if self.tail:
                self.tail.next = new_node
                self.tail = new_node
            else:
                self.head = new_node
                self.tail = new_node
            self.size += 1
        elif 0 <= index < self.size:
            new_node = Node(data)
            current_node = self.head
            current_index = 0
            while index - 1 > current_index:
                current_node = current_node.next
                current_index += 1
            new_node.next = current_node.next
            current_node.next = new_node
            if new_node.next is None:
                self.tail = new_node
            self.size += 1
        else:
            raise IndexError("Index out of range")

    def search(self, task_id):  # Search by task_id
        index = 0
        current_node = self.head
        while current_node is not None:
            if current_node.data[0] == task_id:  # Compare IDs
                return index
            current_node = current_node.next
            index += 1
        return -1

    def remove(self, index):
        if not 0 <= index < self.size:
            raise IndexError("Index out of range")

        if index == 0:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
        else:
            current_node = self.head
            current_index = 0
            while current_index < index - 1:
                current_node = current_node.next
                current_index += 1
            current_node.next = current_node.next.next
            if current_node.next is None:
                self.tail = current_node
        self.size -= 1

    def __str__(self):
        result = ""
        current_node = self.head
        while current_node is not None:
            result += str(current_node.data)
            result += " -> "
            current_node = current_node.next
        return result