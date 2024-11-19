from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from django.utils.timezone import now
from collections import Counter
import datetime
from .models import SecurityEvent
from  device.models import Device
from alerts.models import  SecurityAlert
from django.http import JsonResponse

@login_required
def dashboard(request):
    devices = Device.objects.filter(user=request.user)
    alerts = SecurityAlert.objects.filter(device__user=request.user)
    
    # Device count grouped by type
    device_counts = (
        devices.values('device_type')
        .annotate(count=Count('id'))
        .order_by('device_type')
    )
    device_data = {
        "labels": [entry['device_type'] for entry in device_counts],
        "data": [entry['count'] for entry in device_counts]
    }

    # Alerts grouped by date
    alerts_by_date = (
        alerts.values('timestamp__date')
        .annotate(count=Count('id'))
        .order_by('timestamp__date')
    )
    alert_data = {
        "labels": [entry['timestamp__date'].strftime('%m/%d/%Y') for entry in alerts_by_date],
        "data": [entry['count'] for entry in alerts_by_date]
    }

    if request.method == 'POST':  
        name = request.POST.get('name')
        device_type = request.POST.get('device_type')
        location = request.POST.get('location')
        Device.objects.create(
            name=name, device_type=device_type, location=location, user=request.user
        )
        return redirect('dashboard')
    print(device_data)
    print(alert_data)

    return render(request, 'security/dashboard.html', {
        'devices': devices,
        'alerts': alerts,
        'device_data': device_data,
        'alert_data': alert_data,
    })

@login_required
def generate_alert(request, device_id, alert_type):
    device = get_object_or_404(Device, id=device_id)
    SecurityAlert.objects.create(
        device=device,
        alert_type=alert_type,
        timestamp=timezone.now()
    )
    return redirect('dashboard')


