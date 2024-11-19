from . import views
from django.urls import path
urlpatterns = [
  path('alerts/', views.alerts, name='alerts'),
  path('resolve_alert/<int:alert_id>/', views.resolve_alert, name='resolve_alert')
]