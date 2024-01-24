import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Create a Treeview widget
tree = ttk.Treeview(root, columns=("column1", "column2"))
tree.pack(fill=tk.BOTH, expand=True)

# Add some items to the Treeview widget
tree.insert("", tk.END, text="Item 1", values=("foo", "bar"))
tree.insert("", tk.END, text="Item 2", values=("baz", "qux"))

# Define a function to modify the selected item
def modify_item():
    # Get the selected item
    selected_item = tree.selection()[0]
    
    # Modify the text label and values of the selected item
    tree.item(selected_item, text="Modified Item", values=("qux", "baz"))

# Create a button to trigger the modification
button = ttk.Button(root, text="Modify Selected Item", command=modify_item)
button.pack(fill=tk.X, padx=10, pady=10)

root.mainloop()