from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from .supabase_client import supabase
from .models import StaffAccount, AdminAccount, Bus, Schedule
from django.contrib.auth.decorators import login_required
from supabase import create_client
from datetime import datetime
from collections import defaultdict
import requests
from django.contrib import messages

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
    
    # Clear all session data
    for key in list(request.session.keys()):
        del request.session[key]
    
    logout(request)  # Django’s built-in logout (safe for future expansion)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('staff_login')


# DASHBOARDS 
def home(request):
   
    search = request.GET.get("search", "").strip()
    terminal = request.GET.get("terminal", "").strip()
    route = request.GET.get("route", "").strip()
    departure_period = request.GET.get("departure", "").strip()
    status = request.GET.get("status", "").strip()

    try:
        # Fetch from Supabase
        schedules_data = supabase.table("bus_schedule").select("*").execute().data
        buses_data = supabase.table("bus").select("*").execute().data

        # Map buses by ID
        bus_map = {bus['id']: bus for bus in buses_data}

        # Convert each schedule row
        clean_schedules = []
        for sched in schedules_data:

            # Attach bus
            sched['bus'] = bus_map.get(sched.get('bus_id'))

            # Convert times safely
            sched['departure_time'] = convert_time_string(sched.get('departure_time'))
            sched['arrival_time'] = convert_time_string(sched.get('arrival_time'))

            # Ensure available seats
            if not sched.get("available_seats"):
                bus = sched['bus']
                sched['available_seats'] = bus.get("capacity", 0) if bus else 0

            clean_schedules.append(sched)

        schedules = clean_schedules

        if search:
            schedules = [
                s for s in schedules
                if search.lower() in s["route"].lower()
                or (s["bus"] and search.lower() in s["bus"]["bus_company"].lower())
                or (s["bus"] and search.lower() in s["bus"]["plate_number"].lower())
            ]

        # Terminal filter
        if terminal and terminal != "All Terminal":
            schedules = [s for s in schedules if s.get("terminal") == terminal]

        # Route filter
        if route and route != "All Routes":
            schedules = [s for s in schedules if s.get("route") == route]

        if departure_period and departure_period != "All Departure":
            def is_period(time, period):
                hour = time.hour if time else 0
                if period == "Morning":
                    return 5 <= hour < 12
                elif period == "Afternoon":
                    return 12 <= hour < 17
                elif period == "Evening":
                    return 17 <= hour <= 23
                return True

            schedules = [
                s for s in schedules 
                if is_period(s["departure_time"], departure_period)
            ]

        # Status filter
        if status and status != "All Status":
            schedules = [s for s in schedules if s.get("status") == status]

    except Exception as e:
        print("Error:", e)
        schedules = []

    return render(request, "bustrackr_app/home.html", {
        "schedules": schedules,
        "search": search,
        "terminal": terminal,
        "route": route,
        "departure": departure_period,
        "status": status,
    })

def about(request):
    return render(request, "bustrackr_app/user_about_us.html")

def staff_dashboard_view(request):
    if not request.session.get('staff_id'):
        return redirect('staff_login')
    
    buses = [] 
    
    try:
        resp = supabase.table("bus").select("*").execute()
        if resp and hasattr(resp, 'data'):
            buses = resp.data
            
    except Exception as e:
        print(f"Error fetching buses for staff dashboard: {e}")

    active_buses_count = 0
    for bus in buses:
        if bus.get('status') in ['Active', 'Delayed']:
            active_buses_count += 1
            
    inactive_buses_count = len(buses) - active_buses_count

    context = {
        'buses': buses,
        'active_buses_count': active_buses_count,
        'inactive_buses_count': inactive_buses_count,
    }

    return render(request, 'bustrackr_app/staff_dashboard.html', context)


def admin_dashboard_view(request):
    if not request.session.get('is_admin'):
        return redirect('staff_login')
    
    bus_data = []
    active_buses_count = 0
    inactive_buses_count = 0 
    
    try:
        bus_resp = supabase.table("bus").select("*").execute()
        bus_data = bus_resp.data if bus_resp else []
        

        for bus in bus_data:
            if bus.get('status') in ['Active', 'Delayed']:
                active_buses_count += 1
        
        inactive_buses_count = len(bus_data) - active_buses_count
                
    except Exception as e:
        print(f"Error fetching buses: {e}")

    try:
        sched_resp = supabase.table("bus_schedule").select("*").execute()
        schedules = sched_resp.data if sched_resp else []
    except Exception as e:
        
        schedules = []


    status_counts = {"OnTime": 0, "Delayed": 0, "Cancelled": 0}

    route_stats = defaultdict(lambda: {"trips": 0, "passengers": 0, "buses": set()})

    for sched in schedules:
        # Status Logic
        status = sched.get('status')
        if status == "On Time":
            status_counts["OnTime"] += 1
        elif status == "Delayed":
            status_counts["Delayed"] += 1
        elif status == "Cancelled":
            status_counts["Cancelled"] += 1
        
  
        route = sched.get('route')
        if route:
            route_stats[route]["trips"] += 1
            pax = sched.get('passengers_onboard') or 0
            route_stats[route]["passengers"] += pax
            route_stats[route]["buses"].add(sched.get('bus_id'))


    final_route_data = []
    for route_name, data in route_stats.items():
        final_route_data.append({
            "name": route_name,
            "trips": data["trips"],
            "passengers": data["passengers"],
            "unique_buses": len(data["buses"])
        })

  
    chart_labels = ["On Time", "Delayed", "Cancelled"]
    chart_data = [status_counts["OnTime"], status_counts["Delayed"], status_counts["Cancelled"]]

    context = {
  
        "buses": bus_data,
        "active_buses_count": active_buses_count,
        "inactive_buses_count": inactive_buses_count,
        
   
        "route_performance": final_route_data,
        "status_counts": status_counts,
        "chart_labels": chart_labels,
        "chart_data": chart_data,
        "total_tracked": len(schedules)
    }
    
    return render(request, 'bustrackr_app/admin_dashboard.html', context)

def register_bus(request):
    if request.method == 'POST':
        plate_number = request.POST.get('plate_number')
        bus_company = request.POST.get('bus_company')
        bus_type = request.POST.get('bus_type')
        capacity = request.POST.get('capacity')
        
   
        if not all([plate_number, bus_company, bus_type, capacity]):
            messages.error(request, 'All fields are required!')
            return redirect('admin_dashboard')
        
        try:
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
        
        return redirect('bus_management')  
    
    
    return redirect('bus_management')

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
    return redirect("bus_management") 

#EDIT BUS
def edit_bus(request, id):
    if request.method == "POST":
        updated = {
            "capacity": int(request.POST["capacity"]),
            "status": request.POST["status"]
        }
        supabase.table("bus").update(updated).eq("id", id).execute()
        messages.success(request, "Bus updated successfully!")
        return redirect("bus_management")

    return redirect("bus_management")


#STAFF MANAGEMENT
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

def delete_staff_view(request, staff_id):
    staff = get_object_or_404(StaffAccount, staff_id=staff_id)

    if request.method == "POST":
        name = staff.name

        try:
            staff.delete()
            supabase.table("StaffAccount").delete().eq("staff_id", staff_id).execute()

            messages.success(request, f'Staff "{name}" deleted successfully.')
        except Exception as e:
            print("Delete Error:", e)
            messages.error(request, "Failed to delete staff. Please try again later.")

        return redirect("user_management")

    return redirect("user_management")

#SEAT AVAILABILITY
def seat_availability(request):
    if not (request.session.get('staff_id') or request.session.get('is_admin')):
        return redirect('staff_login')

    print("\n--- DEBUG: Fetching bus and schedule data ---")

    try:
        sched_resp = supabase.table("bus_schedule").select("*").execute()
        bus_resp = supabase.table("bus").select("*").execute()

        schedules = sched_resp.data
        buses = bus_resp.data

        # conversion
        for s in schedules:
            s["departure_time"] = convert_time_string(s.get("departure_time"))
            s["arrival_time"] = convert_time_string(s.get("arrival_time"))
            
        # SORT SCHEDULES ALPHABETICALLY BY ROUTE
        schedules = sorted(schedules, key=lambda x: x.get("route", "").lower())


    except Exception as e:
        print("Supabase ERROR:", e)
        schedules, buses = [], []

    return render(request, "bustrackr_app/staff_dashboard_seat_availability.html", {
        "schedules": schedules,
        "buses": buses,
    })

#seat availability update
def update_seat_availability(request):
    if request.method == "POST":

        schedule_id = request.POST.get("schedule_id")
        operation = request.POST.get("operation")
        count = int(request.POST.get("passenger_count"))

        # Fetch schedule row
        schedule_resp = supabase.table("bus_schedule").select("*").eq("id", schedule_id).execute()
        print("Schedule response:", schedule_resp)

        if not schedule_resp.data:
            messages.error(request, "Schedule not found.")
            return redirect("seat_availability")

        schedule = schedule_resp.data[0]

        # Fetch bus info
        bus_id_from_schedule = schedule["bus_id"]
        bus_resp = supabase.table("bus").select("*").eq("id", bus_id_from_schedule).execute()
        print("Bus response:", bus_resp)

        bus = bus_resp.data[0]
        capacity = int(bus["capacity"])

        # Current values
        available = int(schedule.get("available_seats") or capacity)
        onboard = int(schedule.get("passengers_onboard") or 0)

        print("Current available:", available)
        print("Current onboard:", onboard)

        if operation == "subtract" and onboard == 0:
            messages.warning(request, "Cannot subtract passengers. There are no passengers onboard yet.")
            return redirect("seat_availability")

        if operation == "add" and count > available:
            messages.warning(request,
                f"Cannot add {count} passengers. Only {available} seats are available."
            )
            return redirect("seat_availability")

        if operation == "add":
            new_available = available - count
            new_onboard = onboard + count
        else:
            new_available = available + count
            new_onboard = onboard - count



        # Update Supabase
        update_result = supabase.table("bus_schedule").update({
            "available_seats": new_available,
            "passengers_onboard": new_onboard
        }).eq("id", schedule_id).execute()

        messages.success(request, "Seat availability updated successfully!")
        return redirect("seat_availability")

    return redirect("seat_availability")

def bus_overview(request):
    if not (request.session.get('staff_id') or request.session.get('is_admin')):
        return redirect('staff_login')
    return render(request, 'bustrackr_app/staff_dashboard_bus_overview.html')

def reports(request):
    if not (request.session.get('staff_id') or request.session.get('is_admin')):
        return redirect('staff_login')


    try:
        response = supabase.table("bus_schedule").select("*").execute()
        schedules = response.data if response else []
    except Exception as e:
        print(f"Error fetching schedules: {e}")
        schedules = []


    status_counts = {
        "On Time": 0,
        "Delayed": 0,
        "Cancelled": 0
    }

    route_stats = defaultdict(lambda: {"trips": 0, "passengers": 0, "buses": set()})

    for sched in schedules:

        status = sched.get('status')
        if status in status_counts:
            status_counts[status] += 1
        

        route = sched.get('route')
        if route:
            route_stats[route]["trips"] += 1
            pax = sched.get('passengers_onboard') or 0
            route_stats[route]["passengers"] += pax
            route_stats[route]["buses"].add(sched.get('bus_id'))


    final_route_data = []
    for route_name, data in route_stats.items():
        final_route_data.append({
            "name": route_name,
            "trips": data["trips"],
            "passengers": data["passengers"],
            "unique_buses": len(data["buses"])
        })


    chart_labels = ["On Time", "Delayed", "Cancelled"]
    chart_data = [status_counts["On Time"], status_counts["Delayed"], status_counts["Cancelled"]]
    
    total_buses_tracked = len(schedules)

    context = {
        "route_performance": final_route_data,
        "chart_labels": chart_labels,
        "chart_data": chart_data,
        "status_counts": status_counts, 
        "total_tracked": total_buses_tracked
    }

    return render(request, 'bustrackr_app/staff_dashboard_reports.html', context)

def user_management(request):
    if not request.session.get('is_admin'):
        return redirect('staff_login')

    response = supabase.table("bustrackr_app_staffaccount").select("*").execute()
    staff_list = response.data  


    for staff in staff_list:
        created_at = staff.get("created_at")
        if created_at:
            staff["created_at"] = datetime.fromisoformat(created_at.replace("Z", "+00:00"))

    return render(request, "bustrackr_app/admin_user_management.html", {"staff_list": staff_list}) 

def bus_management(request):
    if not request.session.get('is_admin'):
        return redirect('staff_login')


    buses = Bus.objects.all().order_by('-id')
    total_buses = buses.count()

    active_buses_count = Bus.objects.filter(
        Q(status='Active') | Q(status='Delayed')
    ).count()

   
    inactive_buses_count = total_buses - active_buses_count

    context = {
        'buses': buses,
        'active_buses_count': active_buses_count,
        'inactive_buses_count': inactive_buses_count, 
    }

    return render(request, 'bustrackr_app/admin_bus_schedule.html', context)

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

def create_schedule(request):
    if request.method == "POST":
        data = request.POST

        bus_id = int(data.get("bus_id"))

        try:
            bus_resp = supabase.table("bus").select("capacity").eq("id", bus_id).execute()
            bus = bus_resp.data[0]
            capacity = bus["capacity"]
        except Exception as e:
            messages.error(request, f"Could not load bus capacity: {e}")
            return redirect("schedule_management")

        payload = {
            "id": str(uuid.uuid4()),
            "bus_id": bus_id,
            "route": data.get("route"),
            "departure_time": data.get("departure_time"),
            "arrival_time": data.get("arrival_time"),
            "status": data.get("status"),

            "available_seats": capacity,
            "passengers_onboard": 0
        }

        # STEP 4 — Insert the record
        try:
            supabase.table("bus_schedule").insert(payload).execute()
            messages.success(request, "Schedule created! Available seats set equal to capacity.")
        except Exception as e:
            messages.error(request, f"Error creating schedule: {e}")

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

def convert_time_string(value):
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%H:%M:%S").time()
        except:
            return value
    return value







