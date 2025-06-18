from uuid import UUID
from sqlalchemy import insert, select, update, delete

from models.task import Task
from backend.session import async_session_maker

class TasksService:
    model = Task

    @classmethod
    async def create_task(cls, created_task_data: dict):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**created_task_data)
            await session.execute(stmt)
            await session.commit()
    
    @classmethod
    async def get_task_or_none(cls, task_id: UUID):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=task_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def get_all_tasks(cls, user_id: UUID):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(user_id=user_id)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def update_task(cls, update_task_data: dict):
        async with async_session_maker() as session:
            stmt = update(cls.model).values(**update_task_data)
            await session.execute(stmt)
            await session.commit()
    
    @classmethod
    async def complete_task(cls, complete_status: bool):
        async with async_session_maker() as session:
            stmt = update(cls.model).values(complete_status=complete_status)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def delete_task(cls, task_id: UUID):
        async with async_session_maker() as session:
            stmt = delete(cls.model).filter_by(id=task_id)
            await session.execute(stmt)
            await session.commit()