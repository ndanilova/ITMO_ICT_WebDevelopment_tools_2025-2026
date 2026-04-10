from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from api.deps import get_session
from db.models.tag import TaskTag, TaskTagCreate, TaskTagPublic, TaskTagUpdate


router = APIRouter(prefix="/task-tags", tags=["TaskTags"])


@router.post("/", response_model=TaskTagPublic)
def create_task_tag(payload: TaskTagCreate, session: Session = Depends(get_session)) -> TaskTagPublic:
    existing = session.get(TaskTag, (payload.task_id, payload.tag_id))
    if existing:
        raise HTTPException(status_code=400, detail="Task-tag relation already exists")

    task_tag = TaskTag.model_validate(payload)
    session.add(task_tag)
    session.commit()
    session.refresh(task_tag)
    return task_tag


@router.get("/", response_model=List[TaskTagPublic])
def get_task_tags(session: Session = Depends(get_session)) -> List[TaskTagPublic]:
    return session.exec(select(TaskTag)).all()


@router.get("/{task_id}/{tag_id}", response_model=TaskTagPublic)
def get_task_tag(task_id: int, tag_id: int, session: Session = Depends(get_session)) -> TaskTagPublic:
    task_tag = session.get(TaskTag, (task_id, tag_id))
    if not task_tag:
        raise HTTPException(status_code=404, detail="Task-tag relation not found")
    return task_tag


@router.patch("/{task_id}/{tag_id}", response_model=TaskTagPublic)
def update_task_tag(
    task_id: int,
    tag_id: int,
    payload: TaskTagUpdate,
    session: Session = Depends(get_session),
) -> TaskTagPublic:
    task_tag = session.get(TaskTag, (task_id, tag_id))
    if not task_tag:
        raise HTTPException(status_code=404, detail="Task-tag relation not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(task_tag, key, value)

    session.add(task_tag)
    session.commit()
    session.refresh(task_tag)
    return task_tag


@router.delete("/{task_id}/{tag_id}")
def delete_task_tag(task_id: int, tag_id: int, session: Session = Depends(get_session)) -> dict[str, str]:
    task_tag = session.get(TaskTag, (task_id, tag_id))
    if not task_tag:
        raise HTTPException(status_code=404, detail="Task-tag relation not found")

    session.delete(task_tag)
    session.commit()
    return {"message": "Task-tag relation deleted"}
