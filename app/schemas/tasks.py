from uuid import UUID
from datetime import date
from pydantic import BaseModel

from enums.tasks import ImportanceStatusTask

class TaskSchema(BaseModel):
    name: str
    description: str | None = None
    finished_date: date
    importance_status: ImportanceStatusTask = ImportanceStatusTask.first_level
    complete_status: bool = False

class CreateTaskSchema(TaskSchema):
    user_id: UUID

class ReadTaskSchema(TaskSchema):
    class Config:
        from_attributes = True

class UpdateTaskSchema(TaskSchema):
    pass