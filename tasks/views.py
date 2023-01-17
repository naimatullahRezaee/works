from tokenize import group
from django.http import HttpResponse
from django.shortcuts import redirect, render
from decimal import Decimal
from jalali_date import datetime2jalali
from courses.models import Content, Course
from students.models import Student
from .models import Assignment, Event, Respond, AssignmentScore
from accounts.decorators import allowed_groups
from django.contrib.auth.decorators import login_required
from .forms import AssignmentCreateForm, RespondForm, EventForm
from results.models import Result
from actions.utils import create_action
from datetime import datetime
from django.contrib import messages

@login_required(login_url="login")
@allowed_groups(groups=["instructors"])
def create_assignment_view(request, pk):
    content = Content.objects.get(pk=pk)
    assignments = Assignment.objects.filter(owner=request.user, content=content)
    if not(content.module.course.owner.id == request.user.id):
        return HttpResponse("You are not the owner of this course")
    if request.method == "POST":
        form = AssignmentCreateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.owner = request.user
            assignment.content = content
            assignment.save()
            create_action(request.user, "یک فعالیت جدید ایجاد کرد. ", assignment)
            messages.success(request, "فعالیت جدید موفقانه ایجاد گردید")
            return redirect("create-assignment",content.pk)
            
    else:
        form = AssignmentCreateForm()

    context = {
        "form" : form,
        "assignments" : assignments
    }
    return render(request, "tasks/assignments/form.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["students"])
def open_assignment_for_student_view(request, pk):
    assignment = Assignment.objects.get(pk=pk)

    submitted = assignment.respond_set.filter(sender=request.user)

    if request.method == "POST":
        form = RespondForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            respond = form.save(commit=False)
            respond.sender = request.user
            respond.assignment = assignment
            assignment.is_submitted.add(request.user.student)
            respond.save()
            create_action(request.user, "فعالیت خود را تکمیل کرد. ")
            return redirect("course-content", assignment.content.module.course.slug, assignment.content.module.id)
    else:
        form = RespondForm()
    

    context = {
        "assignment" : assignment, 
        "form" : form, 
        "submitted" : submitted
    }

    return render(request, "tasks/assignments/open_student.html", context)




@login_required(login_url="login")
@allowed_groups(groups=["instructors"])
def open_assignment_for_instructor_view(request, pk):
    assignment = Assignment.objects.get(pk=pk)
    students = []
    if request.user == assignment.content.module.course.owner:
        # all students
        students = assignment.content.module.course.students.all()
        # submitted students
        submitted_students = assignment.is_submitted.all()
        # not submitted students
        unsubmitted_students = []
        for i in assignment.content.module.course.students.all():
            unsubmitted_students.append(i)
            for std in unsubmitted_students:
                for j in assignment.is_submitted.all():
                    if j == std:
                        unsubmitted_students.remove(std)
        # scored assignments

    else:
        return HttpResponse("you are not authorize to view this page")

    scored_students = AssignmentScore.objects.filter(student__in=students)
    context = {
        "assignment" : assignment, 
        "students" : students, 
        "submitted_students" : submitted_students, 
        "unsubmitted_students" : unsubmitted_students,
        "scored_students" : scored_students
    }
    return render(request, "tasks/assignments/open_instructor.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["instructors"])
def check_and_score_assignment(request, pk, student_pk):
    assignment = Assignment.objects.get(pk=pk)
    # if assignment.expir_at.strftime('%Y, %m, %d - %H:%M:%S') == datetime.strftime('%Y, %m, %d - %H:%M:%S'):
    #     assignment.lock_after_expiration = False
    #     assignment.save()
    student = Student.objects.get(pk=student_pk)
    respond = Respond.objects.get(sender=student.user, assignment=assignment)    
    has_score = ""
    result, created = Result.objects.get_or_create(student=student, subject=assignment.content.module.course.subject)
    if not result:
        result = Result.objects.create(
            student=student, 
            subject=assignment.content.module.course.subject, 
            assignment = 0
        )
    if request.method == "POST":
        score = request.POST.get("score")
        result.assignment += Decimal(score)
        result.save()
        create_action(request.user, "نمره فعالیت شما را اضافه کرد. ", result)
        messages.success(request, "نمره فوق موفقانه ثبت گردید.")
        return redirect("open-instructor", assignment.pk)


    context = {
        "assignment" : assignment, 
        "respond" : respond,
        "student" : student, 
        "has_score" : has_score
    }

    return render(request, "tasks/assignments/grading.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["instructors"])
def create_event_phase_one(request):
    my_courses = Course.objects.filter(owner=request.user)
    context = {
        "my_courses" : my_courses
    }
    return render(request, "tasks/events/select_courses.html", context)

@login_required(login_url="login")
@allowed_groups(groups=["instructors"])
def create_event_view(request, slug):
    course = Course.objects.get(slug=slug)

    if request.method == "POST":
        form = EventForm(request.POST, user=request.user)
        if form.is_valid():
            event = form.save(commit=False)
            event.course = course
            event.user = request.user
            event.save()
            create_action(request.user, "رویداد جدید اضافه کرد. ", event)
            messages.success(request, "رویداد جدید موفقانه ثبت گردید.")
    else:
        form = EventForm(user=request.user)

    context = {
        "form" : form
    }
    
    return render(request, "tasks/events/form.html", context)

@login_required(login_url="login")
@allowed_groups(groups=["instructors"])
def event_list_view(request):
    events = Event.objects.filter(user=request.user)
    my_events = Event.objects.filter(user=request.user)
    event_list = []
    for event in events:
            event_list.append(
                {
                    "title": event.title,
                    "start": event.start_date.date().strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_date.date().strftime("%Y-%m-%dT%H:%M:%S"),
                }
            )
    context = {
        "events" : event_list, 
        "my_events" : my_events
    }

    return render(request, "tasks/events/list.html", context)



def student_event_list_view(request):
    event_list = []
    my_courses = Course.objects.filter(students=request.user.student)
    events = Event.objects.filter(course__in=my_courses)
    my_events = Event.objects.filter(course__in=my_courses)
    for event in events:
        event_list.append(
                {
                    "title": event.title,
                    "start": event.start_date.date().strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_date.date().strftime("%Y-%m-%dT%H:%M:%S"),
                }
            )

    context = {
        "events" : event_list, 
        "my_events" : my_events
    }

    return render(request, "tasks/events/student_list.html", context)