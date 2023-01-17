from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from accounts.decorators import allowed_groups
from subjects.models import Subject
from django.http import HttpResponse, HttpResponseRedirect

from .models import Content, Course, Module, Session
from django.forms.models import inlineformset_factory
from .forms import UpdateCourseDetailForm, UpdateCourseForm, ContentUpdateForm
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from actions.utils import create_action
from django.contrib import messages
from students.models  import Student

@login_required(login_url="login")
@allowed_groups(groups=['instructors'])
def create_course_view(request):
    session =  Session.objects.last()
    if request.method == "POST":
        subject = Subject.objects.get(pk=request.POST.get("subject"))
        title = request.POST.get("course-title")
        overview = request.POST.get("course-overview")
        system = request.POST.get("system")
        if system == "credit":
            system = "کریدیت"
        elif system == "traditional":
            system = "قدیمی"

        course = Course.objects.create(
                owner = request.user,
                session = session, 
                subject=subject, 
                title=title,
                overview=overview,
                system=system, 
                status = True
            )
        if course:
            create_action(request.user, "یک کورس جدید ایجاد کرد", course)
            Module.objects.create(
                course=course, 
                week=1, 
                title="Course Introduction",
                content="In this module you are going to get introdcued with... "
            )
        students = []
        for std in Student.objects.all():
            if std.department.id == course.subject.department.id and std.semester == course.subject.semester:
                students.append(std)
        if course.system == "قدیمی":
            for student in students:
                course.students.add(student)
        messages.success(request, "کورس جدید موفقانه ایجاد گردید.")
        return redirect("course-detail", course.slug)
        

@login_required(login_url="login")
@allowed_groups(groups=["instructors"])
def course_detail_view(request, slug):
    course = Course.objects.get(slug=slug)
    if request.method == "POST":
        c_form = UpdateCourseForm(request.POST, instance=course)
        cd_form = UpdateCourseDetailForm(request.POST, request.FILES, instance=course.coursedetail)
        if c_form.is_valid() and cd_form.is_valid():
            c_form.save()
            cd_form.save()
            create_action(request.user, f"{course.title} را ویرایش کرد. ", course)
            return redirect("course-detail", course.slug)
    else:
        c_form = UpdateCourseForm(instance=course)
        cd_form = UpdateCourseDetailForm(instance=course.coursedetail)

    if request.user != course.owner:
        return HttpResponse("You are not authorized")

    modules = course.module_set.all()

    ModuleFormSet = inlineformset_factory(
        Course, 
        Module,
        fields = ["week", "title", "content"],
        extra=1, 
        can_delete=True
    )
    if request.method == "POST":
        formset = ModuleFormSet(request.POST, instance=course)
        if formset.is_valid():
            formset.save()
            # send notificatios when new modules get created
            # create_action(request.user, "module created", formset)
            return redirect("course-detail", course.slug)
    else:
        formset = ModuleFormSet(instance=course)
    context = {
        "formset" : formset, 
        "course" : course, 
        "modules" : modules, 
        "c_form" : c_form,
        "cd_form" : cd_form
    }
    return render(request, "courses/detail.html", context)



@login_required(login_url="login")
@allowed_groups(groups=["instructors"])
def list_course_view(request, page=1):
    q = request.GET.get("q") if  request.GET.get("q") != None else ""

    subjects = Subject.objects.filter(department=request.user.employee.department)
    courses = Course.objects.filter(
        Q(title__icontains=q) | Q(overview__icontains=q),
        owner=request.user, 
        status=True, 
        )
    deactive_courses = Course.objects.filter(status=False, owner=request.user)
    # implement pagination
    paginator = Paginator(courses, 4)

    try:
        courses = paginator.page(page)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    # latest visited course

    
    
    context = {
        'subjects' : subjects, 
        "courses" : courses, 
        "deactive_courses" : deactive_courses
    }
    return render(request, "courses/list.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["instructors", "students"])
def course_content_view(request, slug, pk):
    course = Course.objects.get(slug=slug)
    module = Module.objects.get(pk=pk)

    # if not request.user.student in course.students.all():
    #     return HttpResponse("You are not authorize to view this page")
    
    
    if request.method == "POST":
        module_id = request.POST.get("content-module")
        title = request.POST.get("content-title")
        text = request.POST.get("content-desc")
        image = request.FILES.get("content-image")
        file = request.FILES.get("content-file")
        video = request.FILES.get("content-video")

        content = Content.objects.create(
            module=Module.objects.get(pk=module_id),
            title = title,
            text=text,
            image=image, 
            file=file, 
            video=video
        )
        create_action(request.user, "معلومات جدید درج کرد. ", course)
        messages.success(request, "معلومات جدید موفقانه اضافه گردید.")
        

    context = {
        "course" : course, 
        "module" : module
    }

    return render(request, "courses/contents/list.html", context)

@login_required(login_url="login")
@allowed_groups(groups=["instructors"])
def content_update_view(request, pk):
    content = Content.objects.get(pk=pk)
    if request.user == content.module.course.owner:

        if request.method == "POST":
            form = ContentUpdateForm(request.POST or None, request.FILES or None, instance=content)
            if form.is_valid():
                form.save()
                create_action(request.user, "معلومات درج شده را ویرایش کرد. ")
                return redirect("course-content", content.module.course.slug, content.module.pk)
        else:
            form = ContentUpdateForm(instance=content)
    else:
        return HttpResponse("You are not authorize to update this content ")
    context = {
        "form" : form
    }
    return render(request, "courses/contents/update.html", context)



@login_required(login_url="login")
@allowed_groups(groups=["instructors"])
def delete_content_view(request):
    if request.method == "POST":
        content = Content.objects.get(pk=request.POST.get("content-id"))
        if request.user == content.module.course.owner:
            content.delete()
            create_action(request.user, "معلومات درج شده را حذف کرد. ")
        else:
            return HttpResponse("You are not allowed ")
        return redirect("course-content", content.module.course.slug, content.module.pk)




@login_required(login_url="login")
@allowed_groups(groups=["managers"])
def approve_course(request):
    if request.method == "POST":
        course = Course.objects.get(pk=request.POST.get("approve-course"))
        if course.status == True:
            return redirect("department-detail", course.subject.department.slug)
        else:
            course.status = True
            create_action(request.user, "کورس شما را تایید کرد. ")
            course.save()
            messages.success(request, "کورس فوق توسط آمریت محترم تدریسی تایید گردید.")
            return redirect("department-detail", course.subject.department.slug)



@login_required(login_url="login")
@allowed_groups(groups=["managers"])
def session_list_view(request):
    sessions = Session.objects.all()

    context = {
        "sessions" : sessions
    }

    return render(request, "courses/sessions/list.html", context)





@login_required(login_url="login")
@allowed_groups(groups=["managers", "admins", "department_loans"])
def session_detail_view(request, year, month, day, type):

    session = get_object_or_404(Session, session__year=year, session__month=month, session__day=day,  session_type=type)
    courses = session.course_set.all().count()
    students = 0
    new = 0
    chances = 0
    new_students = []
    for std in Student.objects.all():
        if std.semester.semester_number == 1:
            new_students.append(std)

    all_students = []
    for course in session.course_set.all():
        for std in course.students.all():
            all_students.append(std)
        students += course.students.all().count()
    
    for std in all_students:
        for result in std.result_set.all():
            if std.semester.semester_number == result.subject.semester.semester_number and result.total_score() < 55:
                chances += 1

    context = {
        "session" : session, 
        "courses" : courses, 
        "students" : students, 
        "new_students" : new, 
        "chances" : chances
    }

    return render(request, "courses/sessions/detail.html", context)



@login_required(login_url="login")
@allowed_groups(groups=["managers", "admins", "department_loans"])
def session_create_view(request):

    if request.method == "POST":
        session_type = request.POST.get("name")
        if session_type == "spring":
            session_type = "بهاری"
        elif session_type == "fall":
            session_type = "خزانی"

        
        session_date = request.POST.get("date")
    
        session = Session.objects.create(
            session=session_date, 
            session_type=session_type
        )
        if session:
            messages.success(request, "دوره جدید تحصیلی ایجاد گردید.")
            return redirect("session-list")


@login_required(login_url="login")
@allowed_groups(groups=["managers", "admins"])
def course_admin_detail_view(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {
        "course" : course
    }
    return render(request, "courses/admin/detail.html", context)