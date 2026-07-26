from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class CommentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., min_length=1, max_length=1000)

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Comment text must not be blank")
        return cleaned


class CommentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int = Field(..., ge=1)
    text: str
    created_at: datetime


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    tag: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("title must not be blank")
        if len(stripped) > 200:
            raise ValueError("title must be at most 200 characters")
        return stripped

    @field_validator("assignee", "tag")
    @classmethod
    def clean_optional_text(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    tag: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title", "description", "status", "priority", mode="before")
    @classmethod
    def reject_null_required_fields(cls, value: object, info: ValidationInfo) -> object:
        if value is None:
            raise ValueError(f"{info.field_name} must not be null")
        return value

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        stripped = value.strip()
        if not stripped:
            raise ValueError("title must not be blank")
        if len(stripped) > 200:
            raise ValueError("title must be at most 200 characters")
        return stripped

    @field_validator("assignee", "tag")
    @classmethod
    def clean_optional_text(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    tag: Optional[str] = None
    due_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime
    comments: list[CommentResponse] = Field(default_factory=list)
    comment_count: int = Field(default=0, ge=0)
