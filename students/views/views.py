from tokenize import group
from django.shortcuts import render, redirect, get_object_or_404
from departments.models import Department, Semester, DepartmentProgramLevel
from students.models import Student, StudentBulkUpload
from ..forms import UserUpdateForm, StudentProfileUpdateForm, StudentUploadForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_groups
from courses.models import Course
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q
from subjects.models import Subject
from tasks.models import Assignment, Event, Respond
from results.models import Result
from students.utils import endResult
from django.http import HttpResponse
import csv
from django.contrib.admin.views.decorators import staff_member_required
from actions.utils import create_action


@login_required(login_url="login")
@allowed_groups(groups=['students'])
def student_dashboard(request):
    data = []
    label = []
    student = request.user.student
    courses = Course.objects.filter(students=student).count()
    my_courses = Course.objects.filter(students=student)
    total_score = 0
    percentage = 0
    total = 0
    total_credits = 1
    events = []
    for c in my_courses:
        if c.event_set.all().count() > 0 :
            for e in c.event_set.all():
                events.append(e)
    # passed course


    passed_courses = []
    for result in Result.objects.filter(student=student, subject__semester__exact=student.semester.semester_number):
        if result.total_score() >= 55:
            passed_courses.append(result)
    
    for subject in Subject.objects.filter(department=student.department, semester__semester_number__exact=student.semester.semester_number):
        total_credits += subject.credit
    for result in Result.objects.filter(student=student, subject__semester__exact=student.semester.semester_number):
        if result.subject.semester.semester_number == student.semester.semester_number:
            label.append(result.subject.subject)
            data.append(int(result.total_score()))
    for result in Result.objects.filter(student=student, subject__semester__exact=student.semester.semester_number):
        total_score += result.total_score()
        total += (result.total_score() * result.subject.credit)
    percentage = total_score / total_credits
    context = {
        "student" : student, 
        "courses" : courses, 
        "total_score" : total_score, 
        "percentage" : percentage, 
        "total_credits" : total_credits, 
        "my_courses" : my_courses, 
        "data" : data,
        "label" : label, 
        "passed_courses" : passed_courses, 
        "events" : events
    }
    return render(request, "student_dashboard.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["students"])
def student_profile(request):
    my_courses = Course.objects.filter(students=request.user.student)
    # value for charts
    courses = []
    scores = []

    total_score = 0
    total_credit = 0
    passed_credit = 0
    user = request.user
    student = request.user.student
    subjects = Subject.objects.filter(department=student.department)
    for subject in subjects:
        total_credit += subject.credit
    
    for result in Result.objects.filter(student=student):
        total_score += result.total_score()
        scores.append(int(result.total_score()))
    for course in Course.objects.filter(students=student):
        courses.append(course.title)
    context = {
        "user" : user, 
        "student" : student, 
        "total_credit" : total_credit, 
        "total_score" : total_score, 
        "courses" : courses, 
        "scores" : scores, 
        "my_courses" : my_courses
    }
    return render(request, "students/profile/profile_first_page.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["students"])
def profile_detail(request, pk):
    student = Student.objects.get(pk=pk)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = StudentProfileUpdateForm(request.POST, request.FILES, instance=request.user.student)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "معلومات شما موفقانه ثبت سیستم گردید")
            return redirect("student-profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = StudentProfileUpdateForm(instance=request.user.student)

    context = {
        "u_form" : u_form, 
        "p_form" : p_form
    }

    return render(request, "students/profile/student_detail_page.html", context)

@login_required(login_url="login")
@allowed_groups(groups=["students"])
def student_course_start_view(request):
    return render(request, "students/courses/start.html")



@login_required(login_url="login")
@allowed_groups(groups=["students"])
def student_relevant_course_view(request):
    student = request.user.student
    all_courses = []
    for course in Course.objects.all():
        if course.subject.semester == student.semester and course.subject.department == student.department and course.status == True:
            all_courses.append(course)
    
    context = {
        "all_courses" : all_courses
    }
    return render(request, "students/courses/relevant.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["students"])
def join_to_course_view(request, slug):
    course = Course.objects.get(slug=slug)
    if request.method == "POST":
        code = request.POST.get("code")

        if code == course.code:
            course.students.add(request.user.student)
            return redirect("student-dashboard")

    context = {
        "course" : course
    }
    return render(request, "students/courses/join.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["students"])
def my_courses_view(request, page=1):
    student = request.user.student
    results = Result.objects.filter(student=student)
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    subjects = Subject.objects.filter(department=request.user.student.department, semester=request.user.student.semester)
    courses = Course.objects.filter(
        Q(title__icontains=q) | Q(overview__icontains=q),
        students=request.user.student, 
        status=True
        )
    
    # implement pagination

    paginator = Paginator(courses, 4)

    try:
        courses = paginator.page(page)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    

    # course status
    passed_courses = []
    failed_courses = []


    for result in results:
        if result.total_score() >= 55:
            passed_courses.append(result.subject)
        else:
            failed_courses.append(result.subject)
    context = {
        "courses" : courses,
        "subjects" : subjects,
        "passed_courses" : passed_courses,
        "failed_courses" : failed_courses
    }
    return render(request, "students/courses/list.html", context)



@login_required(login_url="login")
@allowed_groups(groups=["students"])
def my_activity_view(request):
    my_courses = Course.objects.filter(students=request.user.student)
    my_events = Event.objects.filter(course__in=my_courses)
    assignments = []
    for course in my_courses:
        for module in course.module_set.all():
            for content in module.contents.all():
                for assignment in content.assignment_set.all():
                    assignments.append(assignment)
    
    responds = Respond.objects.filter(sender=request.user)
    context = {
        "assignments" : assignments, 
        "responds" : responds, 
        "my_events" : my_events
    }
    return render(request, "students/activities/list.html", context)

@login_required(login_url="login")
@allowed_groups(groups=["students"])
def department_subject_view(request):
    department = request.user.student.department
    subjects = Subject.objects.filter(department=department)
    context = {
        "department" : department, 
        "subjects" : subjects
    }
    return render(request, "students/departments/info.html", context)



@login_required(login_url="login")
@allowed_groups(groups=["managers", "admins"])
def student_bulk_upload_view(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        print(file)
        bulk_upload = StudentBulkUpload.objects.create(
            csv_file=file
        )
        if bulk_upload:
            messages.success(request, "file uploaded ")
            return redirect("/")
    return render(request, "students/student_upload.html")

    

def student_csv_download_view(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="student_template.csv"'
    writer = csv.writer(response)
    writer.writerow(
        [
            "kankor_id",
            "f_name",
            "l_name",
            "father_name",
            "grand_father_name",
            "school_name",
            "score",
            "department",
            "province",
            "gender",
            "semester",
            "section",
            "username", 
            "email", 
            "password",
        ]
    )

    return response


@login_required(login_url="login")
@allowed_groups(groups=['managers', 'instructors'])
def student_detail_info(request, pk):
    student = get_object_or_404(Student, pk=pk)
    department = student.department
    departments = Department.objects.filter(status="فعال")
    program = DepartmentProgramLevel.objects.get(level="لیسانس", department=department)
    semesters = program.semester_set.all()
    # ? update student info
    # * check if the request method is POST
    if request.method == "POST":
        # TODO get each field individually
        kankor_id  = request.POST.get("kankor_id")
        f_name  = request.POST.get("f_name")
        l_name  = request.POST.get("l_name")
        father_name  = request.POST.get("father_name")
        grand_father_name  = request.POST.get("grand_father_name")
        school_name  = request.POST.get("school_name")
        score  = request.POST.get("score")
        gender  = request.POST.get("gender")
        department  = Department.objects.get(slug=request.POST.get("department"))
        semester  = Semester.objects.get(id = request.POST.get("semester"))
        section  = request.POST.get("section")
        status  = request.POST.get("status")
        province  = request.POST.get("province")

        # ? now update student current info with the new recieved info
        student.kankor_id=kankor_id
        student.f_name=f_name
        student.l_name=l_name
        student.father_name=father_name
        student.grand_father_name=grand_father_name
        student.school_name=school_name
        student.score=score
        student.gender=gender
        student.province=province
        student.department=department
        student.semester=semester
        student.section=section
        student.status=status
        # TODO save student
        student.save()
        create_action(request.user, 'معلومات شاگرد ویرایش گردید. ', student)
        return redirect("student_detail_actions", student.pk)
    context = {
        "student" : student, 
        "department" : department, 
        "departments" : departments, 
        "semesters" : semesters
    }
    return render(request, "students/detail/index.html", context)


@login_required(login_url="login")
@allowed_groups(groups=['managers'])
def delete_student(request):
    student = request.POST.get("student_id")
    student.delete()
    return redirect("")
