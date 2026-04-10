from datetime import datetime
from enum import Enum
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from db.models.mixins import TimestampMixin

from db.models.tag import TaskTag

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.models.notification import Notification
    from db.models.schedule import ScheduleItem
    from db.models.tag import Tag
    from db.models.timelog import TimeLog
    from db.models.user import User



class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


# base class
class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    priority: Priority = Field(default=Priority.LOW)
    status: Status = Status.TODO
    deadline: Optional[datetime] = None


# takes fields from superclass
class TaskCreate(TaskBase):
    user_id: Optional[int] = None


# all fields are optional for correct update
class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[Status] = None
    deadline: Optional[datetime] = None


# for ORM
class Task(TaskBase, TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="tasks")

    # relationships
    time_logs: List["TimeLog"] = Relationship(
        back_populates="task", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    notifications: List["Notification"] = Relationship(
        back_populates="task", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    schedule_items: List["ScheduleItem"] = Relationship(
        back_populates="task", sa_relationship_kwargs={"cascade": "all, delete"}
    )

    tags: List["Tag"] = Relationship(back_populates="tasks", link_model=TaskTag)


# for API response
class TaskPublic(TaskBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime


# for inner entities
class TaskFull(TaskPublic):
    time_logs: List["TimeLog"] = []
    tags: List["Tag"] = []

