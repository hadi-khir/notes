from fastapi import FastAPI, HTTPException

from database import add_user, create_tables, get_user_by_username
from models import User

app = FastAPI() 
create_tables()

@app.post("/users", response_model=User, response_model_exclude={"password"})
async def create_user(username: str, password: str, email: str) -> User:
    user: User = add_user(username, password, email)
    return User(**user)

@app.get("/users/{username}", response_model=User, response_model_exclude={"password"})
async def get_user(username: str) -> User:
    user: User = get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user)