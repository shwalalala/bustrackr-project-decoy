from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('dashboard/', views.staff_dashboard_view, name='staff_dashboard'),
    path('login/', views.staff_login_view, name='staff_login'),  



]