from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SecurityAlertBase(BaseModel):
    alert_type: str
    resolved: Optional[bool] = False
    device_id: int

class SecurityAlertCreate(SecurityAlertBase):
    pass

class SecurityAlert(SecurityAlertBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
    @staticmethod
    def json(cls, **kwargs):
        original_json = super().json(**kwargs)
        if 'timestamp' in kwargs:
            kwargs['timestamp'] = kwargs['timestamp'].isoformat()
        return original_json
