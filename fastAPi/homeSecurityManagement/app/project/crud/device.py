from sqlalchemy.orm import Session
from typing import List, Optional
from ..schemas import DeviceCreate
from ..models import Device


def create_device(db: Session, device: DeviceCreate, user_id: int) -> Device:
    db_device = Device(**device.dict(), owner_id=user_id)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def get_devices(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> List[Device]:
    return db.query(Device).filter(Device.owner_id == user_id).offset(skip).limit(limit).all()


def get_device_by_id(db: Session, device_id: int) -> Optional[Device]:
    return db.query(Device).filter(Device.id == device_id).first()


def update_device(db: Session, device_id: int, device: DeviceCreate) -> Optional[Device]:
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if db_device:
        for key, value in device.dict().items():
            setattr(db_device, key, value)
        db.commit()
        db.refresh(db_device)
        return db_device
    return None


def delete_device(db: Session, device_id: int) -> bool:
    device = db.query(Device).filter(Device.id == device_id).first()
    if device:
        db.delete(device)
        db.commit()
        return True
    return False
