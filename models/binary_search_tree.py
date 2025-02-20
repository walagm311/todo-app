class Node:
    def __init__(self, value):
        self.value = value  # Store the entire tuple (task_id, description, priority, completed)
        self.left = None
        self.right = None
        self.parent = None  # Add parent pointer for easier deletion
        self.height = 0 # Height for balancing

    def __repr__(self, level=0):
        # Improved __repr__ to handle tuples
        ret = "\t" * level + repr(self.value[1]) + "\n"  # Show description
        if self.left:
            ret += "L" + self.left.__repr__(level + 1)
        if self.right:
            ret += "R" + self.right.__repr__(level + 1)
        return ret

class BST:
    def __init__(self):
        self.root = None

    def update_height(self, node):
        if node is None: #Add the check if the node is none
            return -1
        if node.left is None:
            height_l = -1
        else:
            height_l = node.left.height
        if node.right is None:
            height_r = -1
        else:
            height_r = node.right.height
        return max(height_l, height_r) + 1

    def insert_rec(self, node, value):
        # Compare based on the description (second element of the tuple)
        if value[1] >= node.value[1]:
            if node.right is None:
                node.right = Node(value)
                node.right.parent = node  # Set parent pointer
            else:
                self.insert_rec(node.right, value)
            node.height = self.update_height(node)
        else:
            if node.left is None:
                node.left = Node(value)
                node.left.parent = node  # Set parent pointer
            else:
                self.insert_rec(node.left, value)
            node.height = self.update_height(node)

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self.insert_rec(self.root, value)
        self.root.height = self.update_height(self.root)

    def search_rec(self, node, value):
        # Search by description
        if node is None:
            return False
        elif node.value[1] == value:
            return True
        elif value > node.value[1]:
            return self.search_rec(node.right, value)
        else:
            return self.search_rec(node.left, value)

    def search(self, value):
        if self.root is None:
            return False
        else:
            return self.search_rec(self.root, value)
    
    def searchByData(self, task_id):
        return self._search_by_data_recursive(self.root, task_id)

    def _search_by_data_recursive(self, node, task_id):
        if node is None:
            return None  # Not found
        if task_id == node.value[0]:  # Compare with the task_id
            return node
        else:  # Search both subtrees (since BST is ordered by description)
            left_result = self._search_by_data_recursive(node.left, task_id)
            if left_result:
                return left_result
            return self._search_by_data_recursive(node.right, task_id)

    def find_min(self, node):
        current_node = node
        while current_node.left is not None:
            current_node = current_node.left
        return current_node

    def delete(self, node):
        if node is None:
            return

        # Case 1: Node has no children
        if node.left is None and node.right is None:
            if node.parent:
                if node.parent.left == node:
                    node.parent.left = None
                else:
                    node.parent.right = None
            else:
                self.root = None

        # Case 2: Node has one child
        elif node.left is None:
            if node.parent:
                if node.parent.left == node:
                    node.parent.left = node.right
                else:
                    node.parent.right = node.right
                node.right.parent = node.parent
            else:
                self.root = node.right
                self.root.parent = None
        elif node.right is None:
            if node.parent:
                if node.parent.left == node:
                    node.parent.left = node.left
                else:
                    node.parent.right = node.left
                node.left.parent = node.parent
            else:
                self.root = node.left
                self.root.parent = None
        # Case 3: Node has two children
        else:
            successor = self.find_min(node.right)
            node.value = successor.value
            self.delete(successor)  # Recursively delete the successor

        if node is not None and node.parent is not None:
             node.parent.height = self.update_height(node.parent)

    def BFS(self):
        if not self.root:
            return
        q = [self.root]
        while len(q) > 0:
            current_node = q.pop(0)  # Use pop(0) for FIFO queue
            yield current_node.value
            if current_node.left is not None:
                q.append(current_node.left)
            if current_node.right is not None:
                q.append(current_node.right)

    def inorder(self, node="root"):
        if node == "root":
            yield from self.inorder(self.root)
        else:
            if node is not None:
                yield from self.inorder(node.left)
                yield node.value
                yield from self.inorder(node.right)

    def preorder(self, node="root"):
        if node == "root":
            yield from self.preorder(self.root)
        else:
            if node is not None:
                yield node.value
                yield from self.preorder(node.left)
                yield from self.preorder(node.right)

    def postorder(self, node="root"):
        if node == "root":
            yield from self.postorder(self.root)
        else:
            if node is not None:
                yield from self.postorder(node.left)
                yield from self.postorder(node.right)
                yield node.value

    def __repr__(self):
        if self.root is None:
            return "<empty tree>"
        return self.root.__repr__()