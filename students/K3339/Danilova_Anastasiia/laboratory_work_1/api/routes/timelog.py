from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from api.deps import get_session
from db.models.timelog import TimeLog, TimeLogCreate, TimeLogPublic, TimeLogUpdate


router = APIRouter(prefix="/time-logs", tags=["TimeLogs"])


@router.post("/", response_model=TimeLogPublic)
def create_time_log(time_log: TimeLogCreate, session: Session = Depends(get_session)) -> TimeLogPublic:
    db_time_log = TimeLog.model_validate(time_log)
    session.add(db_time_log)
    session.commit()
    session.refresh(db_time_log)
    return db_time_log


@router.get("/", response_model=List[TimeLogPublic])
def get_time_logs(session: Session = Depends(get_session)) -> List[TimeLogPublic]:
    return session.exec(select(TimeLog)).all()


@router.get("/{time_log_id}", response_model=TimeLogPublic)
def get_time_log(time_log_id: int, session: Session = Depends(get_session)) -> TimeLogPublic:
    time_log = session.get(TimeLog, time_log_id)
    if not time_log:
        raise HTTPException(status_code=404, detail="Time log not found")
    return time_log


@router.patch("/{time_log_id}", response_model=TimeLogPublic)
def update_time_log(
    time_log_id: int,
    time_log_update: TimeLogUpdate,
    session: Session = Depends(get_session),
) -> TimeLogPublic:
    time_log = session.get(TimeLog, time_log_id)
    if not time_log:
        raise HTTPException(status_code=404, detail="Time log not found")

    for key, value in time_log_update.model_dump(exclude_unset=True).items():
        setattr(time_log, key, value)

    session.add(time_log)
    session.commit()
    session.refresh(time_log)
    return time_log


@router.delete("/{time_log_id}")
def delete_time_log(time_log_id: int, session: Session = Depends(get_session)) -> dict[str, str]:
    time_log = session.get(TimeLog, time_log_id)
    if not time_log:
        raise HTTPException(status_code=404, detail="Time log not found")

    session.delete(time_log)
    session.commit()
    return {"message": "Time log deleted"}
