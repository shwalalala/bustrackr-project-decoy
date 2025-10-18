from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import StaffAccount, AdminAccount

def staff_login_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        username = request.POST.get('username')  # for staff_id or admin_id
        password = request.POST.get('password')

        # --- ADMIN LOGIN ---
        if username == '1' and password == '123456':
            request.session['is_admin'] = True
            return redirect('admin_dashboard')  # make sure this URL/view exists

        # --- OPERATOR OR STAFF LOGIN ---
        elif role in ['operator', 'staff']:
            if role == 'staff':
                try:
                    staff = StaffAccount.objects.get(staff_id=username, password=password)
                    request.session['staff_id'] = staff.staff_id
                    return redirect('staff_dashboard')
                except StaffAccount.DoesNotExist:
                    messages.error(request, 'Invalid staff ID or password.')

            elif role == 'operator':
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    request.session['staff_role'] = role
                    return redirect('operator_dashboard')
                else:
                    messages.error(request, 'Invalid operator credentials.')

    return render(request, 'bustrackr_app/staff_login.html')


# --- DASHBOARDS ---
def home(request):
    return render(request, 'bustrackr_app/home.html')

def staff_dashboard_view(request):
    return render(request, 'bustrackr_app/staff_dashboard.html')

def operator_dashboard_view(request):
    return render(request, 'bustrackr_app/operator_dashboard.html')

def admin_dashboard_view(request):
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
    return render(request, 'bustrackr_app/staff_dashboard_schedule.html')

def seat_availability(request):
    return render(request, 'bustrackr_app/seat_availability.html')

def bus_overview(request):
    return render(request, 'bustrackr_app/bus_overview.html')

def reports(request):
    return render(request, 'bustrackr_app/reports.html')
