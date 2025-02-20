import tkinter as tk

from gui.logic import Logic
from gui.ui import UI


class ToDoList:
    def __init__(self, master):
        ui = UI(master)
        logic = Logic(ui)
        ui.initialize()
        logic.run()
        

root = tk.Tk()
app = ToDoList(root)
root.mainloop()