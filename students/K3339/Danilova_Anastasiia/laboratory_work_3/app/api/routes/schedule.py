from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from api.deps import get_session
from db.models.schedule import (
    ScheduleDay,
    ScheduleDayCreate,
    ScheduleDayPublic,
    ScheduleDayUpdate,
    ScheduleItem,
    ScheduleItemCreate,
    ScheduleItemPublic,
    ScheduleItemUpdate,
)


router = APIRouter(prefix="/schedule", tags=["Schedule"])


@router.post("/days", response_model=ScheduleDayPublic)
def create_schedule_day(
    schedule_day: ScheduleDayCreate, session: Session = Depends(get_session)
) -> ScheduleDayPublic:
    db_schedule_day = ScheduleDay.model_validate(schedule_day)
    session.add(db_schedule_day)
    session.commit()
    session.refresh(db_schedule_day)
    return db_schedule_day


@router.get("/days", response_model=List[ScheduleDayPublic])
def get_schedule_days(session: Session = Depends(get_session)) -> List[ScheduleDayPublic]:
    return session.exec(select(ScheduleDay)).all()


@router.get("/days/{schedule_day_id}", response_model=ScheduleDayPublic)
def get_schedule_day(schedule_day_id: int, session: Session = Depends(get_session)) -> ScheduleDayPublic:
    schedule_day = session.get(ScheduleDay, schedule_day_id)
    if not schedule_day:
        raise HTTPException(status_code=404, detail="Schedule day not found")
    return schedule_day


@router.patch("/days/{schedule_day_id}", response_model=ScheduleDayPublic)
def update_schedule_day(
    schedule_day_id: int,
    schedule_day_update: ScheduleDayUpdate,
    session: Session = Depends(get_session),
) -> ScheduleDayPublic:
    schedule_day = session.get(ScheduleDay, schedule_day_id)
    if not schedule_day:
        raise HTTPException(status_code=404, detail="Schedule day not found")

    for key, value in schedule_day_update.model_dump(exclude_unset=True).items():
        setattr(schedule_day, key, value)

    session.add(schedule_day)
    session.commit()
    session.refresh(schedule_day)
    return schedule_day


@router.delete("/days/{schedule_day_id}")
def delete_schedule_day(schedule_day_id: int, session: Session = Depends(get_session)) -> dict[str, str]:
    schedule_day = session.get(ScheduleDay, schedule_day_id)
    if not schedule_day:
        raise HTTPException(status_code=404, detail="Schedule day not found")

    session.delete(schedule_day)
    session.commit()
    return {"message": "Schedule day deleted"}


@router.post("/items", response_model=ScheduleItemPublic)
def create_schedule_item(
    schedule_item: ScheduleItemCreate, session: Session = Depends(get_session)
) -> ScheduleItemPublic:
    db_schedule_item = ScheduleItem.model_validate(schedule_item)
    session.add(db_schedule_item)
    session.commit()
    session.refresh(db_schedule_item)
    return db_schedule_item


@router.get("/items", response_model=List[ScheduleItemPublic])
def get_schedule_items(session: Session = Depends(get_session)) -> List[ScheduleItemPublic]:
    return session.exec(select(ScheduleItem)).all()


@router.get("/items/{schedule_item_id}", response_model=ScheduleItemPublic)
def get_schedule_item(schedule_item_id: int, session: Session = Depends(get_session)) -> ScheduleItemPublic:
    schedule_item = session.get(ScheduleItem, schedule_item_id)
    if not schedule_item:
        raise HTTPException(status_code=404, detail="Schedule item not found")
    return schedule_item


@router.patch("/items/{schedule_item_id}", response_model=ScheduleItemPublic)
def update_schedule_item(
    schedule_item_id: int,
    schedule_item_update: ScheduleItemUpdate,
    session: Session = Depends(get_session),
) -> ScheduleItemPublic:
    schedule_item = session.get(ScheduleItem, schedule_item_id)
    if not schedule_item:
        raise HTTPException(status_code=404, detail="Schedule item not found")

    for key, value in schedule_item_update.model_dump(exclude_unset=True).items():
        setattr(schedule_item, key, value)

    session.add(schedule_item)
    session.commit()
    session.refresh(schedule_item)
    return schedule_item


@router.delete("/items/{schedule_item_id}")
def delete_schedule_item(schedule_item_id: int, session: Session = Depends(get_session)) -> dict[str, str]:
    schedule_item = session.get(ScheduleItem, schedule_item_id)
    if not schedule_item:
        raise HTTPException(status_code=404, detail="Schedule item not found")

    session.delete(schedule_item)
    session.commit()
    return {"message": "Schedule item deleted"}
