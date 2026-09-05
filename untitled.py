# to do list 

tasks = ["cook food", "wash clothes", "wash the dishes", "clean ure room", "studying", "shower"]
print(tasks)

def task():
    while True:
        user = input("-> remove task: 'r'\n-> add task: 'a'\n-> change task: 'c'\n")

        if user == "r":
            delete = int(input("Enter the number of the task to remove: "))
            removed = tasks.pop(delete-1)
            print("Removed:", removed)
            print("Tasks:", tasks)

        elif user == "a":
            adding = input("Insert your task: ")
            insert = int(input("Enter position to insert it: "))
            tasks.insert(insert-1, adding) 
            print("Added:", adding)
            print("Tasks:", tasks)

        elif user == "c":
            change = int(input("Task number to change: "))
            changed = input("New task: ")

            old = tasks.pop(change-1)        
            tasks.insert(change-1, changed)  
            print("Changed:", old, "→", changed)
            print("Tasks:", tasks)

        else:
            print("Invalid input")

task()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            