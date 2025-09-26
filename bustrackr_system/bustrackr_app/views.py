from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # or your home page
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'bustrackr_app/login.html')


def home(request):
    return render(request, 'bustrackr_app/home.html')

def dashboard_view(request):
    return render(request, 'bustrackr_app/dashboard.html')
