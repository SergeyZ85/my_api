from sqlalchemy.orm import Session

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: dict):
    db_task = Task(**task)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task