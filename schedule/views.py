from django.shortcuts import render, get_object_or_404, redirect
from departments.models import Department, Semester
from courses.models import Session
from subjects.models import Subject
from employees.models import Employee
from django.contrib.auth.decorators import login_required
from .models import Schedule
# Create your views here.

@login_required(login_url="login")
def schedule_list(request):
    departments = Department.objects.all()
    context = {
        "departments" : departments
    }
    return render(request, "schedule/list.html", context)

@login_required(login_url="login")
def create_new_schedule(request):
    departments = Department.objects.all()
    context = {
        "departments" : departments
    }
    return render(request, "schedule/create/step1.html", context)

@login_required(login_url="login")
def create_schedule_step2(request, slug):
    department = get_object_or_404(Department, slug=slug)
    semesters = Semester.objects.filter(program__department__name=department)
    context = {
        "department" : department, 
        "semesters" : semesters
    }
    return render(request, "schedule/create/step2.html", context)

@login_required(login_url="login")
def create_schedule_final(request, slug, id):
    department = get_object_or_404(Department, slug=slug)
    semester = get_object_or_404(Semester, id=id)
    subjects = department.subject_set.all()
    instructors = department.department.all()
    sessions = Session.objects.get(current_session=True)
    schedules = Schedule.objects.filter(department=department, semester=semester)

    if request.method == "POST":
        subject = Subject.objects.get(slug=request.POST.get("subject"))
        instructor = Employee.objects.get(id=request.POST.get("instructor"))
        days  = request.POST.get("days")
        hours = request.POST.get("hours")
        start = request.POST.get("start")
        finish = request.POST.get("finish")

        Schedule.objects.create(
            department=department, 
            semester=semester, 
            session=sessions, 
            subject=subject, 
            instructor=instructor, 
            days=days, 
            hours=hours, 
            from_time=start, 
            to_time=finish
        )
        return redirect("create_schedule_final", department.slug, semester.id)

    context = {
        "department" : department, 
        "semester" : semester, 
        "subjects" : subjects, 
        "instructors" : instructors, 
        "sessions" : sessions, 
        "schedules" : schedules
    }

    return render(request, "schedule/create/final.html", context)