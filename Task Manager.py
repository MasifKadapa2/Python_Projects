import json

# Node class for a linked list
class Node:
    def __init__(self, task):
        self.task = task
        self.next = None

# Linked List class for managing tasks
class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, task):
        new_node = Node(task)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def delete(self, task_id):
        current = self.head
        previous = None
        while current:
            if current.task['id'] == task_id:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                return True
            previous = current
            current = current.next
        return False

    def update(self, task_id, updated_task):
        current = self.head
        while current:
            if current.task['id'] == task_id:
                current.task = updated_task
                return True
            current = current.next
        return False

    def get_all_tasks(self):
        tasks = []
        current = self.head
        while current:
            tasks.append(current.task)
            current = current.next
        return tasks

# Priority Queue class for managing tasks based on priority
class PriorityQueue:
    def __init__(self):
        self.tasks = []

    def enqueue(self, task):
        self.tasks.append(task)
        self.tasks.sort(key=lambda x: x['priority'])

    def dequeue(self):
        return self.tasks.pop(0) if self.tasks else None

    def is_empty(self):
        return len(self.tasks) == 0

    def get_all_tasks(self):
        return self.tasks

# Task Management System
class TaskManager:
    def __init__(self):
        self.task_list = LinkedList()
        self.priority_queue = PriorityQueue()
        self.load_tasks()

    def add_task(self, title, description, priority):
        task_id = len(self.priority_queue.get_all_tasks()) + 1
        task = {'id': task_id, 'title': title, 'description': description, 'priority': priority}
        self.task_list.append(task)
        self.priority_queue.enqueue(task)
        self.save_tasks()

    def update_task(self, task_id, title, description, priority):
        updated_task = {'id': task_id, 'title': title, 'description': description, 'priority': priority}
        if self.task_list.update(task_id, updated_task):
            # Update in priority queue as well
            self.priority_queue.delete(task_id)
            self.priority_queue.enqueue(updated_task)
            self.save_tasks()
            return True
        return False

    def delete_task(self, task_id):
        if self.task_list.delete(task_id):
            self.priority_queue.delete(task_id)
            self.save_tasks()
            return True
        return False

    def view_tasks(self):
        return self.priority_queue.get_all_tasks()

    def save_tasks(self):
        tasks = self.task_list.get_all_tasks()
        with open('tasks.json', 'w') as f:
            json.dump(tasks, f)

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as f:
                tasks = json.load(f)
                for task in tasks:
                    self.task_list.append(task)
                    self.priority_queue.enqueue(task)
        except FileNotFoundError:
            pass  # No tasks saved yet

# Main function to interact with the Task Manager
def main():
    task_manager = TaskManager()

    # ANSI escape codes for colors
    PRIORITY_COLORS = {
        1: "\033[91m",  # Red
        2: "\033[93m",  # Yellow
        3: "\033[92m",  # Green
        4: "\033[94m",  # Blue
        5: "\033[95m",  # Magenta
    }
    RESET_COLOR = "\033[0m"

    while True:
        print("\nTask Management System")
        print("1. Add Task")
        print("2. Update Task")
        print("3. Delete Task")
        print("4. View All Tasks")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            priority = int(input("Enter task priority (1-5): "))
            task_manager.add_task(title, description, priority)
            print("Task added successfully!")

        elif choice == '2':
            task_id = int(input("Enter task ID to update: "))
            title = input("Enter new task title: ")
            description = input("Enter new task description: ")
            priority = int(input("Enter new task priority (1-5): "))
            if task_manager.update_task(task_id, title, description, priority):
                print("Task updated successfully!")
            else:
                print("Task ID not found.")

        elif choice == '3':
            task_id = int(input("Enter task ID to delete: "))
            if task_manager.delete_task(task_id):
                print("Task deleted successfully!")
            else:
                print("Task ID not found.")

        elif choice == '4':
            tasks = task_manager.view_tasks()
            if tasks:
                print("\nTasks:")
                for task in tasks:
                    color = PRIORITY_COLORS.get(task['priority'], RESET_COLOR)
                    print(f"{color}ID: {task['id']}, Title: {task['title']}, Description: {task['description']}, Priority: {task['priority']}{RESET_COLOR}")
            else:
                print("No tasks available.")

        elif choice == '5':
            print("Exiting Task Management System.")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
