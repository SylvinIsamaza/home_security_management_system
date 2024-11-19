from django.urls import path
from . import views
urlpatterns = [
    path('devices/', views.devices, name='devices'),
    path('add_device/', views.add_device, name='add_device'),
   
]
