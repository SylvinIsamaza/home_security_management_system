from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class UserCreate(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True 


class User(BaseModel):
    id: str
    username: str
    created_at: datetime

    class Config:
        orm_mode = True  
