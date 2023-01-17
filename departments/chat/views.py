from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
def course_discussion(request, course_id):
    try:
        course = request.user.student.join_course.get(slug=course_id)
    except:
        return HttpResponseForbidden()

    context = {
        "course" : course
    }
    return render(request, "chat/room.html", context)
