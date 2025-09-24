import os
from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi import HTTPException

from app.db.database import get_db
from app.db.models.todos import Users, bcrypt_context
from app.schemas.todos import TodoRequest, CreateUserRequest, Token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
user_router = APIRouter()

SECRET_KEY ="239cbd90a12ce950d0293228ed3cc0eb470e77a055456a14f75083125806bfbca905cde498f8aa8f072f72b758516290e72c9f23e6b4a58b95afcc834dd6a143"
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/users/token")
@user_router.get("/auth")
async def get_user():
    return {"user":"authenticated"}

@user_router.post("/auth")
async def create_user(user: CreateUserRequest, db:Session=Depends(get_db)):
    create_user_model = Users(email=user.email, role=user.role,first_name=user.first_name, last_name=user.last_name, is_active=True, hashed_password=bcrypt_context.hash(user.password), username=user.username)
    db.add(create_user_model)
    db.commit()



async def get_current_user(token:str=Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str = payload.get("sub")
        user_id = payload.get("id")
        user_role = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        return {'username':username, 'user_id':user_id, "role":user_role}
    except JWTError:
        raise HTTPException(status_code=404, detail="Incorrect username or password")

def authenticate_user(username, password, db:Session=Depends(get_db)):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not bcrypt_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=404, detail="Incorrect password")
    return user



def create_access_token(username:str, user_id:int, expires_delta:timedelta, role:str):
    encode = {"sub":username, "exp":datetime.now(timezone.utc)+expires_delta, "id":user_id,"role":role}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@user_router.post("/token", response_model=Token)
async def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    print(form_data.username)
    if user:
        token = create_access_token(username=user.username, user_id=user.id, expires_delta=timedelta(minutes=20), role=user.role)
        return {"access_token": token, "token_type": "bearer"}
    return "Invalid credentials", 401




