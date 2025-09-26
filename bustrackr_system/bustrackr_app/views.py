from django.shortcuts import render
from .models import Student

# Create your views here.

def home(request):
    return render(request, 'myapp/home.html')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'myapp/student_list.html', {'students': students})