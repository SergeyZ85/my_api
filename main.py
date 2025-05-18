

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
from schemas import TaskCreate, Task, TaskUpdate
from crud import create_task_service, get_task, update_task, delete_task, get_tasks

# Создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks/")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task_service(db=db, task=task.dict())

@app.get("/tasks/")
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = get_tasks(db, skip=skip, limit=limit)
    return tasks

@app.get("/tasks/{task_id}")
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
@app.put("/tasks/{task_id}", response_model=Task)
def update_existing_task(task_id: int, task:TaskUpdate, db: Session = Depends(get_db)):
    """
    Обновление существующей задачи
    """
    db_task = update_task(db, task_id=task_id, task_data=task.dict(exclude_unset=True))
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}")
def delete_existing_task(task_id: int, db: Session = Depends(get_db)):
    """
    Удаление задачи
    """
    success = delete_task(db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}