from fastapi import FastAPI
from .routers import tasks, db_tasks

app = FastAPI()

app.include_router(tasks.router)
app.include_router(db_tasks.router)


@app.get("/")
async def root():
    return {"message": "ToDo API is running"}
