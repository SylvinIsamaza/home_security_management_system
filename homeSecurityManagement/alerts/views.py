from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from device.models import Device
from django.utils import timezone
from django.core.paginator import Paginator
from .models import SecurityAlert

@login_required
def alerts(request):
    if request.method == 'POST':
        device_id = request.POST.get('device') 
        alert_type = request.POST.get('alert_type')  
        
        device = get_object_or_404(Device, id=device_id, user=request.user)  
        
        SecurityAlert.objects.create(
            device=device,
            alert_type=alert_type,
            timestamp=timezone.now(),
            resolved=False  
        )
        
        return redirect(request.META.get('HTTP_REFERER', '/'))

    devices = Device.objects.filter(user=request.user)
    alerts = SecurityAlert.objects.filter(device__user=request.user)

    paginator = Paginator(alerts, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    return render(request, 'alerts/alerts.html', {
        'page_obj': pa
        
        
        
        
        
        ge_obj,
        'devices': devices
    })     
@login_required
def resolve_alert(request, alert_id):
    alert = get_object_or_404(SecurityAlert, id=alert_id)
    alert.resolved = True
    alert.save()
    return redirect('alerts')
