import tkinter as tk
from tkinter import messagebox, ttk

from gui.utils import format_task_for_display

class UI:
    def __init__(self, master):
        self.master = master
        
    def initialize(self):
        self.master.title("To-do app")
        self.create_widgets()

    def paint_description_label(self):
        self.description_label = ttk.Label(self.master, text="Description:")
        self.description_label.grid(row=0, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(self.master, width=40)
        self.description_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=3)

    def paint_priority_label_and_menu(self):
        self.priority_label = ttk.Label(self.master, text="Priority:")
        self.priority_label.grid(row=1, column=0, padx=5, pady=5)
        self.priority_var = tk.StringVar(value="Medium")
        self.priority_menu = ttk.OptionMenu(
            self.master, self.priority_var, "Medium", "High", "Medium", "Low"
        )
        self.priority_menu.grid(row=1, column=1, padx=5, pady=5, columnspan=3)

    def paint_completed_checkbox(self):
        self.completed_var = tk.BooleanVar()
        self.completed_check = ttk.Checkbutton(
            self.master, text="Completed", variable=self.completed_var
        )
        self.completed_check.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

    def paint_search_label_and_input(self):
        self.search_label = ttk.Label(self.master, text="Search:")
        self.search_label.grid(row=3, column=0, padx=5, pady=5)
        self.search_entry = ttk.Entry(self.master, width=30)
        self.search_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=3)
        self.search_button = ttk.Button(
            self.master, text="Search"
        )
        self.search_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    
    def paint_reset_button(self):
        self.reset_button = ttk.Button(
            self.master, text="Reset"
        )
        self.reset_button.grid(row=4, column=2, columnspan=2, padx=5, pady=5)

    def paint_task_list(self):
        self.task_listbox = tk.Listbox(self.master, width=50, height=10)
        self.task_listbox.grid(row=5, column=0, columnspan=4, padx=5, pady=5)
    
    def paint_sorting_menu_and_button(self):
        self.sort_label = ttk.Label(self.master, text="Sort by:")
        self.sort_label.grid(row=6, column=0, padx=5, pady=5)
        self.sort_var = tk.StringVar(value="None")
        self.sort_menu = ttk.OptionMenu(
            self.master, self.sort_var, "None", "Priority", "Completed"
        )
        self.sort_menu.grid(row=6, column=1, padx=5, pady=15, columnspan=3)
    
    def paint_action_buttons(self):
        self.add_button = ttk.Button(
            self.master, text="Add Task"
        )
        self.add_button.grid(row=8, column=0, padx=5, pady=5)
        self.delete_button = ttk.Button(
            self.master, text="Delete Task"
        )
        self.delete_button.grid(row=8, column=1, padx=5, pady=5)
        self.sort_button = ttk.Button(
            self.master, text="Sort"
        )
        self.sort_button.grid(row=8, column=2, padx=5, pady=5)
        self.complete_button = ttk.Button(
            self.master,
            text="Set Completed",
            state=tk.DISABLED,
        )
        self.complete_button.grid(row=8, column=3, padx=5, pady=5)
    
    def get_add_button(self):
        return self.add_button
    
    def get_delete_button(self):
        return self.delete_button
    
    def get_sort_button(self):
        return self.sort_button
    
    def get_search_button(self):
        return self.search_button

    def get_reset_button(self):
        return self.reset_button
    
    def get_complete_button(self):
        return self.complete_button
    
    def get_description(self):
        return self.description_entry.get()
    
    def get_priority(self):
        return self.priority_var.get()
    
    def get_completed(self):
        return self.completed_var.get()
    
    def get_sorting(self):
        return self.sort_var.get()
    
    def get_list_box(self):
        return self.task_listbox
    
    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def show_info(self, title, message):
        messagebox.showinfo(title, message)

    def clear_search(self):
        self.search_entry.delete(0, tk.END)

    def clear_sorting(self):
        self.sort_var.set("None")

    def clear_description(self):
        self.description_entry.delete(0, tk.END)
    
    def clear_listbox(self):
        self.task_listbox.delete(0, tk.END)
    
    def get_query(self):
        return self.search_entry.get()
    
    def insert_task(self, task):
        self.task_listbox.insert(tk.END, format_task_for_display(task))
    
    def select_task(self, index):
        self.task_listbox.selection_set(index)

    def get_task(self, index):
        return self.task_listbox.get(index)
    
    def get_task_list(self):
        return self.task_listbox.get(0, tk.END)
    
    def get_list_box_size(self):
        return self.task_listbox.size()
    
    def get_current_selection(self):
        return self.task_listbox.curselection()
    
    def set_button_state(self, state):
        self.complete_button.config(state=state)
    
    def recreate_sort_menu(self):
        self.master.after_idle(self.generate_sort_menu, self.get_sorting())
    
    def generate_sort_menu(self, sort_by):  # Helper function to recreate the sort menu to avoid UI shiftings
        self.sort_menu.destroy()
        self.sort_menu = ttk.OptionMenu(
            self.master, self.sort_var, sort_by, "None", "Priority", "Completed"
        )
        self.sort_menu.grid(row=6, column=1, padx=5, pady=15, columnspan=3)

    def create_widgets(self):
        # --- Task Input ---
        self.paint_description_label()
        # --- Priority ---
        self.paint_priority_label_and_menu()
        # --- Completed checkbox ---
        self.paint_completed_checkbox()
        # --- Search ---
        self.paint_search_label_and_input()
        # --- Reset ---
        self.paint_reset_button()
        # --- Task List ---
        self.paint_task_list()
        # --- Sorting ---
        self.paint_sorting_menu_and_button()
        # --- Action buttons ---
        self.paint_action_buttons()
