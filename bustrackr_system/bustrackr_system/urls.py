"""
URL configuration for bustrackr_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from bustrackr_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bustrackr_app.urls')), 
    path("__reload__/", include("django_browser_reload.urls")),
   
   #register bus url
    path("register-bus/", views.register_bus, name="register_bus"),
    path("dashboard/", views.dashboard, name="dashboard"),  # Keep this if needed elsewhere
    path("admin-dashboard/", views.admin_dashboard_view, name="admin_dashboard"),  # Add this
    path("delete-bus/<str:id>/", views.delete_bus, name="delete_bus"),
    path("edit-bus/<str:id>/", views.edit_bus, name="edit_bus"),
    path("schedule-management/", views.schedule_management, name="schedule_management"),
    path("schedule/add/", views.create_schedule, name="create_schedule"),
    path("schedule/edit/<str:id>/", views.edit_schedule, name="edit_schedule"),
    path("schedule/delete/<str:id>/", views.delete_schedule, name="delete_schedule"),
    path('edit-staff/<str:staff_id>/', views.edit_staff_view, name='edit_staff'),
    path("delete-staff/<str:staff_id>/", views.delete_staff_view, name="delete_staff"),

]
