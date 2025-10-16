from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def staff_login_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')

        # Admin login (fixed credentials)
        if role == 'admin':
            admin_id = request.POST.get('admin_id')
            admin_password = request.POST.get('admin_password')
            if admin_id == '1' and admin_password == 'admin':
                request.session['staff_role'] = 'admin'
                return redirect('admin_dashboard')  # redirect to admin dashboard
            else:
                messages.error(request, 'Invalid admin credentials')

        # Operator or Staff login using Django auth
        elif role in ['operator', 'staff']:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['staff_role'] = role
                if role == 'operator':
                    return redirect('operator_dashboard')
                else:
                    return redirect('staff_dashboard')
            else:
                messages.error(request, 'Invalid credentials')

    return render(request, 'bustrackr_app/staff_login.html')


def home(request):
    return render(request, 'bustrackr_app/home.html')

def staff_dashboard_view(request):
    return render(request, 'bustrackr_app/staff_dashboard.html')

def schedule_management(request):
    return render(request, 'bustrackr_app/staff_dashboard_schedule.html')

def operator_dashboard_view(request):
    return render(request, 'bustrackr_app/operator_dashboard.html')

def admin_dashboard_view(request):
    return render(request, 'bustrackr_app/admin_dashboard.html')

from django.shortcuts import render

def seat_availability(request):
    return render(request, 'bustrackr_app/seat_availability.html')

def bus_overview(request):
    return render(request, 'bustrackr_app/bus_overview.html')

def reports(request):
    return render(request, 'bustrackr_app/reports.html')
