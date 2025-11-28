from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .supabase_client import supabase
from .models import StaffAccount, AdminAccount
from django.contrib.auth.decorators import login_required
from supabase import create_client
#import requests
#from django.http import JsonResponse
import uuid

# LOGIN VIEW 
def staff_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # for staff_id or admin_id
        password = request.POST.get('password')

        #  ADMIN LOGIN 
        if username == '1' and password == '123456':
            request.session['is_admin'] = True
            return redirect('admin_dashboard')

        #  STAFF LOGIN 
        try:
            staff = StaffAccount.objects.get(staff_id=username, password=password)
            request.session['staff_id'] = staff.staff_id
            return redirect('staff_dashboard')
        except StaffAccount.DoesNotExist:
            messages.error(request, 'Invalid staff ID or password.')

    return render(request, 'bustrackr_app/staff_login.html')


#  LOGOUT VIEW
def logout_view(request):
    """Logs out both admin and staff users and clears session data."""
    # Clear all session data
    for key in list(request.session.keys()):
        del request.session[key]
    
    logout(request)  # Django’s built-in logout (safe for future expansion)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('staff_login')


# DASHBOARDS 
def home(request):
    return render(request, 'bustrackr_app/home.html')

def about(request):
    return render(request, "bustrackr_app/user_about_us.html", {
        "company_name": "BusTrackr",
        "mission": "Making transport tracking simple, reliable and accessible for all.",
        "founding_year": 2024,
        "founders": ["Alice Smith", "Bob Johnson"],
        "core_values": ["Transparency", "Reliability", "Innovation"],
    
    })

def staff_dashboard_view(request):
    if not request.session.get('staff_id'):
        return redirect('staff_login')
    # Fetch buses from Supabase to display on the staff dashboard
    try:
        resp = supabase.table("bus").select("*").execute()
        buses = resp.data if resp and hasattr(resp, 'data') else []
    except Exception as e:
        print(f"Error fetching buses for staff dashboard: {e}")
        buses = []

    return render(request, 'bustrackr_app/staff_dashboard.html', {
        'buses': buses
    })

# def admin_dashboard_view(request):
#     if not request.session.get('is_admin'):
#         return redirect('staff_login')
#     return render(request, 'bustrackr_app/admin_dashboard.html')

def admin_dashboard_view(request):
    if not request.session.get('is_admin'):
        return redirect('staff_login')
    
    # Get buses from Supabase
    try:
        buses = supabase.table("bus").select("*").execute()
        bus_data = buses.data
    except Exception as e:
        print(f"Error fetching buses: {e}")
        bus_data = []
    
    return render(request, 'bustrackr_app/admin_dashboard.html', {
        "buses": bus_data
    })

#CREATE BUS REGISTER VIEW
# def register_bus(request):
#     if request.method == "POST":
#         data = {
#             "plate_number": request.POST["plate_number"],
#             "bus_company": request.POST["bus_company"],
#             "bus_type": request.POST["bus_type"],
#             "capacity": int(request.POST["capacity"]),
#         }
#         supabase.table("bus").insert(data).execute()
#         return redirect("dashboard")

#     return render(request, "components/register_bus.html")

def register_bus(request):
    if request.method == 'POST':
        plate_number = request.POST.get('plate_number')
        bus_company = request.POST.get('bus_company')
        bus_type = request.POST.get('bus_type')
        capacity = request.POST.get('capacity')
        
        # Validate required fields
        if not all([plate_number, bus_company, bus_type, capacity]):
            messages.error(request, 'All fields are required!')
            return redirect('admin_dashboard')
        
        try:
            # Save to Supabase
            data = {
                "plate_number": plate_number,
                "bus_company": bus_company,
                "bus_type": bus_type,
                "capacity": int(capacity),
                "status": request.POST["status"], 
            }
            response = supabase.table("bus").insert(data).execute()
            
            if response.data:
                messages.success(request, 'Bus registered successfully!')
            else:
                messages.error(request, 'Failed to register bus.')
                
        except Exception as e:
            messages.error(request, f'Error registering bus: {str(e)}')
        
        return redirect('admin_dashboard')  # Redirect to admin dashboard
    
    # If GET request, redirect to admin dashboard
    return redirect('admin_dashboard')

#READ BUS LIST
def dashboard(request):
    buses = supabase.table("bus").select("*").execute()

    return render(request, "bustrackr_app/dashboard.html", {
        "buses": buses.data
    })

#DELETE BUS
def delete_bus(request, id):
    supabase.table("bus").delete().eq("id", id).execute()
    messages.success(request, 'Bus deleted successfully!')
    return redirect("admin_dashboard")  # Redirect to admin dashboard

#EDIT BUS
def edit_bus(request, id):
    if request.method == "POST":
        updated = {
            "capacity": int(request.POST["capacity"]),
            "status": request.POST["status"]
        }
        supabase.table("bus").update(updated).eq("id", id).execute()
        messages.success(request, "Bus updated successfully!")
        return redirect("admin_dashboard")

    return redirect("admin_dashboard")


#STAFF MANAGEMENT
""""
def add_staff_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        new_staff = StaffAccount(name=name, password=password)
        new_staff.save()

        staff_id = new_staff.staff_id
        messages.success(request, f'Staff "{name}" added successfully! Staff ID: {staff_id}')
        return redirect('user_management')
    return redirect('user_management')
"""
def add_staff_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            new_staff = StaffAccount(name=name, password=password)
            new_staff.save()

            staff_id = new_staff.staff_id
            messages.success(request, f'Staff "{name}" added successfully! Staff ID: {staff_id}')
        except Exception as e:
            messages.error(request, f'Failed to add staff: {str(e)}')

        return redirect('user_management')
    return redirect('user_management')


def edit_staff_view(request, staff_id=None):

    # Accept staff_id from either the URL or the hidden form input
    if request.method == 'POST':
        staff_id = staff_id or request.POST.get('staff_id')

    # Now safely fetch the staff object
    staff = get_object_or_404(StaffAccount, staff_id=staff_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        # Update name
        staff.name = name

        # Update password only if provided
        if password and password.strip() != "":
            staff.password = password

        staff.save()

        # Prepare Supabase update fields
        update_data = {"name": name}
        if password and password.strip() != "":
            update_data["password"] = password

        # Update in Supabase
        try:
            response = supabase.table("StaffAccount") \
                .update(update_data) \
                .eq("staff_id", staff_id) \
                .execute()

            if response.data:
                messages.success(request, f'Staff "{name}" updated successfully and synced with Supabase!')
            else:
                messages.warning(request, f'Staff updated locally but Supabase did not update.')

        except Exception as e:
            print("Supabase update error:", e)
            messages.warning(request, "Staff updated locally but failed to sync with Supabase.")

        return redirect('user_management')

    # GET request — load modal template
    context = {'staff': staff}
    return render(request, 'edit_staff.html', context)

#OTHER EXISTING PAGES
def schedule_management(request):
    if not (request.session.get('staff_id') or request.session.get('is_admin')):
        return redirect('staff_login')
    return render(request, 'bustrackr_app/staff_dashboard_schedule.html')

def seat_availability(request):
    if not (request.session.get('staff_id') or request.session.get('is_admin')):
        return redirect('staff_login')
    return render(request, 'bustrackr_app/staff_dashboard_seat_availability.html')

def bus_overview(request):
    if not (request.session.get('staff_id') or request.session.get('is_admin')):
        return redirect('staff_login')
    return render(request, 'bustrackr_app/staff_dashboard_bus_overview.html')

def reports(request):
    if not (request.session.get('staff_id') or request.session.get('is_admin')):
        return redirect('staff_login')
    return render(request, 'bustrackr_app/staff_dashboard_reports.html')

def user_management(request):
     if not request.session.get('is_admin'):
        return redirect('staff_login')
     response = supabase.table("bustrackr_app_staffaccount").select("*").execute()
     staff_list = response.data  # Supabase returns a list of dicts

     return render(request, "bustrackr_app/admin_user_management.html", {"staff_list": staff_list})
    

def bus_management(request):
    if not request.session.get('is_admin'):
        return redirect('staff_login')
    return render(request, 'bustrackr_app/admin_bus_schedule.html')

# STAFF DASHBOARD PROTECTED ROUTE
@login_required(login_url='staff_login')
def staff_dashboard(request):
    if not request.session.get('staff_id'):
        return redirect('staff_login')
    return render(request, 'bustrackr_app/staff_dashboard.html')

#SCHEDULE MANAGEMENT

def schedule_management(request):
    if not (request.session.get('is_admin') or request.session.get('staff_id')):
        return redirect('staff_login')

    try:
        buses = supabase.table("bus").select("*").execute().data
        schedules = supabase.table("bus_schedule").select("*").execute().data
    except Exception as e:
        print("Error:", e)
        buses, schedules = [], []

    routes = [
        "Cebu - Toledo",
        "Cebu - Pinamungahan",
        "Cebu - Aloguinsan",
        "Cebu - Asturias"
    ]

    statuses = ["On Time", "Delayed", "Cancelled"]

    return render(request, 'bustrackr_app/staff_dashboard_schedule.html', {
        "buses": buses,
        "schedules": schedules,
        "routes": routes,
        "statuses": statuses
    })




# POSTGREST_URL = "http://127.0.0.1:8000/bus_schedule"

def create_schedule(request):
    if request.method == "POST":
        data = request.POST

        payload = {
            "bus_id": int(data.get("bus_id")),
            "route": data.get("route"),
            "departure_time": data.get("departure_time"),
            "arrival_time": data.get("arrival_time"),
            "status": data.get("status"),
        }

        # Validate required fields
        if not all([payload["bus_id"], payload["route"], payload["departure_time"], payload["arrival_time"], payload["status"]]):
            messages.error(request, "All fields are required.")
            return redirect("schedule_management")

        try:
            supabase.table("bus_schedule").insert(payload).execute()
            messages.success(request, "Schedule created successfully!")
        except Exception as e:
            messages.error(request, f"Error creating schedule: {str(e)}")

        return redirect("schedule_management")


def edit_schedule(request, id):
    if request.method == "POST":
        updated = {
            "bus_id": int(request.POST.get("bus_id")),
            "route": request.POST.get("route"),
            "departure_time": request.POST.get("departure_time"),
            "arrival_time": request.POST.get("arrival_time"),
            "status": request.POST.get("status"),
        }

        try:
            supabase.table("bus_schedule").update(updated).eq("id", id).execute()
            messages.success(request, "Schedule updated successfully!")
        except Exception as e:
            messages.error(request, f"Error updating schedule: {str(e)}")

    return redirect("schedule_management")


def delete_schedule(request, id):
    supabase.table("bus_schedule").delete().eq("id", id).execute()
    messages.success(request, "Schedule deleted successfully!")
    return redirect("schedule_management")
