import sys
from todo_app.services.project_manager import ProjectManager
from todo_app.services.task_manager import TaskManager
from todo_app.utils.validators import ValidationError

class TodoCLI:
    """Command-line interface for To-Do application"""
    
    def __init__(self):
        self.project_manager = ProjectManager()
        self.task_manager = TaskManager(self.project_manager)
    
    def run(self):
        """Main application loop"""
        print("=" * 60)
        print("Welcome to To-Do List Application".center(60))
        print("=" * 60)
        
        while True:
            self.display_main_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.project_menu()
            elif choice == '2':
                self.task_menu()
            elif choice == '3':
                self.list_all_projects()
            elif choice == '4':
                print("\nThank you for using To-Do List Application!")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
    
    def display_main_menu(self):
        """Display main menu"""
        print("\n" + "=" * 60)
        print("MAIN MENU")
        print("=" * 60)
        print("1. Project Management")
        print("2. Task Management")
        print("3. List All Projects")
        print("4. Exit")
    
    def project_menu(self):
        """Project management menu"""
        while True:
            print("\n" + "-" * 60)
            print("PROJECT MANAGEMENT")
            print("-" * 60)
            print("1. Create Project")
            print("2. Edit Project")
            print("3. Delete Project")
            print("4. Back to Main Menu")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.create_project()
            elif choice == '2':
                self.edit_project()
            elif choice == '3':
                self.delete_project()
            elif choice == '4':
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
    
    def task_menu(self):
        """Task management menu"""
        while True:
            print("\n" + "-" * 60)
            print("TASK MANAGEMENT")
            print("-" * 60)
            print("1. Create Task")
            print("2. Edit Task")
            print("3. Delete Task")
            print("4. List Tasks in Project")
            print("5. Back to Main Menu")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.create_task()
            elif choice == '2':
                self.edit_task()
            elif choice == '3':
                self.delete_task()
            elif choice == '4':
                self.list_tasks()
            elif choice == '5':
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
    
    def create_project(self):
        """Create a new project"""
        try:
            print("\n--- Create New Project ---")
            name = input("Enter project name: ").strip()
            description = input("Enter project description (optional): ").strip()
            
            description = description if description else None
            project = self.project_manager.create_project(name, description)
            
            print(f"\n✓ Project created successfully! (ID: {project.id})")
        except ValidationError as e:
            print(f"\n❌ Error: {e}")
    
    def edit_project(self):
        """Edit an existing project"""
        try:
            self.list_all_projects()
            project_id = int(input("\nEnter project ID to edit: "))
            
            print("\nLeave blank to keep current value")
            name = input("Enter new project name: ").strip()
            description = input("Enter new description: ").strip()
            
            name = name if name else None
            description = description if description else None
            
            project = self.project_manager.edit_project(project_id, name, description)
            print(f"\n✓ Project updated successfully!")
        except (ValidationError, ValueError) as e:
            print(f"\n❌ Error: {e}")
    
    def delete_project(self):
        """Delete a project"""
        try:
            self.list_all_projects()
            project_id = int(input("\nEnter project ID to delete: "))
            
            confirm = input(f"Are you sure you want to delete project {project_id}? (yes/no): ").strip().lower()
            if confirm == 'yes':
                self.project_manager.delete_project(project_id)
                print(f"\n✓ Project deleted successfully!")
            else:
                print("\n❌ Deletion cancelled.")
        except (ValidationError, ValueError) as e:
            print(f"\n❌ Error: {e}")
    
    def create_task(self):
        """Create a new task"""
        try:
            self.list_all_projects()
            project_id = int(input("\nEnter project ID: "))
            
            print("\n--- Create New Task ---")
            title = input("Enter task title: ").strip()
            description = input("Enter task description (optional): ").strip()
            status = input("Enter status (to-do/doing/done) [default: to-do]: ").strip()
            deadline = input("Enter deadline (YYYY-MM-DD): ").strip()
            
            description = description if description else None
            status = status if status else 'to-do'
            
            task = self.task_manager.create_task(project_id, title, deadline, description, status)
            print(f"\n✓ Task created successfully! (ID: {task.id})")
        except (ValidationError, ValueError) as e:
            print(f"\n❌ Error: {e}")
    
    def edit_task(self):
        """Edit an existing task"""
        try:
            self.list_all_projects()
            project_id = int(input("\nEnter project ID: "))
            
            self.list_tasks_for_project(project_id)
            task_id = int(input("\nEnter task ID to edit: "))
            
            print("\nLeave blank to keep current value")
            title = input("Enter new title: ").strip()
            description = input("Enter new description: ").strip()
            status = input("Enter new status (to-do/doing/done): ").strip()
            deadline = input("Enter new deadline (YYYY-MM-DD): ").strip()
            
            title = title if title else None
            description = description if description else None
            status = status if status else None
            deadline = deadline if deadline else None
            
            task = self.task_manager.edit_task(project_id, task_id, title, description, status, deadline)
            print(f"\n✓ Task updated successfully!")
        except (ValidationError, ValueError) as e:
            print(f"\n❌ Error: {e}")
    
    def delete_task(self):
        """Delete a task"""
        try:
            self.list_all_projects()
            project_id = int(input("\nEnter project ID: "))
            
            self.list_tasks_for_project(project_id)
            task_id = int(input("\nEnter task ID to delete: "))
            
            confirm = input(f"Are you sure you want to delete task {task_id}? (yes/no): ").strip().lower()
            if confirm == 'yes':
                self.task_manager.delete_task(project_id, task_id)
                print(f"\n✓ Task deleted successfully!")
            else:
                print("\n❌ Deletion cancelled.")
        except (ValidationError, ValueError) as e:
            print(f"\n❌ Error: {e}")
    
    def list_tasks(self):
        """List tasks in a project"""
        try:
            self.list_all_projects()
            project_id = int(input("\nEnter project ID to view tasks: "))
            self.list_tasks_for_project(project_id)
        except (ValidationError, ValueError) as e:
            print(f"\n❌ Error: {e}")
    
    def list_all_projects(self):
        """List all projects"""
        projects = self.project_manager.list_projects()
        
        print("\n" + "=" * 60)
        print("ALL PROJECTS")
        print("=" * 60)
        
        if not projects:
            print("No projects found. Create your first project!")
        else:
            for project in projects:
                print(f"\nID: {project.id}")
                print(f"Name: {project.name}")
                print (f"Created at: {project.created_at}")
                print(f"Description: {project.description if project.description else 'N/A'}")
                print(f"Tasks: {len(project.tasks)}")
                print("-" * 60)
    
    def list_tasks_for_project(self, project_id: int):
        """List tasks for a specific project"""
        tasks = self.task_manager.list_tasks(project_id)
        
        print("\n" + "=" * 60)
        print(f"TASKS IN PROJECT {project_id}")
        print("=" * 60)
        
        if not tasks:
            print("No tasks found in this project.")
        else:
            for task in tasks:
                print(f"\nID: {task.id}")
                print(f"Title: {task.title}")
                print(f"Status: {task.status}")
                print(f"Deadline: {task.deadline.strftime('%Y-%m-%d')}")
                print(f"Description: {task.description if task.description else 'N/A'}")
                print("-" * 60)

def main():
    """Entry point for the application"""
    try:
        cli = TodoCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()