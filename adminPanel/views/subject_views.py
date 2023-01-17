from django.shortcuts import redirect, render
from employees.models import Employee
from students.models import Student
from django.contrib.auth.models import Group, Permission
from subjects.models import Subject
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_groups
from django.contrib import messages
from accounts.models import User



@login_required(login_url="login")
@allowed_groups(groups=["admins", "managers", "department_loans"])
def subject_detail_view(request, slug):
    subject = Subject.objects.get(slug=slug)
    courses = subject.course_set.all()

    context = {
        "subject" : subject, 
        "courses" : courses
    }
    return render(request, "adminPanel/subjects/detail.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["admins", "managers", "department_loans"])
def subject_delete_view(request, slug):

    subject = Subject.objects.get(slug=slug)
    if request.method == "POST":
        subject.delete()
        messages.success(request, f"مضمون {subject.subject} موفقانه از سیستم حذف گردید.")
        return redirect("department-detail", subject.department.slug)

    context = {
        "subject" : subject
    }

    return render(request, "adminPanel/subjects/delete.html", context)