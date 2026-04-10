from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from sqlmodel import select
from db.models.task import Task, TaskCreate, TaskUpdate, TaskPublic, TaskFull

from api.deps import get_session

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskPublic)
def create_task(task: TaskCreate, session: Session = Depends(get_session)) -> TaskPublic:
    db_task = Task.model_validate(task)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.get("/", response_model=List[TaskPublic])
def get_tasks(session: Session = Depends(get_session)) -> List[TaskPublic]:
    tasks = session.exec(select(Task)).all()
    return tasks

@router.get("/{task_id}", response_model=TaskFull)
def get_task(task_id: int, session: Session = Depends(get_session)) -> TaskFull:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task



@router.patch("/{task_id}", response_model=TaskPublic)
def update_task(
    task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)
) -> TaskPublic:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)) -> dict[str, str]:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()

    return {"message": "Task deleted"}