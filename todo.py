############ TASK-1 : To-Do List #######################  
########### Kaustubh Gaikwad ##############

import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from tkcalendar import DateEntry
import json
import os

# File to save tasks
TASKS_FILE = "tasks.json"

# To-Do List Application Class
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("1280x720")
        self.root.configure(bg="#ADD8E6")
        
        self.set_titlebar_color("#ADD8E6")
        
            
        # Attributes
        self.tasks = []
        self.load_tasks()
        self.mode = "light"

        #Setting titlebar color to dark
        if self.mode == "dark":
            self.set_titlebar_color("#2B2B2B")
            
        # UI Components
        self.create_widgets(self.mode == "light")
        self.display_tasks()

    # Set Title Bar Color
    def set_titlebar_color(self, color):
        self.root.tk_setPalette(background=color)
        self.root.update()

    # Create GUI Widgets
    def create_widgets(self, mode):
        # Header
        header = tk.Label(self.root, text="To-Do List Application", font=("Roboto", 24, "bold"), fg="Black")
        header.pack(fill=tk.X, pady=10)

        # if self.mode == "light":
        #     self.header = header
        # else:
        #     self.header = tk.Label(self.root, text="To-Do List Application", font=("Roboto", 24, "bold"), fg="white")
        #     self.header.pack(fill=tk.X, pady=10)
        
        
        # Task Entry Frame
        if self.mode == "dark":
            entry_frame = tk.Frame(self.root, bg="black")
            entry_frame.pack(pady=15)
        else:
            entry_frame = tk.Frame(self.root, bg="#ADD8E6")
            entry_frame.pack(pady=15)
            

        # Task Name
        tk.Label(entry_frame, text="Task:", font=("Helvetica", 12, "bold"), fg="black").grid(row=0, column=0, padx=10, pady=5)
        self.task_entry = tk.Entry(entry_frame, width=40, font=("Helvetica", 11), bg="white")
        self.task_entry.grid(row=0, column=1, padx=10, pady=5)

        # Category
        tk.Label(entry_frame, text="Category:", font=("Helvetica", 12, "bold"), fg="black").grid(row=1, column=0, padx=10, pady=5)
        self.category_combobox = ttk.Combobox(entry_frame, values=["Work", "Personal", "Shopping", "Others"], state="readonly", font=("Helvetica", 11))
        self.category_combobox.grid(row=1, column=1, padx=10, pady=5)
        self.category_combobox.set("Work")

        # Priority
        tk.Label(entry_frame, text="Priority:", font=("Helvetica", 12, "bold"), fg="black").grid(row=2, column=0, padx=10, pady=5)
        self.priority_combobox = ttk.Combobox(entry_frame, values=["High", "Medium", "Low"], state="readonly", font=("Helvetica", 11))
        self.priority_combobox.grid(row=2, column=1, padx=10, pady=5)
        self.priority_combobox.set("Medium")

        # Deadline
        tk.Label(entry_frame, text="Deadline:", font=("Helvetica", 12, "bold"), fg="black").grid(row=3, column=0, padx=10, pady=5)
        self.deadline_entry = DateEntry(entry_frame, width=17, background='#4A5C6A', foreground='white', borderwidth=2, font=("Helvetica", 11))
        self.deadline_entry.grid(row=3, column=1, padx=10, pady=5)

        # Add Task Button
        self.add_button = tk.Button(entry_frame, text="Add Task", command=self.add_task, bg="#66A182", fg="white", font=("Helvetica", 11, "bold"), width=15)
        self.add_button.grid(row=4, column=1, pady=10)

        # Task Display Frame
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        self.tree = ttk.Treeview(self.root, columns=("Task", "Category", "Priority", "Deadline"), show="headings")
        self.tree.heading("Task", text="**Task**")
        self.tree.heading("Category", text="**Category**")
        self.tree.heading("Priority", text="**Priority**")
        self.tree.heading("Deadline", text="**Deadline**")
        self.tree.pack(pady=10, fill=tk.X, expand=False, anchor="center")

        # Align task text in center
        for col in ("Task", "Category", "Priority", "Deadline"):
            self.tree.column(col, anchor="center")


        # Buttons Frame
        button_frame = tk.Frame(self.root, bg="#ADD8E6")
        button_frame.pack(pady=10)

                

        self.delete_button = tk.Button(button_frame, text="Delete Task", command=self.delete_task, bg="#E54B4B", fg="white", font=("Helvetica", 11, "bold"), width=15)
        self.delete_button.grid(row=0, column=0, padx=10)

        self.update_button = tk.Button(button_frame, text="Update Task", command=self.update_task, bg="#FFC107", fg="black", font=("Helvetica", 11, "bold"), width=15)
        self.update_button.grid(row=0, column=1, padx=10)

        self.toggle_button = tk.Button(button_frame, text="Dark Mode", command=self.toggle_mode, bg="#4A5C6A", fg="white", font=("Helvetica", 11, "bold"), width=15)
        self.toggle_button.grid(row=0, column=2, padx=10)

        
        # Buttons Frame (Dark mode)
        if self.mode == "Dark":
            button_frame = tk.Frame(self.root, bg="black")
            button_frame.pack(pady=10)
        else:
            button_frame = tk.Frame(self.root, bg="#ADD8E6")
            button_frame.pack(pady=10)
            
            
        # Progress Label
        self.progress_label = tk.Label(self.root, text="Progress: 0%", font=("Helvetica", 12), bg="#EDEDED", fg="#333333")
        self.progress_label.pack(pady=10)

    # Add Task
    def add_task(self):
        task = self.task_entry.get()
        category = self.category_combobox.get()
        priority = self.priority_combobox.get()
        deadline = self.deadline_entry.get_date().strftime("%d-%m-%Y")

        if not task:
            messagebox.showwarning("Warning", "Task name cannot be empty!")
            return

        self.tasks.append({"task": task, "category": category, "priority": priority, "deadline": deadline})
        self.save_tasks()
        self.display_tasks()
        self.task_entry.delete(0, tk.END)

    # Update Task
    def update_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to update!")
            return

        task_index = self.tree.index(selected_item)
        task_data = self.tasks[task_index]

        update_window = Toplevel(self.root)
        update_window.title("Update Task")
        update_window.geometry("400x300")

        tk.Label(update_window, text="Update Task Details", font=("Helvetica", 14, "bold")).pack(pady=10)

        tk.Label(update_window, text="Task:").pack()
        task_entry = tk.Entry(update_window)
        task_entry.insert(0, task_data['task'])
        task_entry.pack()

        tk.Label(update_window, text="Category:").pack()
        category_combobox = ttk.Combobox(update_window, values=["Work", "Personal", "Shopping", "Others"], state="readonly")
        category_combobox.set(task_data['category'])
        category_combobox.pack()

        tk.Label(update_window, text="Priority:").pack()
        priority_combobox = ttk.Combobox(update_window, values=["High", "Medium", "Low"], state="readonly")
        priority_combobox.set(task_data['priority'])
        priority_combobox.pack()

        def save_updates():
            task_data['task'] = task_entry.get()
            task_data['category'] = category_combobox.get()
            task_data['priority'] = priority_combobox.get()
            self.save_tasks()
            self.display_tasks()
            update_window.destroy()

        tk.Button(update_window, text="Save", command=save_updates).pack(pady=10)

    # Delete Selected Task
    def delete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            task_index = self.tree.index(selected_item)
            del self.tasks[task_index]
            self.save_tasks()
            self.display_tasks()

    # Save Tasks
    def save_tasks(self):
        try:
            with open(TASKS_FILE, "w") as file:
                json.dump(self.tasks, file, indent=4)
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save tasks: {e}")

    # Load Tasks
    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            try:
                with open(TASKS_FILE, "r") as file:
                    self.tasks = json.load(file)
            except (IOError, json.JSONDecodeError) as e:
                messagebox.showerror("Error", f"Failed to load tasks: {e}")

    # Display Tasks
    def display_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for task in self.tasks:
            self.tree.insert("", tk.END, values=(task["task"], task["category"], task["priority"], task["deadline"]))
        self.update_progress()

   
    # Update Progress
    def update_progress(self):
        target_tasks = 10  # Define your target number of tasks
        total_tasks = len(self.tasks)
    
        if total_tasks >= target_tasks:
            progress = 100  # If the total tasks meet or exceed the target, set progress to 100%
        else:
            progress = round((total_tasks / target_tasks) * 100)  # Calculate progress as a percentage of the target

        self.progress_label.config(text=f"Progress: {progress}%")

    # Toggle Mode
    def toggle_mode(self):
        if self.mode == "light":
            self.mode = "dark"
            self.task_entry.config(bg="White")
            self.root.config(bg="black")
            self.style.configure("Treeview", background="darkblue", foreground="white")
            self.toggle_button.config(text="Light Mode", bg="#333333", fg="white")
            self.update_widgets_style("dark")
        else:
            self.mode = "light"
            self.root.config(bg="#ADD8E6")
            self.style.configure("Treeview", background="lightblue", foreground="black")
            self.toggle_button.config(text="Dark Mode", bg="#4A5C6A", fg="white")
            self.update_widgets_style("light")

    def update_widgets_style(self, mode):
        bg_color = "white" if mode == "light" else "#333333"
        fg_color = "black" if mode == "light" else "White"
        # self.task_entry.config(bg=bg_color, fg=fg_color)
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=self.root.cget("bg"), fg=fg_color)
            elif isinstance(widget, tk.Button):
                widget.config(bg="#EDEDED" if mode == "light" else "#4A5C6A", fg=fg_color)

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()