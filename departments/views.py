from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Department, DepartmentProgramLevel, DepartmentChief
from employees.models import Employee
from django.contrib import messages
from students.models import Student
from subjects.models import Subject
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_groups
from accounts.models import User
from courses.models import Course, Session
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import Group
from django.utils import timezone

@login_required(login_url="login")
@allowed_groups(groups=["managers", "instructors", "admins"])
def department_list_view(request):
    
    users = User.objects.all()
    employees = Employee.objects.all()
    departments = Department.objects.all()
    context = {
        "departments" : departments, 
        "users" : users,
        "employees":employees
    }
    return render(request, "departments/list.html", context)

@login_required(login_url="login")
@allowed_groups(groups=["managers", "admins"])
def create_department_view(request):
    if request.method == "POST":
        name = request.POST.get("dep_name")
        publish_date = request.POST.get("dep_publish")
        about = request.POST.get("dep_about")

        try:
            dep = Department.objects.create(
                name=name, 
                publish_date=publish_date,
                about=about
            )
            messages.success(request, "دیپارتمنت جدید موفقانه ثبت سیستم گردید")
        except:
            messages.error(request, "احتمالا در پر کردن فورم دچار مشکل شده اید. لطفا دوباره تلاش نمایید.")
            return redirect("department-list")
    return redirect("department-list")

@login_required(login_url="login")
@allowed_groups(groups=["instructors", "managers", "admins"])
def department_detail_view(request, slug):
    q = request.GET.get("query") if  request.GET.get("query") != None else ""
    department = Department.objects.get(slug=slug)
    students = Student.objects.filter(
        Q(f_name__icontains=q) | Q(l_name__icontains=q) | Q(section__icontains=q) | Q(gender__icontains=q),
        department=department,
        )
    employees = Employee.objects.filter(department=department)
    subjects = Subject.objects.filter(department=department)
    deactive_courses = Course.objects.filter(status=False)
    active_courses = Course.objects.filter(status=True)
    done_courses = []
    
    context = {"department" : department, "students":students, "employees" : employees, "subjects" : subjects, "deactive_courses" : deactive_courses, "active_courses" : active_courses, "done_courses" : done_courses}
    return render(request, "departments/detail.html", context)

@allowed_groups(groups=["managers", "admins", "instructors"])
@login_required(login_url="login")
def department_program(request, slug):
    department = Department.objects.get(slug=slug)
    programs = department.departmentprogramlevel_set.all()
    if request.method == "POST":
        dep = Department.objects.get(slug=request.POST.get("department"))
        level = request.POST.get("level")

        if dep == department:
            DepartmentProgramLevel.objects.create(
                department=dep, 
                level=level
            )
        return redirect("department_program", department.slug)

    context = {
        "department" : department, 
        "programs" : programs
    }
    return render(request, "departments/detail/program.html", context)

@allowed_groups(groups=["managers", "admins", "instructors"])
@login_required(login_url="login")
def department_students_list(request, slug):
    department = get_object_or_404(Department, slug=slug)
    params = request.GET.get("query")
    limit = request.GET.get("qty")
    gender = request.GET.get("with_gender")
    semester = request.GET.get("with_semester")
    status = request.GET.get("with_status")
    if limit == None:
        limit = 10
    if params == None:
        params = ""
    if gender == None:
        gender = ""
    if semester == None:
        semester = ""
    if status == None:
        status = ""

    student_list = department.student_set.filter(
        Q(f_name__icontains=params) | 
        Q(l_name__icontains=params) | 
        Q(status__icontains=params)
    )[0:int(limit)] if gender == "" and semester == "" and status == "" else department.student_set.filter()
    
    if gender:
        student_list = student_list.filter(gender=gender)
    if semester:
        student_list = student_list.filter(semester__semester_number=semester)
    if status:
        student_list = student_list.filter(status=status)

    page = request.GET.get("page", 1)
    paginator = Paginator(student_list, 10)

    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    context = {
        "department" : department, 
        "students" : students
    }
    return render(request, "departments/detail/students.html", context)


@allowed_groups(groups=["managers", "admins", "instructors"])
@login_required(login_url='login')
def department_subject_list(request, slug):
    department = get_object_or_404(Department, slug=slug)
    query = request.GET.get("query")
    if query == None:
        query = ""
    
    subjects = department.subject_set.filter(
        Q(subject__icontains=query) | 
        Q(subject_type__icontains=query) | 
        Q(credit__icontains=query)
    )
    context = {
        "department" : department, 
        "subjects" : subjects
    }

    return render(request, "departments/detail/subjects.html", context)


@allowed_groups(groups=["managers", "admins", "instructors"])
@login_required(login_url='login')
def department_instructors_list(request, slug):
    query = request.GET.get("query")
    if query == None:
        query = ""
    department = Department.objects.get(slug=slug)
    instructors = department.department.filter(
        Q(f_name__icontains=query),
        user__groups__name__in=["instructors"]
        )

    context = {
        "department" : department, 
        "instructors" : instructors
    }

    return render(request, "departments/detail/instructors.html", context)

@allowed_groups(groups=["managers", "admins", "instructors"])
@login_required(login_url='login')
def department_create_instructor(request, slug):
    department = get_object_or_404(Department, slug=slug)
    available_groups  = Group.objects.filter(name__in=["instructors", "department_head"])
    if request.method == "POST":
        emp_id = request.POST.get("ins_id")
        name = request.POST.get("f_name")
        last_name = request.POST.get("l_name")
        father_name = request.POST.get("father_name")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        group = request.POST.getlist("groups")

        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        passwordConfirm = request.POST.get("passwordConfirm")

        if User.objects.filter(email=email).exists():
            return HttpResponse("User already exists")
        elif password != passwordConfirm:
            return HttpResponse("passwords do not match")
        else:
            user = User.objects.create_user(
                email=email, 
                username=username, 
                password=password
            )
            user.is_employee = True
            for g in group:
                if g == "department_head":
                    DepartmentChief.objects.create(
                        department=department,
                        user=user, 
                        from_date=timezone.now()
                    )
                selected_group, created = Group.objects.get_or_create(name=g)
                user.groups.add(selected_group)
            
            user.save()
        
        try:
            Employee.objects.create(
                user=user,
                emp_unique_id=emp_id,
                department=department,
                f_name=name, 
                l_name=last_name, 
                father_name=father_name, 
                gender=gender, 
                dob=dob, 
                phone_number=phone_number, 
                address=address
            )
        except:
            return HttpResponse("error")
    context = {
        "department" : department, 
        "groups" : available_groups
    }
    return render(
        request, 
        "departments/detail/create_instructor.html", 
        context
    )


@allowed_groups(groups=["managers", "admins", "instructors"])
@login_required(login_url='login')
def department_courses(request, slug, current_session=None):
    item = None
    department = get_object_or_404(Department, slug=slug)
    courses = Course.objects.filter(subject__department=department, status=True)
    sessions = Session.objects.all().order_by('-session')

    if current_session:
        item = current_session
        courses = Course.objects.filter(session=current_session)
    

    context = {
        "department" : department, 
        "courses" : courses, 
        "sessions" : sessions, 
        "item" : item
    }
    return render(request, "departments/detail/courses.html", context)


@allowed_groups(groups=["managers", "admins", "instructors"])
@login_required(login_url='login')
def department_detail_update_view(request, slug):
    department = get_object_or_404(Department, slug=slug)
    departmentChief = DepartmentChief.objects.get(department=department, to_date=None)
    users = User.objects.filter(groups__name__in=['instructors'], employee__department__name=department.name)
    if request.method == "POST":
        name = request.POST.get("name")
        publish_date = request.POST.get("publish")
        about = request.POST.get("about")

        department.name = name
        department.publish_date  = publish_date
        department.about = about

        department.save()
    context = {
        "department" : department, 
        "departmentChief" : departmentChief, 
        "users" : users
    }
    return render(request, "departments/detail/detail_update.html", context)

@allowed_groups(groups=["managers", "admins", "instructors"])
@login_required(login_url='login')
def manage_department_chief(request):
    dep_chief = ""
    if request.method== "POST":
        department = Department.objects.get(slug=request.POST.get("department"))
        user = User.objects.get(id=request.POST.get("chief"))
        from_date = request.POST.get("from_date")
        dep_chief = DepartmentChief.objects.get(department=department, to_date=None)


@allowed_groups(groups=["managers", "admins"])
@login_required(login_url='login')
def department_delete_view(request):
    department = Department.objects.get(slug=request.POST.get("slug"))
    department.delete()
    return redirect("department-list")