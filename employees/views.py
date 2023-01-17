from tasks.models import Event
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from employees.models import Education, Employee, Experience
from .forms import UserProfileUpdateForm, EmployeeProfileUpdateForm, EmployeeEducation, EmployeeExperience
from django.contrib import messages
from courses.models import Course
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_groups
from students.models import Student
from subjects.models import Subject
from django.contrib.auth.models import Group, Permission
from accounts.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q


@login_required(login_url="login")
@staff_member_required
def create_employee_view(request):
    groups = Group.objects.exclude(name="students")
    if request.method == "POST":
        emp_id = request.POST.get("emp_id")
        name = request.POST.get("name")
        last_name = request.POST.get("last_name")
        father_name = request.POST.get("father_name")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        group = request.POST.getlist("group")

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
                print(g)
                selected_group, created = Group.objects.get_or_create(name=g)
                print(selected_group)
                user.groups.add(selected_group)
            
            user.save()
        
        try:
            Employee.objects.create(
                user=user,
                emp_unique_id=emp_id,
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
        "groups" : groups
    }

    return render(request, "employees/register.html", context)

@staff_member_required
def employee_list_view(request):
    params = request.GET.get("query")
    if params == None:
        params = ""
    
    employees = Employee.objects.filter(
        Q(f_name__icontains=params) |
        Q(l_name__icontains=params),
        user__is_employee=True,
        )
    context = {
        "employees" : employees
    }
    return render(
        request, 
        "employees/list.html",
        context
    )

@login_required(login_url="login")
@allowed_groups(groups=["managers", "instructors"])
def employee_dashboard_view(request):
    return render(request, "employees/employee/index.html")


@login_required(login_url="login")
@allowed_groups(groups=["instructors", "managers", "admins"])
def employee_profile(request):
    employee = request.user.employee
    experiences = Experience.objects.filter(employee=employee)
    educations = Education.objects.filter(employee = employee)
    courses = Course.objects.filter(owner=request.user)
    context = {"employee" : employee, "experiences" :  experiences, "educations" : educations, "courses" : courses}

    return render(request, "employees/profile/employee-profile.html", context)

@login_required(login_url="login")
@allowed_groups(groups=["instructors", "managers", "admins"])
def employee_profile_detail(request, pk):
    employee = Employee.objects.get(pk=pk)

    if request.method == "POST":
        u_form = UserProfileUpdateForm(request.POST or None, instance=request.user)
        p_form = EmployeeProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.employee)
        if u_form.save() and p_form.save():
            u_form.save()
            p_form.save()
            messages.success(request,"معلومات شما موفقانه ثبت سیستم گردید")
            return redirect("employee-profile")

    else:
        u_form = UserProfileUpdateForm(instance=request.user)
        p_form = EmployeeProfileUpdateForm(instance=request.user.employee)

    
    return render(request, "employees/profile/employee_profile_detail.html", {"u_form" : u_form, "p_form" : p_form})



@login_required(login_url="login")
@allowed_groups(groups=["instructors", "managers", "admins"])
def create_education_view(request, pk):
    employee = Employee.objects.get(pk=pk)
    if request.method == "POST":
        form = EmployeeEducation(request.POST or None, request.FILES or None)
        if form.is_valid():
            edu = form.save(commit=False)
            print(edu)
            edu.employee = employee
            edu.save()
            messages.success(request, "سابقه تحصیلی شما موفقانه ثبت سیستم گردید.")
            return redirect("employee-profile")
    else:
        form = EmployeeEducation()
    
    context = {
        "form" : form
    }

    return render(request, "employees/profile/education.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["instructors", "managers", "admins"])
def create_background_experience_view(request, pk):
    employee = Employee.objects.get(pk=pk)
    if request.method  == "POST":
        form = EmployeeExperience(request.POST or None, request.FILES or None)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.employee = employee
            exp.save()
            messages.success(request, "شما موفقانه معلومات در رابطه به سابقه کاری خود را ذخیره کردید.")
            return redirect("employee-profile")
    else:
        form = EmployeeExperience()

    context = {
        "form" : form
    }

    return render(request, "employees/profile/experience.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["instructors", "managers", "admins"])
def employee_detail_view(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    user = employee.user
    selected_permissions = user.user_permissions.all()
    permissions = Permission.objects.all()
    custom_permissions = {
        "selected" : [],
        "others" : []
    }
    for i in selected_permissions:
        custom_permissions["selected"].append(i)
    for j in permissions:
        if j not in selected_permissions:
            custom_permissions["others"].append(j)
    context = {
        "employee" : employee, 
        "permissions" : permissions, 
        "custom_permissions" : custom_permissions
    }
    return render(request, "employees/detail/index.html", context)

@login_required(login_url="login")
@allowed_groups(groups=["instructors", "managers", "admins"])
def employee_create_permission(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    user = employee.user
    if request.method == "POST":
        permissions = request.POST.getlist("permission")
        user.user_permissions.clear()
        for per in permissions:
            user.user_permissions.add(per)

        user.save()
    return redirect("employee_detail_route", employee.id)



@login_required(login_url="login")
@allowed_groups(groups=["instructors", "managers", "admins"])
def update_employee_info(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        unique_id = request.POST.get("emp_id")
        f_name = request.POST.get("name")
        l_name = request.POST.get("last_name")
        father_name = request.POST.get("father_name")
        phone_number = request.POST.get("phone_number")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        address = request.POST.get("address")
        avatar = request.FILES.get("avatar")

        print(f_name)
    
        employee.emp_unique_id = unique_id
        employee.f_name=f_name
        employee.l_name=l_name
        employee.father_name=father_name
        employee.phone_number=phone_number
        employee.gender=gender
        employee.dob=dob
        employee.address=address
        employee.avatar=avatar
        employee.save()

    context = {
        "employee" : employee
    }

    return render(request, "employees/detail/update.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["instructors", "managers", "admins"])
def delete_employee(request):
    employee = Employee.objects.get(id=request.POST.get("employee_id"))
    employee.delete()
    return redirect("employee_list")
