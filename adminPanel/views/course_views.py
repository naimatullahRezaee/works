from django.shortcuts import redirect, render
from courses.models import Course
from employees.models import Employee
from students.models import Student
from django.contrib.auth.models import Group, Permission
from subjects.models import Subject
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_groups
from django.contrib import messages
from accounts.models import User
from courses.forms import UpdateCourseForm



@login_required(login_url="login")
@allowed_groups(groups=["admins"])
def course_detail_view(request, slug):
    course = Course.objects.get(slug=slug)

    context = {
        "course" : course
    }

    return render(request, "adminPanel/courses/detail.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["admins", "managers"])
def course_review_view(request, slug):

    course = Course.objects.get(slug=slug)
    if request.method == "POST":
        form = UpdateCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"کورس {course.title} موفقانه ویرایش و ذخیره گردید.")
            return redirect("department-detail",course.subject.department.slug)

    else:
        form = UpdateCourseForm(instance=course)

    context = {
        "course" : course, 
        "form" : form
    }

    return render(request, "adminPanel/courses/edit.html", context)
