from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('dashboard/', views.staff_dashboard_view, name='staff_dashboard'),
    path('login/', views.staff_login_view, name='staff_login'),  
    path('schedule/', views.schedule_management, name='schedule_management'),
    path('seat-availability/', views.seat_availability, name='seat_availability'),
    path('bus-overview/', views.bus_overview, name='bus_overview'),
    path('reports/', views.reports, name='reports'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('add-staff/', views.add_staff_view, name='add_staff'),

]