from sqlalchemy.orm import Session

from models import TaskDatabase


def get_task(db: Session, task_id: int):
    return db.query(TaskDatabase).filter(TaskDatabase.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    result = [{'id': res.id,
               'title': res.title,
               'description': res.description,
               'created_at': res.created_at,
               'updated_at': res.updated_at} for res in db.query(TaskDatabase).offset(skip).limit(limit).all()]
    return result


def create_task_service(db: Session, task: dict):
    db_task = TaskDatabase(**task)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_data: dict):
    db_task = db.query(TaskDatabase).filter(TaskDatabase.id == task_id).first()
    if db_task:
        for key, value in task_data.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    db_task = db.query(TaskDatabase).filter(TaskDatabase.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False
