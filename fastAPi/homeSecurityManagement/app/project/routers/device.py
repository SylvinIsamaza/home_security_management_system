from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..crud import create_device,get_devices,get_device_by_id,update_device,delete_device
from ..schemas import DeviceCreate, Device
from ..database import get_db
from ..models import User
from fastapi.security import OAuth2PasswordBearer
from ..utils import get_current_user 
from typing import List



router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/", response_model=Device, status_code=status.HTTP_201_CREATED)
def create_device_route(device: DeviceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_device(db, device=device, user_id=current_user.id)

@router.get("/", response_model=List[Device])
def get_devices_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_devices(db, user_id=current_user.id, skip=skip, limit=limit)

@router.put("/{device_id}", response_model=Device)
def update_device_router(device_id: int, device: DeviceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_device = get_device_by_id(db, device_id=device_id)
    if not db_device or db_device.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to update this device")
    updated_device = update_device(db, device_id=device_id, device=device)
    if not updated_device:
        raise HTTPException(status_code=404, detail="Device not found")
    return updated_device

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device_router(device_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_device = get_device_by_id(db, device_id=device_id)
    if not db_device or db_device.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this device")
    if not delete_device(db, device_id):
        raise HTTPException(status_code=404, detail="Device not found")
    return
