from django.shortcuts import render
from courses.models import Course
from students.models import Student
from django.contrib.auth.models import Group, Permission
from subjects.models import Subject
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_groups
from employees.models import Employee

@login_required(login_url="login")
def dashboard(request):
    if request.user.is_staff:
        groups = Group.objects.all()
        students = Student.objects.all().count()
        employees = Employee.objects.all().count()
        emp = Employee.objects.all()
        courses = Course.objects.filter(status=True).count()
    

    context = {
        "groups" : groups, 
        "students" : students, 
        "employees" : employees, 
        "courses" : courses,
        "emp" : emp
    }
    return render(request, "adminPanel/dashboard.html", context)

