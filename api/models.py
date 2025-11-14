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
    
class Note:

    def __init__(self, note_id, user_id, content, created_at, modified_at):

        self.note_id = note_id
        self.user_id = user_id
        self.content = content
        self.created_at = created_at
        self.modified_at = modified_at
    
    def to_dict(self):
        return {
            "note_id": self.note_id,
            "user_id": self.user_id,
            "content": self.content,
            "created_at": self.created_at,
            "modified_at": self.modified_at
        }
    

        
        