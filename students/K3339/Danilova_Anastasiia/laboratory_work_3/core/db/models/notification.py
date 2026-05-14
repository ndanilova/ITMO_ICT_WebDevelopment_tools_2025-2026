from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.models.task import Task
    from db.models.user import User


# base class
class NotificationBase(SQLModel):
    message: str
    notify_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_sent: bool = False

# takes fields from superclass
class NotificationCreate(NotificationBase):
    user_id: Optional[int] = None
    task_id: Optional[int] = None

# all fields are optional for correct update
class NotificationUpdate(SQLModel):
    message: Optional[str] = None
    notify_at: Optional[datetime] = None
    is_sent: Optional[bool] = None

# for ORM
class Notification(NotificationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="notifications")

    task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    task: Optional["Task"] = Relationship(back_populates="notifications")

# for API response
class NotificationPublic(NotificationBase):
    id: int
    user_id: Optional[int] = None
    task_id: Optional[int] = None
    notify_at: datetime
