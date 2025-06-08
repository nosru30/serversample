import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import tasks

app = FastAPI()

# Configure CORS based on the optional CORS_ALLOW_ORIGINS environment
# variable. When unset or set to "*", any origin is allowed. The variable
# may contain a comma-separated list of origins.
origins_env = os.getenv("CORS_ALLOW_ORIGINS", "*")
if origins_env == "*" or not origins_env:
    origins = ["*"]
else:
    origins = [o.strip() for o in origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)


@app.get("/")
async def root():
    return {"message": "ToDo API is running"}
