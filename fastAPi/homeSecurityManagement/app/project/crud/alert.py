from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas


def create_alert(db: Session, alert: schemas.SecurityAlertCreate) -> models.SecurityAlert:
    db_alert = models.SecurityAlert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def get_alerts(db: Session, device_id: Optional[int] = None, skip: int = 0, limit: int = 10) -> List[models.SecurityAlert]:
    query = db.query(models.SecurityAlert)
    if device_id:
        query = query.filter(models.SecurityAlert.device_id == device_id)
    return query.offset(skip).limit(limit).all()


def get_alert_by_id(db: Session, alert_id: int) -> Optional[models.SecurityAlert]:
    return db.query(models.SecurityAlert).filter(models.SecurityAlert.id == alert_id).first()


def update_alert(db: Session, alert_id: int, alert: schemas.SecurityAlertCreate) -> Optional[models.SecurityAlert]:
    db_alert = db.query(models.SecurityAlert).filter(models.SecurityAlert.id == alert_id).first()
    if db_alert:
        for key, value in alert.dict().items():
            setattr(db_alert, key, value)
        db.commit()
        db.refresh(db_alert)
        return db_alert
    return None


def delete_alert(db: Session, alert_id: int) -> bool:
    alert = db.query(models.SecurityAlert).filter(models.SecurityAlert.id == alert_id).first()
    if alert:
        db.delete(alert)
        db.commit()
        return True
    return False
