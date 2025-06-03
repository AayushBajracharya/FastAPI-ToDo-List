from fastapi import FastAPI
from app.users.routes import router as users_router
from sqlmodel import SQLModel
from config import engine

app = FastAPI()

# Create database tables
SQLModel.metadata.create_all(engine)

app.include_router(users_router)

@app.get("/")
def initial():
    return {"Hello World!!"}
