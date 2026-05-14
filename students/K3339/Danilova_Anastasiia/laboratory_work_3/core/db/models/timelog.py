from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.db.models.task import Task
    
# base class
class TimeLogBase(SQLModel):
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[int] = None  # in minutes

# takes fields from superclass
class TimeLogCreate(TimeLogBase):
    task_id: int

# all fields are optional for correct update
class TimeLogUpdate(SQLModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None

# for ORM
class TimeLog(TimeLogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    task_id: int = Field(foreign_key="task.id")
    task: Optional["Task"] = Relationship(back_populates="time_logs")

# for API response
class TimeLogPublic(TimeLogBase):
    id: int
    task_id: int
