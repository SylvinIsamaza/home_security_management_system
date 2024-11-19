from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SecurityAlertBase(BaseModel):
    alert_type: str
    resolved: Optional[bool] = False

class SecurityAlertCreate(SecurityAlertBase):
    pass

class SecurityAlert(SecurityAlertBase):
    id: int
    timestamp: datetime
    device_id: int

    class Config:
        orm_mode = True