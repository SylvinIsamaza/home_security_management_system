from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from security.models import SecurityEvent

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'user/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'user/login.html', {'error': 'Invalid credentials'})
    return render(request, 'user/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        user = request.user
        if not user.check_password(current_password):
            return render(request, 'user/change-password.html', {'error': 'Current password is incorrect.'})

        if new_password != confirm_new_password:
            return render(request, 'user/change-password.html', {'error': 'New passwords do not match.'})
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user) 
        messages.success(request, 'Your password was successfully updated!')
        return redirect('/') 
    else:
        user = request.user
        if(user.is_authenticated):
            return render(request, 'user/change-password.html')
        else:
            return redirect('/')

