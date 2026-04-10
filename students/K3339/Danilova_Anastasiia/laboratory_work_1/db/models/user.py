from datetime import datetime
from typing import Optional, List

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

from db.models.mixins import TimestampMixin

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from db.models.notification import Notification
    from db.models.schedule import ScheduleDay
    from db.models.tag import Tag
    from db.models.task import Task

# base class
class UserBase(SQLModel):
    name: str
    email: EmailStr = Field(unique=True, index=True)

# takes fields from superclass
class UserCreate(UserBase):
    password: str

# all fields are optional for correct update
class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None


class UserLogin(SQLModel):
    email: EmailStr
    password: str


class PasswordChange(SQLModel):
    current_password: str
    new_password: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

# for ORM
class User(UserBase, TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_active: bool = Field(default=True)

    hashed_password: str

    # relations
    tasks: List["Task"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    notifications: List["Notification"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    schedule_days: List["ScheduleDay"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )

# for API response
class UserPublic(UserBase):
    id: int
    created_at: datetime

# for inner entities
class UserWithTasks(UserPublic):
    tasks: List["Task"] = []
