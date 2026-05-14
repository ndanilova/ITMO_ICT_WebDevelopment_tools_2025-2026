from datetime import datetime, timezone
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from db.models.task import Task

class TaskTag(SQLModel, table=True):
    task_id: Optional[int] = Field(
        default=None, foreign_key="task.id", primary_key=True
    )
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    added_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskTagCreate(SQLModel):
    task_id: int
    tag_id: int


class TaskTagUpdate(SQLModel):
    added_at: Optional[datetime] = None


class TaskTagPublic(SQLModel):
    task_id: int
    tag_id: int
    added_at: datetime

# base class
class TagBase(SQLModel):
    name: str

# takes fields from superclass
class TagCreate(TagBase):
    pass

# all fields are optional for correct update
class TagUpdate(SQLModel):
    name: Optional[str] = None

# for ORM
class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    tasks: List["Task"] = Relationship(back_populates="tags", link_model=TaskTag)

# for API response
class TagPublic(TagBase):
    id: int
