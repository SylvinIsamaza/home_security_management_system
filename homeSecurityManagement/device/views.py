from django.shortcuts import render,redirect
from .models import Device
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
@login_required
def add_device(request):
    if request.method == 'POST':
        name = request.POST['name']
        device_type = request.POST['device_type']
        location = request.POST['location']
        Device.objects.create(
            name=name, device_type=device_type, location=location, user=request.user
        )
        return redirect('devices')
    return render(request, 'device/add_device.html')

@login_required
def devices(request):
    devices = Device.objects.filter(user=request.user)
    return render(request, 'device/devices.html', {'devices': devices})

