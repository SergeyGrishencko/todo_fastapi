import uvicorn

from fastapi import FastAPI

from routers.tasks import task_router
from routers.users import user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(task_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)