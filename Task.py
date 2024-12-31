from sqlalchemy import Column, Integer, VARCHAR, DATE
import datetime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    task = Column(VARCHAR)
    deadline = Column(DATE, default=datetime.date.today())

    def __repr__(self):
        return self.task
