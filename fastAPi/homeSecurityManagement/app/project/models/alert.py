from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from project.database import Base
from datetime import datetime
class SecurityAlert(Base):
    __tablename__ = "security_alerts"
    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Boolean, default=False)
    device_id = Column(Integer, ForeignKey("devices.id"))
    device = relationship("Device", back_populates="alerts")