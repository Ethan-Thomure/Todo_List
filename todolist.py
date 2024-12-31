from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Task import Base, Task
from datetime import date, timedelta, datetime


class ToDoList:

    def __init__(self):
        self.engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.menu()

    def menu(self):
        """
        a continual text user interface that has 5 options:
        1) display_today_tasks
        2) display_week_tasks
        3) display_tasks
        4) add_task
        0) termination
        """
        prompt = ("1) Today's Tasks\n"
                  "2) Week's tasks\n"
                  "3) All tasks\n"
                  "4) Missed tasks\n"
                  "5) Add a task\n"
                  "6) Delete a task\n"
                  "0) Exit\n")

        options = {
            '1': self.display_today_tasks,
            '2': self.display_week_tasks,
            '3': self.display_tasks,
            '4': self.display_missed_tasks,
            '5': self.add_task,
            '6': self.delete_task,
            '0': self.termination
        }

        while True:
            # select an input and run the key in the options dict based on that input
            options.get(input(prompt), lambda: None)()
            print()

    @staticmethod
    def print_task_day(*tasks: "Query result", display_date=False, message_if_nothing="Nothing to do!"):
        """
        given the query result of tasks, print out the tasks
        :return:
        """
        if len(tasks) == 0:
            print(message_if_nothing)
        for task in range(len(tasks)):
            task_date = f". {tasks[task].deadline.strftime('%#d %b')}" if display_date else ""
            print(f"{task + 1}. {tasks[task]}{task_date}")

    def display_today_tasks(self):
        """
        displays all of today's tasks under the 'task' table in todo.db
        """
        print(f"\nToday {date.today().strftime('%#d %b')}")
        rows = self.session.query(Task).filter(Task.deadline == date.today()).order_by(Task.deadline).all()
        self.print_task_day(*rows)

    def display_week_tasks(self):
        """
        displays all of the tasks for the next 7 days including today under the 'task' table in todo.db
        """
        # days of the week
        week = [date.today()]
        for day in range(1, 7):
            week.append(week[-1] + timedelta(days=1))

        # for each day of the week, print the day's task
        for day in week:
            print(f"\n{day.strftime('%A %#d %b')}:")
            rows = self.session.query(Task).filter(Task.deadline == day).order_by(Task.deadline).all()
            self.print_task_day(*rows)

    def display_tasks(self):
        """
        displays all of the current tasks under the 'task' table in todo.db
        """
        print("\nAll tasks:")
        rows = self.session.query(Task).order_by(Task.deadline).all()
        self.print_task_day(*rows, display_date=True)

    def display_missed_tasks(self):
        """
        displays all the tasks whose deadline was before today under the 'task' table in todo.db
        """
        print("\nMissed tasks:")
        rows = self.session.query(Task).filter(Task.deadline < date.today()).order_by(Task.deadline).all()
        self.print_task_day(*rows, display_date=True, message_if_nothing="All tasks have been completed!")

    def add_task(self):
        """
        adds a new task needing only the title of the task to the 'task' table in the todo.db file and commiting it
        """
        new_task = input("\nEnter a task\n")
        deadline = datetime.strptime(input("Enter a deadline\n"), '%Y-%m-%d')

        self.session.add(Task(task=new_task, deadline=deadline))
        self.session.commit()

    def delete_task(self):
        """
        prints all the tasks, then asks user to delete a task using the number of the order of the list
        """
        print("\nChoose the number of the task you want to delete:")
        rows = self.session.query(Task).order_by(Task.deadline).all()
        self.print_task_day(*rows, display_date=True)

        # find the id for the item mentioned in the list and delete it
        self.session.delete(rows[int(input()) - 1])
        self.session.commit()
        print("The task has been deleted!")

    def termination(self):
        """
        the 'deconstructor' without overriding it
        prints "Bye" and closes the connection to the database
        """
        print("\nBye!")
        self.session.close()
        exit()

ToDoList()
