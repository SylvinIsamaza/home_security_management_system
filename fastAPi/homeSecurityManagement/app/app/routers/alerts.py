from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..crud import alert, device
from ..schemas import SecurityAlertCreate, SecurityAlert
from ..database import get_db
from ..models import User
from typing import List,Optional
from ..utils import get_current_user

router = APIRouter()

@router.post("/", response_model=SecurityAlert, status_code=status.HTTP_201_CREATED)
def create_alert(alert: SecurityAlertCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_device = device.get_device_by_id(db, device_id=alert.device_id)
    if not db_device or db_device.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to create alert for this device")
    return alert.create_alert(db, alert=alert, device_id=alert.device_id)

@router.get("/", response_model=List[SecurityAlert])
def get_alerts(skip: int = 0, limit: int = 10, device_id: Optional[int] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if device_id:
        db_device = device.get_device_by_id(db, device_id=device_id)
        if not db_device or db_device.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Unauthorized to view alerts for this device")
    return alert.get_alerts(db, device_id=device_id, skip=skip, limit=limit)

@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(alert_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_alert = alert.get_alert_by_id(db, alert_id=alert_id)
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    db_device = device.get_device_by_id(db, device_id=db_alert.device_id)
    if not db_device or db_device.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this alert")
    if not alert.delete_alert(db, alert_id=alert_id):
        raise HTTPException(status_code=404, detail="Alert not found")
    return
