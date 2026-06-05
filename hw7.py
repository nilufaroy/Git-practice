# Generalized Vector Class  
import math
class Vector:
    def __init__(self, *args):
        self.args = args
    def __add__(self, other):
        if len(self.args) != len(other.args):
            raise ValueError("Vectors must be in the same dimension")
        return Vector(*(a+b for a, b in zip(self.args, other.args)))
    def __sub__(self, other):
        if len(self.args) != len(other.args):
            raise ValueError("Vectors must be in the same dimension")
        return Vector(*(a - b for a , b in zip(self.args, other.args)))
    def __mul__(self, other):
        if isinstance(other, Vector):
            if len(self.args) != len(other.args):
                raise ValueError("Vectors must be of same dimension for dot product")
            return sum(a * b for a, b in zip(self.args, other.args))
        elif isinstance(other, (int, float)):
            return Vector(*(other * x for x in self.args))
        else:
            raise TypeError("Unsupported operand types")
    def __rmul__(self, other):
        return self.__mul__(other)

    def magnitude(self):
        return math.sqrt(sum(x ** 2 for x in self.args))
    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize a zero vector")
        return Vector(*(x / mag for x in self.args))
    def __str__(self):
        return f"Vector({', '.join(str(x) for x in self.args)})"
v1 = Vector(1, 2, 3)
v2 = Vector(4, 5, 6)
print(v1)
v3 = v1 + v2
print(v3) 
v4 = v2 - v1
print(v4)
dot_product = v1 * v2
print(dot_product)
v5 = 3 * v1
print(v5) 
print(v1.magnitude())
v_unit = v1.normalize()
print(v_unit) 


# Employee Records Manager (OOP Version)
class Employee:
    def __init__(self, employee_id, name, position, salary):
        self.employee_id = employee_id
        self.name = name
        self.position = position
        self.salary = float(salary)  # Ensures numeric sorting

    def __str__(self):
        return f"{self.employee_id}, {self.name}, {self.position}, {self.salary}"

    def to_line(self):
        return f"{self.employee_id}|{self.name}|{self.position}|{self.salary}"

    @staticmethod
    def from_line(line):
        try:
            parts = line.strip().split("|")
            if len(parts) != 4:
                raise ValueError("Invalid line format.")
            return Employee(parts[0], parts[1], parts[2], parts[3])
        except Exception as e:
            raise ValueError(f"Failed to parse employee: {e}")

class EmployeeManager:
    def __init__(self, filename="employees.txt"):
        self.filename = filename
        try:
            open(self.filename, "a").close()
        except Exception as e:
            raise Exception(f"Error initializing file: {e}")

    def load_employees(self):
        try:
            with open(self.filename, "r") as file:
                return [Employee.from_line(line) for line in file if line.strip()]
        except FileNotFoundError:
            return []
        except Exception as e:
            raise Exception(f"Error loading employees: {e}")

    def save_employees(self, employees):
        try:
            with open(self.filename, "w") as file:
                for emp in employees:
                    file.write(emp.to_line() + "\n")
        except Exception as e:
            raise Exception(f"Error saving employees: {e}")

    def add_employee(self):
        try:
            employee_id = input("Enter Employee ID: ").strip()
            if self.find_employee(employee_id):
                print("Employee ID already exists. Please use a unique ID.")
                return
            name = input("Enter Name: ").strip()
            position = input("Enter Position: ").strip()
            salary = input("Enter Salary: ").strip()
            if not salary.replace('.', '', 1).isdigit():
                raise ValueError("Salary must be a number.")
            new_emp = Employee(employee_id, name, position, salary)
            with open(self.filename, "a") as file:
                file.write(new_emp.to_line() + "\n")
            print("Employee added successfully!")
        except Exception as e:
            print(f"Failed to add employee: {e}")

    def view_all_employees(self):
        try:
            employees = self.load_employees()
            if not employees:
                print("No records found.")
                return
            choice = input("Sort by (1) Name or (2) Salary or (3) No sort: ").strip()
            if choice == '1':
                employees.sort(key=lambda e: e.name)
            elif choice == '2':
                employees.sort(key=lambda e: e.salary)
            print("Employee Records:")
            for emp in employees:
                print(emp)
        except Exception as e:
            print(f"Error viewing employees: {e}")

    def find_employee(self, employee_id):
        try:
            employees = self.load_employees()
            for emp in employees:
                if emp.employee_id == employee_id:
                    return emp
            return None
        except Exception as e:
            print(f"Error searching for employee: {e}")
            return None

    def search_employee(self):
        try:
            employee_id = input("Enter Employee ID to search: ").strip()
            emp = self.find_employee(employee_id)
            if emp:
                print("Employee Found:")
                print(emp)
            else:
                print("Employee not found.")
        except Exception as e:
            print(f"Error: {e}")

    def update_employee(self):
        try:
            employee_id = input("Enter Employee ID to update: ").strip()
            employees = self.load_employees()
            found = False
            for i, emp in enumerate(employees):
                if emp.employee_id == employee_id:
                    found = True
                    print(f"Current info: {emp}")
                    name = input("Enter new name (leave blank to keep current): ").strip()
                    position = input("Enter new position: ").strip()
                    salary = input("Enter new salary: ").strip()
                    if name:
                        emp.name = name
                    if position:
                        emp.position = position
                    if salary:
                        if not salary.replace('.', '', 1).isdigit():
                            raise ValueError("Salary must be numeric.")
                        emp.salary = float(salary)
                    employees[i] = emp
                    break
            if found:
                self.save_employees(employees)
                print("Employee updated successfully.")
            else:
                print("Employee not found.")
        except Exception as e:
            print(f"Error updating employee: {e}")

    def delete_employee(self):
        try:
            employee_id = input("Enter Employee ID to delete: ").strip()
            employees = self.load_employees()
            new_employees = [emp for emp in employees if emp.employee_id != employee_id]
            if len(employees) == len(new_employees):
                print("Employee ID not found.")
                return
            self.save_employees(new_employees)
            print("Employee deleted successfully.")
        except Exception as e:
            print(f"Error deleting employee: {e}")

    def run(self):
        while True:
            print("\n--- Employee Records Manager ---")
            print("1. Add new employee record")
            print("2. View all employee records")
            print("3. Search for an employee by Employee ID")
            print("4. Update an employee's information")
            print("5. Delete an employee record")
            print("6. Exit")
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                self.add_employee()
            elif choice == '2':
                self.view_all_employees()
            elif choice == '3':
                self.search_employee()
            elif choice == '4':
                self.update_employee()
            elif choice == '5':
                self.delete_employee()
            elif choice == '6':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 6.")
if __name__ == "__main__":
    manager = EmployeeManager()
    manager.run()
    

# To-Do Application
import csv
import json
from datetime import datetime

class Task:
    def __init__(self, task_id, title, description, due_date=None, status="Pending"):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date  # string YYYY-MM-DD or None
        self.status = status

    def __str__(self):
        return f"{self.task_id}, {self.title}, {self.description}, {self.due_date or 'N/A'}, {self.status}"

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data["task_id"],
            data["title"],
            data["description"],
            data.get("due_date"),
            data["status"]
        )


# Abstract storage interface
class TaskStorage:
    def save(self, tasks, filename):
        raise NotImplementedError

    def load(self, filename):
        raise NotImplementedError


# CSV Storage implementation
class CSVStorage(TaskStorage):
    def save(self, tasks, filename):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["task_id", "title", "description", "due_date", "status"])
            writer.writeheader()
            for task in tasks:
                writer.writerow(task.to_dict())

    def load(self, filename):
        tasks = []
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tasks.append(Task.from_dict(row))
        return tasks


# JSON Storage implementation
class JSONStorage(TaskStorage):
    def save(self, tasks, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump([task.to_dict() for task in tasks], file, indent=4)

    def load(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return [Task.from_dict(item) for item in data]


# Factory method for storage
def get_storage(format_name):
    format_name = format_name.lower()
    if format_name == 'csv':
        return CSVStorage()
    elif format_name == 'json':
        return JSONStorage()
    else:
        raise ValueError(f"Unsupported storage format: {format_name}")


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        if any(t.task_id == task.task_id for t in self.tasks):
            print("Task ID already exists. Use a unique Task ID.")
            return
        self.tasks.append(task)
        print("Task added successfully!")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks to show.")
            return
        print("Tasks:")
        for task in self.tasks:
            print(task)

    def update_task(self, task_id, **updates):
        for task in self.tasks:
            if task.task_id == task_id:
                for key, value in updates.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                print("Task updated successfully!")
                return
        print("Task ID not found.")

    def delete_task(self, task_id):
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                del self.tasks[i]
                print("Task deleted successfully!")
                return
        print("Task ID not found.")

    def filter_tasks(self, status):
        filtered = [task for task in self.tasks if task.status.lower() == status.lower()]
        if not filtered:
            print(f"No tasks with status '{status}'.")
            return
        print(f"Tasks with status '{status}':")
        for task in filtered:
            print(task)

    def save_tasks(self, format_name, filename):
        try:
            storage = get_storage(format_name)
            storage.save(self.tasks, filename)
            print(f"Tasks saved to {filename} in {format_name.upper()} format.")
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def load_tasks(self, format_name, filename):
        try:
            storage = get_storage(format_name)
            self.tasks = storage.load(filename)
            print(f"Tasks loaded from {filename} in {format_name.upper()} format.")
        except Exception as e:
            print(f"Error loading tasks: {e}")


def get_task_input():
    task_id = input("Enter Task ID: ").strip()
    title = input("Enter Title: ").strip()
    description = input("Enter Description: ").strip()
    due_date = input("Enter Due Date (YYYY-MM-DD, optional): ").strip()
    if due_date == "":
        due_date = None
    else:
        # Validate date format loosely
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Setting due date to None.")
            due_date = None
    status = input("Enter Status (Pending/In Progress/Completed): ").strip()
    if status not in ["Pending", "In Progress", "Completed"]:
        print("Invalid status. Setting status to 'Pending'.")
        status = "Pending"
    return Task(task_id, title, description, due_date, status)


def main():
    task_manager = TaskManager()
    print("Welcome to the To-Do Application!")

    while True:
        print("""
1. Add a new task
2. View all tasks
3. Update a task
4. Delete a task
5. Filter tasks by status
6. Save tasks
7. Load tasks
8. Exit
        """)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            task = get_task_input()
            task_manager.add_task(task)
        elif choice == "2":
            task_manager.view_tasks()
        elif choice == "3":
            task_id = input("Enter Task ID to update: ").strip()
            field = input("Enter field to update (title, description, due_date, status): ").strip()
            if field not in ["title", "description", "due_date", "status"]:
                print("Invalid field.")
                continue
            value = input(f"Enter new value for {field}: ").strip()
            if field == "due_date" and value != "":
                try:
                    datetime.strptime(value, "%Y-%m-%d")
                except ValueError:
                    print("Invalid date format.")
                    continue
            if field == "status" and value not in ["Pending", "In Progress", "Completed"]:
                print("Invalid status value.")
                continue
            task_manager.update_task(task_id, **{field: value})
        elif choice == "4":
            task_id = input("Enter Task ID to delete: ").strip()
            task_manager.delete_task(task_id)
        elif choice == "5":
            status = input("Enter status to filter by (Pending/In Progress/Completed): ").strip()
            task_manager.filter_tasks(status)
        elif choice == "6":
            format_name = input("Enter format to save (csv/json): ").strip()
            filename = input("Enter filename to save to: ").strip()
            task_manager.save_tasks(format_name, filename)
        elif choice == "7":
            format_name = input("Enter format to load (csv/json): ").strip()
            filename = input("Enter filename to load from: ").strip()
            task_manager.load_tasks(format_name, filename)
        elif choice == "8":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
