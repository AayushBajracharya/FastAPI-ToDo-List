from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.users.routes import router as users_router
from app.auth.routes import router as auth_router
from app.todo.routes import router as todo_router
from sqlmodel import SQLModel
from config import engine

app = FastAPI()

# Create database tables
SQLModel.metadata.create_all(engine)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(todo_router)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
