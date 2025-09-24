from fastapi import FastAPI
from app.db.database import engine, Base, get_db, Session
from app.v1.endpoints.authentication import user_router
from app.v1.endpoints.todos import todo_routers

app = FastAPI(title="AI application")
Base.metadata.create_all(engine)

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(todo_routers, prefix="/todos", tags=["todos"])
