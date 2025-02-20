import tkinter as tk
from gui.utils import format_task_for_display
from models.binary_search_tree import BST
from models.hash_table import HashTable
from models.linked_list import LinkedList


class Logic:
    def __init__(self, view):
        self.view = view
    
    def run(self):
        self.task_list = LinkedList()
        self.hash_table = HashTable(10)
        self.priority_tree = BST()
        self.next_task_id = 1  # Initialize the task ID counter
        self.bind_events()

    def bind_events(self):
        self.view.get_add_button().config(command=self.add_task)
        self.view.get_delete_button().config(command=self.delete_task)
        self.view.get_sort_button().config(command=self.sort_tasks)
        self.view.get_complete_button().config(command=self.set_completed)
        self.view.get_search_button().config(command=self.search_task)
        self.view.get_reset_button().config(command=self.reset_task_list)
        self.view.get_list_box().bind("<<ListboxSelect>>", lambda event: self.check_complete_button_state())
    
    def add_task(self):
        description = self.view.get_description()
        priority = self.view.get_priority()
        completed = self.view.get_completed()
    
        if not description:
            self.view.show_error("Error", "Please enter a task description.")
            return

        # Generate unique ID and create the task tuple
        task_id = self.next_task_id
        self.next_task_id += 1
        task_data = (task_id, description, priority, completed)

        self.task_list.insert(task_data)
        self.hash_table.insert(task_id, task_data)  # Use task_id as key
        self.priority_tree.insert(task_data)

        self.update_task_list()
        self.view.clear_description() # Clear the description input
        self.check_complete_button_state()
    
    def delete_task(self):
        try:
            task_id = self.get_task_id_from_selection()  # Retrieve the task id
            if task_id is None:
                self.view.show_error("Error", "Please select a valid task to delete.")
                return

            index_to_remove = self.task_list.search(task_id)
            if index_to_remove != -1:
                self.task_list.remove(index_to_remove)
            else:
                self.view.show_error("Error", "Task not found in LinkedList.")
                return

            self.hash_table.delete(task_id)
            # Delete from BST using searchByData (which returns the node)
            node_to_delete = self.priority_tree.searchByData(task_id)
            if node_to_delete:
                self.priority_tree.delete(node_to_delete)

            self.update_task_list()
            self.check_complete_button_state()

        except (IndexError, ValueError):
            self.view.show_error("Error", "Please select a valid task to delete.")

    def search_task(self):
        query = self.view.get_query()
        # Handle empty query
        if not query:
            self.view.show_error("Error", "Please enter a search query.")
            return
        # Search by description
        tasks_found = self.hash_table.search_by_description(query)
        if tasks_found:
            self.view.clear_listbox()
            for task in tasks_found:
                self.view.insert_task(task)
        else:
            self.view.show_info("Info", "Task not found.")

    def sort_tasks(self):
        sort_by = self.view.get_sorting()

        match sort_by:
            case "Priority":
                sorted_tasks = []
                for task_tuple in self.priority_tree.inorder():
                    sorted_tasks.append(task_tuple)

                priority_order = {"High": 0, "Medium": 1, "Low": 2}
                sorted_tasks.sort(key=lambda x: priority_order.get(x[2], 3))
                self.update_task_list(sorted_tasks)

            case "Completed":
                sorted_tasks = []
                current = self.task_list.head
                while current:
                    sorted_tasks.append(current.data)
                    current = current.next

                sorted_tasks.sort(key=lambda x: x[3], reverse=True)
                self.update_task_list(sorted_tasks)

            case _:  # Default case
                self.update_task_list()

        # Recreate the OptionMenu (for correct display)
        self.view.recreate_sort_menu()
        self.check_complete_button_state()
    
    def reset_task_list(self):
        self.view.clear_search()
        self.view.clear_sorting()
        self.update_task_list()

    def update_task_list(self, sorted_tasks=None):
        self.view.clear_listbox() # Clear the listbox
        if sorted_tasks is None:
            # No sorting, display all tasks from LinkedList
            current = self.task_list.head
            while current:
                task_data = current.data
                self.view.insert_task(  # Don't show the ID
                    tk.END,
                    f"{task_data[1]} - Priority: {task_data[2]}, Completed: {task_data[3]}",
                )
                current = current.next
        else:
            # Display sorted tasks
            for task in sorted_tasks:
                self.view.insert_task(  # Don't show the ID
                    tk.END,
                    f"{task[1]} - Priority: {task[2]}, Completed: {task[3]}",
                )

    def set_completed(self):
        try:
            task_id = self.get_task_id_from_selection() # Retrieve the task id
            if task_id is None:
                self.view.show_error("Error", "Please select a valid task.")
                return

            # Find selected index
            selected_indices = self.view.get_current_selection()

            if not selected_indices:
                self.view.show_error("Error", "Please select a task.")
                return
            selected_index = selected_indices[0]

            # Find and update the task in the LinkedList
            current = self.task_list.head
            while current:
                if current.data[0] == task_id:
                    current.data = (
                        task_id,
                        current.data[1],  # Description
                        current.data[2],  # Priority
                        True,  # Set Completed to True
                    )
                    break
                current = current.next

            # Find and update in HashTable
            task_details = self.hash_table.get(task_id)
            if task_details:
                self.hash_table.insert(
                    task_id, (task_id, task_details[1], task_details[2], True)
                )

            # Find and update in BST
            node_to_update = self.priority_tree.searchByData(task_id)
            if node_to_update:
                node_to_update.value = (
                    task_id,
                    node_to_update.value[1],  # Description
                    node_to_update.value[2],  # Priority
                    True,  # Set Completed to True
                )

            self.update_task_list()
            # Re-select the task after updating
            if 0 <= selected_index < self.view.get_list_box_size():  # Check index range
                self.view.select_task(selected_index)
            self.check_complete_button_state()

        except (IndexError, ValueError):
            self.view.show_error("Error", "Please select a valid task.")

    def check_complete_button_state(self):
        task_id = self.get_task_id_from_selection()

        if task_id is None:
            self.view.set_button_state(state=tk.DISABLED)
            return

        current = self.task_list.head
        while current:
            if current.data[0] == task_id:
                if current.data[3]:  # Check completion status (index 3)
                    self.view.set_button_state(state=tk.DISABLED)
                else:
                    self.view.set_button_state(state=tk.NORMAL)
                return
            current = current.next

        self.view.set_button_state(state=tk.DISABLED)
    
    def update_task_list(self, sorted_tasks=None):
        self.view.clear_listbox()
        if sorted_tasks is None:
            # No sorting, display all tasks from LinkedList
            current = self.task_list.head
            while current:
                task_data = current.data
                # Use the helper function for consistent formatting
                self.view.insert_task(task_data)
                current = current.next
        else:
            # Display sorted tasks
            for task in sorted_tasks:
                # Use the helper function for consistent formatting
                self.view.insert_task(task)
    
    def get_task_id_from_selection(self): # Helper function to get the task_id from the selected listbox item
        selected_indices = self.view.get_current_selection()

        if not selected_indices:
            return None  # No task selected

        selected_index = selected_indices[0]
        selected_task = self.view.get_task(selected_index)

        if not selected_task:  # Handle empty string case
            return None

        description = selected_task.split(" - ")[0]
        tasks = self.hash_table.search_by_description(description)
        for task in tasks:
            if format_task_for_display(task) == selected_task:
                return task[0]  # Return the task_id

        return None