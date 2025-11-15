from pydantic import BaseModel


class User(BaseModel):
    
    username: str
    user_id: int
    email: str
    password: str

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
        }
    
class Note(BaseModel):

    note_id: int
    user_id: int
    content: str
    created_at: str
    modified_at: str
    
    def to_dict(self):
        return {
            "note_id": self.note_id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at,
            "modified_at": self.modified_at
        }
    

        
        