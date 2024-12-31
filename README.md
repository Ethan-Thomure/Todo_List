# Todo_List
A project via Hyperskill using Python and sqlalchemy

Program is a text interface with 7 options that will be printed in this fashion:
1) Today's Tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add a task
6) Delete a task
0) Exit

The program also creats a database file called todo.db

The two main files in the program are:
-  todolist.py
    *  contains the class ToDoList and is the main entrypoint to the program
    *  the class contains all the functions of which would be called directly from the text interface
    *  the class also initiates the database connection via sqlalchemy
-  task.py
    *  contains the class Task, which inherits from a variable made by sqlalchemy.orm.declarative_base()
    *  consists of 4 variables:
        +  __tablename__
        +  id (Integer, primary_key=True)
        +  task (VARCHAR)
        +  deadline (DATE, default=datetime.date.today())
    *  The variables are mapped to the database thanks to the inheriting from the declarative_base
    *  consists of one function: __repr__, which returns task
