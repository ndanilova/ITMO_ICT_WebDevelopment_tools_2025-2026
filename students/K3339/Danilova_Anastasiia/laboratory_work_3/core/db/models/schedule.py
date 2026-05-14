from datetime import datetime, timezone
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from db.models.mixins import TimestampMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.models.task import Task
    from db.models.user import User

# base class
class ScheduleDayBase(SQLModel):
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# takes fields from superclass
class ScheduleDayCreate(ScheduleDayBase):
    user_id: Optional[int] = None

# all fields are optional for correct update
class ScheduleDayUpdate(ScheduleDayBase):
    date: Optional[datetime] = None

# for ORM
class ScheduleDay(ScheduleDayBase, TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="schedule_days")

    schedule_items: List["ScheduleItem"] = Relationship(
        back_populates="schedule_day", sa_relationship_kwargs={"cascade": "all, delete"}
    )

# for API response
class ScheduleDayPublic(ScheduleDayBase):
    id: int
    user_id: Optional[int] = None
    date: Optional[datetime] = None

# base class
class ScheduleItemBase(SQLModel):
    title: str
    start_time: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = None

# takes fields from superclass
class ScheduleItemCreate(ScheduleItemBase):
    schedule_day_id: Optional[int] = None
    task_id: Optional[int] = None

# all fields are optional for correct update
class ScheduleItemUpdate(SQLModel):
    title: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

# for ORM
class ScheduleItem(ScheduleItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    schedule_day_id: Optional[int] = Field(default=None, foreign_key="scheduleday.id")
    schedule_day: Optional[ScheduleDay] = Relationship(back_populates="schedule_items")

    task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    task: Optional["Task"] = Relationship(back_populates="schedule_items")

# for API response
class ScheduleItemPublic(ScheduleItemBase):
    id: int
    schedule_day_id: Optional[int] = None
    task_id: Optional[int] = None
