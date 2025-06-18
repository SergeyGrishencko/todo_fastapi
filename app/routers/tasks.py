from uuid import UUID
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends

from schemas.tasks import CreateTaskSchema, ReadTaskSchema, UpdateTaskSchema, TaskSchema
from services.tasks import TasksService
from routers.users import oauth2_scheme, get_current_user

task_router = APIRouter(
    prefix="/task",
    tags=["Задачи"],
)

@task_router.post("/create")
async def create_task(
    payload: TaskSchema,
    user_id: UUID = Depends(get_current_user),
    token: str = Depends(oauth2_scheme),
):
    create_data = CreateTaskSchema(**payload.dict(), user_id=user_id)
    await TasksService.create_task(created_task_data=create_data.model_dump())
    return "Задача создана"

@task_router.get("/all", response_model=List[ReadTaskSchema])
async def get_all_tasks(
    user_id: UUID = Depends(get_current_user),
    token: str = Depends(oauth2_scheme),
):
    result = await TasksService.get_all_tasks(user_id)
    return result

@task_router.get("/{task_id}", response_model=ReadTaskSchema)
async def get_task_by_id(
    task_id: UUID,
    token: str = Depends(oauth2_scheme),
):
    task = await TasksService.get_task_or_none(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена",
        )
    return task

@task_router.patch("/update/{task_id}", response_model=ReadTaskSchema)
async def update_task(
    task_id: UUID, 
    update_data: UpdateTaskSchema,
    token: str = Depends(oauth2_scheme),
):
    task = await TasksService.get_task_or_none(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detailt="Задача не найдена"
        )
    await TasksService.update_task(update_data.model_dump())
    return await TasksService.get_task_or_none(task_id)

@task_router.patch("/complete/{task_id}")
async def complete_task(
    task_id: UUID, 
    complete_status: bool,
    token: str = Depends(oauth2_scheme),
):
    task = await TasksService.get_task_or_none(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detailt="Задача не найдена"
        )
    await TasksService.complete_task(complete_status)

@task_router.delete("/delete/{task_id}")
async def delete_task(
    task_id: UUID,
    token: str = Depends(oauth2_scheme),
):
    await TasksService.delete_task(task_id=task_id)
    return {
        "status_code": status.HTTP_200_OK,
    }