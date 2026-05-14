from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api.deps import get_session
from core.db.models.notification import (
    Notification,
    NotificationCreate,
    NotificationPublic,
    NotificationUpdate,
)


router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.post("/", response_model=NotificationPublic)
def create_notification(
    notification: NotificationCreate, session: Session = Depends(get_session)
) -> NotificationPublic:
    db_notification = Notification.model_validate(notification)
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification


@router.get("/", response_model=List[NotificationPublic])
def get_notifications(session: Session = Depends(get_session)) -> List[NotificationPublic]:
    return session.exec(select(Notification)).all()


@router.get("/{notification_id}", response_model=NotificationPublic)
def get_notification(notification_id: int, session: Session = Depends(get_session)) -> NotificationPublic:
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


@router.patch("/{notification_id}", response_model=NotificationPublic)
def update_notification(
    notification_id: int,
    notification_update: NotificationUpdate,
    session: Session = Depends(get_session),
) -> NotificationPublic:
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    for key, value in notification_update.model_dump(exclude_unset=True).items():
        setattr(notification, key, value)

    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification


@router.delete("/{notification_id}")
def delete_notification(notification_id: int, session: Session = Depends(get_session)) -> dict[str, str]:
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    session.delete(notification)
    session.commit()
    return {"message": "Notification deleted"}
