import json
import getpass

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

# User class for managing user authentication
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# User Management System
class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def register_user(self, username, password):
        if username in self.users:
            print("User already exists. Please choose a different username.")
            return False
        self.users[username] = User(username, password)
        self.save_users()
        print("User registered successfully!")
        return True

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            return True
        print("Invalid username or password.")
        return False

    def save_users(self):
        with open('users.json', 'w') as f:
            json.dump({username: user.password for username, user in self.users.items()}, f)

    def load_users(self):
        try:
            with open('users.json', 'r') as f:
                users_data = json.load(f)
                self.users = {username: User(username, password) for username, password in users_data.items()}
        except FileNotFoundError:
            pass  # No users saved yet

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
    user_manager = UserManager()
    task_manager = TaskManager()

    # User registration
    print("Welcome to the Task Management System")
    while True:
        choice = input("Do you want to (1) Register or (2) Login? (Enter 1 or 2): ")
        if choice == '1':
            username = input("Enter a username: ")
            password = getpass.getpass("Enter a password: ")
            user_manager.register_user(username, password)
        elif choice == '2':
            username = input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")
            if user_manager.authenticate_user(username, password):
                break
        else:
            print("Invalid option. Please try again.")

    # ANSI escape codes for colors
    PRIORITY_COLORS = {
        1: "\033[91m",  # Red
        2: "\033[93m",  # Yellow
        3: "\033[92m",  # Green
        4: "\033[94m",  # Blue
        5: "\033[95m",  # Magenta
        6: "\033[96m",  # Cyan
        7: "\033[97m",  # White
        8: "\033[90m",  # Bright Black
        9: "\033[34m",  # Bright Blue
        10: "\033[35m", # Bright Magenta
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
            try:
                priority = int(input("Enter task priority (1-10): "))
                if priority < 1 or priority > 10:
                    raise ValueError("Priority must be between 1 and 10.")
                task_manager.add_task(title, description, priority)
                print("Task added successfully!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '2':
            try:
                task_id = int(input("Enter task ID to update: "))
                title = input("Enter new task title: ")
                description = input("Enter new task description: ")
                priority = int(input("Enter new task priority (1-10): "))
                if priority < 1 or priority > 10:
                    raise ValueError("Priority must be between 1 and 10.")
                if task_manager.update_task(task_id, title, description, priority):
                    print("Task updated successfully!")
                else:
                    print("Task ID not found.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '3':
            try:
                task_id = int(input("Enter task ID to delete: "))
                if task_manager.delete_task(task_id):
                    print("Task deleted successfully!")
                else:
                    print("Task ID not found.")
            except ValueError as e:
                print(f"Error: {e}")

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
