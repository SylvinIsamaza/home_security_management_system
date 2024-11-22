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

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from .models import SecurityEvent
from device.models import Device
from alerts.models import SecurityAlert

@login_required
def dashboard(request):
    # Get devices and alerts for the user
    devices = Device.objects.filter(user=request.user)
    alerts = SecurityAlert.objects.filter(device__user=request.user)
    
    # Device counts by type
    device_counts = (
        devices.values('device_type')
        .annotate(count=Count('id'))
        .order_by('device_type')
    )
    device_data = {
        "labels": [entry['device_type'] for entry in device_counts],
        "data": [entry['count'] for entry in device_counts]
    }

    # Alerts by date and resolved status
    alerts_by_date_resolved = (
        alerts.values('timestamp__date', 'resolved')
        .annotate(count=Count('id'))
        .order_by('timestamp__date', 'resolved')
    )
    resolved_alerts_data = {}
    unresolved_alerts_data = {}
    
    for entry in alerts_by_date_resolved:
        date_str = entry['timestamp__date'].strftime('%m/%d/%Y')
        if entry['resolved']:
            resolved_alerts_data[date_str] = entry['count']
        else:
            unresolved_alerts_data[date_str] = entry['count']
    
    all_dates = sorted(set(resolved_alerts_data.keys()) | set(unresolved_alerts_data.keys()))
    resolved_alerts = [resolved_alerts_data.get(date, 0) for date in all_dates]
    unresolved_alerts = [unresolved_alerts_data.get(date, 0) for date in all_dates]
    
    alert_data = {
        "labels": all_dates,
        "resolved": resolved_alerts,
        "unresolved": unresolved_alerts
    }

    # Handle the form submission for creating a new device
    if request.method == 'POST':
        name = request.POST.get('name')
        device_type = request.POST.get('device_type')
        location = request.POST.get('location')
        # Create new device
        Device.objects.create(
            name=name, device_type=device_type, location=location, user=request.user
        )
        return redirect('dashboard')

    
    if 'create_alert' in request.POST:
        device_id = request.POST.get('device_id')
        alert_type = request.POST.get('alert_type')
        device = get_object_or_404(Device, id=device_id)
       
        SecurityAlert.objects.create(
            device=device,
            alert_type=alert_type,
            timestamp=timezone.now(),
            resolved=False  
        )
        return redirect('dashboard')

  
    return render(request, 'security/dashboard.html', {
        'devices': devices[:5],         
        'alerts': alerts[:5],           
        'alldevices': devices,          
        'activeAlerts': alerts,         
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


