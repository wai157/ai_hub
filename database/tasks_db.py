from .models import Task
from .config import SessionLocal

class Task_Mapper:
    def __init__(self, task: Task):
        if not task:
            return None
        for key, value in task.serialize().items():
            setattr(self, key, value)

def get_tasks():
    with SessionLocal() as session:
        db_tasks = session.query(Task).all()
        tasks = [Task_Mapper(task) for task in db_tasks]
        return tasks
    
def get_task(task_name):
    with SessionLocal() as session:
        db_task = session.query(Task).filter(Task.name == task_name).first()
        task = Task_Mapper(db_task)
        return task