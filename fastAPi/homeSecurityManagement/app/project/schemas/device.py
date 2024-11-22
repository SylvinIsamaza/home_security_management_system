from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
from .alert import SecurityAlert

class DeviceBase(BaseModel):
    name: str
    device_type: str
    location: str

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    owner_id: str 
    alerts: List[SecurityAlert] = []  

    class Config:
        orm_mode = True
