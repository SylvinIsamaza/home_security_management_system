from django.db import models
from django.contrib.auth.models import User


class Device(models.Model):
    DEVICE_TYPES = (
        ('Camera', 'Camera'),
        ('Alarm', 'Alarm'),
        ('Motion Sensor', 'Motion Sensor'),
        ('Door Lock', 'Door Lock'),
    )
    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPES)
    location = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.name} ({self.device_type}) at {self.location}"
