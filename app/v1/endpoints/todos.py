from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Path
from app.db.models.todos import Todos

from app.db.database import  get_db, Session
from app.schemas.todos import TodoRequest
from app.v1.endpoints.authentication import get_current_user

todo_routers = APIRouter()

@todo_routers.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(Todos).all()


@todo_routers.get("/todos/{id}")
async def read_todo(id:int, db:Session = Depends(get_db), user = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=404, detail="Authentication failed")
    todo_model = db.query(Todos).filter(Todos.owner_id == user.get("id")).filter(Todos.id==id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found.")

@todo_routers.get("/", status_code=status.HTTP_200_OK)
async def read_todos(db:Session = Depends(get_db), user=Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=404, detail="Not authenticated")
    return db.query(Todos).filter(Todos.id==user.get('id')).all()
@todo_routers.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo( todo_request:TodoRequest,user=Depends(get_current_user) , db: Session=Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail="Authentication Failed")
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("id"))
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model

@todo_routers.put("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(todo_request:TodoRequest,id:int=Path(gt=0), db:Session=Depends(get_db), user=Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=404, detail="Authentication Failed")

    todo_model = db.query(Todos).filter(Todos.owner_id == user.get("id")).filter(Todos.id==id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

@todo_routers.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id:int, db:Session=Depends(get_db), user=Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=404, detail="Authentication Failed")

    todo_model = db.query(Todos).filter(Todos.owner_id==user.get("id")).filter(Todos.id==todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="No content Found")
    db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get("id")).delete()
    db.commit()
    return

