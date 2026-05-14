from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api.deps import get_session
from core.db.models.tag import Tag, TagCreate, TagPublic, TagUpdate


router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", response_model=TagPublic)
def create_tag(tag: TagCreate, session: Session = Depends(get_session)) -> TagPublic:
    db_tag = Tag.model_validate(tag)
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag


@router.get("/", response_model=List[TagPublic])
def get_tags(session: Session = Depends(get_session)) -> List[TagPublic]:
    return session.exec(select(Tag)).all()


@router.get("/{tag_id}", response_model=TagPublic)
def get_tag(tag_id: int, session: Session = Depends(get_session)) -> TagPublic:
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.patch("/{tag_id}", response_model=TagPublic)
def update_tag(tag_id: int, tag_update: TagUpdate, session: Session = Depends(get_session)) -> TagPublic:
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    for key, value in tag_update.model_dump(exclude_unset=True).items():
        setattr(tag, key, value)

    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


@router.delete("/{tag_id}")
def delete_tag(tag_id: int, session: Session = Depends(get_session)) -> dict[str, str]:
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    session.delete(tag)
    session.commit()
    return {"message": "Tag deleted"}
