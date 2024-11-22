from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from ..crud import create_alert, get_alerts, get_alert_by_id, update_alert, delete_alert,get_device_by_id
from ..schemas import SecurityAlertCreate, SecurityAlert
from ..database import get_db
from ..models import User
from typing import List,Optional
from ..utils import get_current_user

router = APIRouter()

@router.post("/", response_model=SecurityAlert, status_code=status.HTTP_201_CREATED)
def create_alert_routes(
    alert: SecurityAlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_device = get_device_by_id(db, device_id=alert.device_id)
    if not db_device or db_device.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized to create alert for this device"
        )

    new_alert = create_alert(db, alert=alert)
    return new_alert

@router.get("/", response_model=List[SecurityAlert])
def get_alerts_routes(skip: int = 0, limit: int = 10, device_id: Optional[int] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if device_id:
        db_device = get_device_by_id(db, device_id=device_id)
        if not db_device or db_device.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Unauthorized to view alerts for this device")
    return get_alerts(db, device_id=device_id, skip=skip, limit=limit)

@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert_routes(alert_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_alert = get_alert_by_id(db, alert_id=alert_id)
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    db_device = get_device_by_id(db, device_id=db_alert.device_id)
    if not db_device or db_device.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this alert")
    if not delete_alert(db, alert_id=alert_id):
        raise HTTPException(status_code=404, detail="Alert not found")
    return


# router to update alert
@router.put("/{alert_id}", response_model=SecurityAlert)
def update_alert_routes(alert_id: int, alert: SecurityAlertCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_alert = get_alert_by_id(db, alert_id=alert_id)
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    db_device = get_device_by_id(db, device_id=db_alert.device_id)
    if not db_device or db_device.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to update this alert")
    updated_alert = update_alert(db, alert_id=alert_id, alert=alert)
    if not updated_alert:
        raise HTTPException(status_code=404, detail="Alert not found")  