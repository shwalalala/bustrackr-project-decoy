from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import StaffAccount, AdminAccount
from django.contrib.auth.decorators import login_required

# --- LOGIN VIEW ---
def staff_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # for staff_id or admin_id
        password = request.POST.get('password')

        # --- ADMIN LOGIN ---
        if username == '1' and password == '123456':
            request.session['is_admin'] = True
            return redirect('admin_dashboard')

        # --- STAFF LOGIN ---
        try:
            staff = StaffAccount.objects.get(staff_id=username, password=password)
            request.session['staff_id'] = staff.staff_id
            return redirect('staff_dashboard')
        except StaffAccount.DoesNotExist:
            messages.error(request, 'Invalid staff ID or password.')

    return render(request, 'bustrackr_app/staff_login.html')


# --- LOGOUT VIEW ---
def logout_view(request):
    """Logs out both admin and staff users and clears session data."""
    # Clear all session data
    for key in list(request.session.keys()):
        del request.session[key]
    
    logout(request)  # Django’s built-in logout (safe for future expansion)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('staff_login')


# --- DASHBOARDS ---
def home(request):
    return render(request, 'bustrackr_app/home.html')

def staff_dashboard_view(request):
    if not request.session.get('staff_id'):
        return redirect('staff_login')
    return render(request, 'bustrackr_app/staff_dashboard.html')

def admin_dashboard_view(request):
    if not request.session.get('is_admin'):
        return redirect('staff_login')
    return render(request, 'bustrackr_app/admin_dashboard.html')


# --- STAFF MANAGEMENT ---
def add_staff_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        new_staff = StaffAccount(name=name, password=password)
        new_staff.save()

        staff_id = new_staff.staff_id
        messages.success(request, f'Staff "{name}" added successfully! Staff ID: {staff_id}')
        return redirect('admin_dashboard')
    return redirect('admin_dashboard')


# --- OTHER EXISTING PAGES ---
def schedule_management(request):
    if not request.session.get('staff_id'):
        return redirect('staff_login')
    return render(request, 'bustrackr_app/staff_dashboard_schedule.html')

def seat_availability(request):
    if not request.session.get('staff_id'):
        return redirect('staff_login')
    return render(request, 'bustrackr_app/seat_availability.html')

def bus_overview(request):
    if not request.session.get('staff_id'):
        return redirect('staff_login')
    return render(request, 'bustrackr_app/bus_overview.html')

def reports(request):
    if not request.session.get('staff_id'):
        return redirect('staff_login')
    return render(request, 'bustrackr_app/reports.html')


# --- STAFF DASHBOARD PROTECTED ROUTE ---
@login_required(login_url='staff_login')
def staff_dashboard(request):
    if not request.session.get('staff_id'):
        return redirect('staff_login')
    return render(request, 'bustrackr_app/staff_dashboard.html')
