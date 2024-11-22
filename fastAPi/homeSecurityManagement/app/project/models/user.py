from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from project.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)  
    devices = relationship("Device", back_populates="owner")
    devices = relationship("Device", back_populates="owner")