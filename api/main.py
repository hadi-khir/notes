from fastapi import FastAPI, HTTPException

from database import add_note, add_user, create_tables, get_notes_by_user_id, get_user_by_username, update_note_by_note_id_and_user_id
from models import Note, User

app = FastAPI() 
create_tables()

@app.post("/api/users", response_model=User, response_model_exclude={"password"})
async def create_user(username: str, password: str, email: str) -> User:
    user: User = add_user(username, password, email)
    return User(**user)

@app.get("/api/users/{username}", response_model=User, response_model_exclude={"password"})
async def get_user(username: str) -> User:
    user: User = get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user)

@app.post("/api/notes", response_model=Note)
async def create_note(content: str, user_id: int):

    note: Note = add_note(user_id=user_id, content=content)
    return Note(**note)

@app.get("/api/notes/user/{user_id}", response_model=list[Note])
async def get_notes_by_user(user_id: int):
    db_notes: list[Note] = get_notes_by_user_id(user_id)
    if len(db_notes) == 0: 
        raise HTTPException(status_code=404, detail=f"No notes found for user ID: {user_id}")
    
    notes = []
    for note in db_notes:
        notes.append(Note(**note))
    
    return notes

@app.put("/api/notes/{note_id}", response_model=Note)
async def update_note(note_id: int, user_id: int, content: str):
    note: Note = update_note_by_note_id_and_user_id(note_id, user_id, content)
    return note

