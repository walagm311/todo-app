# Documentation

## Introduction
This application is a To-Do list which allows to add tasks, sort them set them complete and search them.
It has been developed using python and Tkinter.

## Data Structure Utilization

This application employs three core data structures:

1.  **Linked List:**
    *   Used to store the tasks, maintaining their insertion order.
    *   Each task is represented as a node in the list, holding the task's description, priority, and completion status.
    *   Facilitates efficient addition and deletion of tasks. 
    ```python
    class LinkedList:
        #... (other methods)...

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
            #... (rest of the insert method)...

        def remove(self, index):
            if not 0 <= index < self.size:
                raise IndexError("Index out of range")

            if index == 0:
                self.head = self.head.next
                if self.head is None:
                    self.tail = None
            #... (rest of the remove method)...
    ```

2.  **Hash Table:**
    *   Provides efficient searching of tasks by their description.
    *   The hash table uses the task description as the key to store and retrieve corresponding task nodes. 
    ```python
    class HashTable:
        #... (other methods)...

        def insert(self, key, value):
            index = self._hash(key)

            if self.items[index] is None:
                self.items[index] = HashItem(key, value)
                self.size += 1
            #... (rest of the insert method)...

        def search_by_description(self, description):
            tasks =
            for task in self.get_all_values():
                if task == description:
                    tasks.append(task)
            return tasks
    ```

3.  **Binary Search Tree:**
    *   Manages tasks based on their priority.
    *   The tree is structured according to priority levels, enabling efficient sorting and filtering of tasks by priority.
    ```python
    class BST:
        #... (other methods)...

        def insert(self, value):
            if self.root is None:
                self.root = Node(value)
            else:
                self.insert_rec(self.root, value)
            #...

        def inorder(self, node="root"):
            if node == "root":
                yield from self.inorder(self.root)
            else:
                if node is not None:
                    yield from self.inorder(node.left)
                    yield node.value
                    yield from self.inorder(node.right)
    ```

## Functionality Implementation

*   **Adding Tasks:**
    *   Assigns a unique ID to each new task.
    *   Stores the task data in all three data structures (linked list, hash table, and binary search tree) to ensure consistency and support various operations.
    ```python
    def add_task(self):
        #... (get task details)...

        self.task_list.insert(task_data)
        self.hash_table.insert(task_id, task_data)
        self.priority_tree.insert(task_data)
        #...
    ```

*   **Deleting Tasks:**
    *   Removes the specified task from all three data structures to maintain data integrity.
    ```python
    def delete_task(self):
        #...

        self.task_list.remove(index_to_remove)
        self.hash_table.delete(task_id)
        #... (delete from BST)...
        #...
    ```

*   **Searching Tasks:**
    *   Utilizes the hash table to efficiently search for tasks by their description.
    ```python
    def search_task(self):
        #...

        tasks_found = self.hash_table.search_by_description(query)
        #... (display results)...
    ```

*   **Displaying Tasks:**
    *   Displays tasks in a clear and organized manner.
    *   Provides options for sorting by priority (using the binary search tree) or completion status (using the linked list).
    ```python
    def sort_tasks(self):
        #...

        match sort_by:
            case "Priority":
                #... (sort by priority using self.priority_tree.inorder())...
            case "Completed":
                #... (sort by completion status using self.task_list)...
            case _:
                #...
    ```

## Framework Choice

*   **Tkinter** was selected as the GUI framework for its simplicity and ease of use, especially for beginners.

## Challenges

*   **Balancing the BST:**
    *   Maintaining the balance of the binary search tree is crucial for efficient operations.
    *   Unbalanced trees can lead to degraded performance, requiring strategies to ensure balance.

*   **GUI Development:**
    *   Designing a user-friendly interface while keeping the primary focus on the underlying data structure logic.

*   **Integrating Data Structures:**
    *   Ensuring seamless integration of the linked list, hash table, and binary search tree to work together effectively.

## Team Contribution

The team members for this project are:

* Wala Gajim
* Nouralhuda Ben Zaid
* Sajida Shabbi

Each team member contributed in equal size.