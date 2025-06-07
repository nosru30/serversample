from fastapi import FastAPI
from .routers import tasks  # Assuming tasks.py is in routers folder

app = FastAPI()

app.include_router(tasks.router)


@app.get("/")
async def root():
    return {"message": "ToDo API is running"}
