from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True  


class User(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        orm_mode = True 
