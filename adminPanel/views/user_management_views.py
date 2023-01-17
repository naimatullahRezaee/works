from django.shortcuts import redirect, render
from employees.models import Employee
from students.models import Student
from django.contrib.auth.models import Group, Permission
from subjects.models import Subject
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_groups
from django.contrib import messages
from accounts.models import User
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_profile(request):
    user = request.user
    profile = user.employee
    context = {
        'profile' : profile
    }
    return render(request, "adminPanel/profile/index.html", context)

@staff_member_required
def admin_update_profile_info(request):
    profile = request.user.employee
    if request.method == "POST":
        name = request.POST.get("name")
        last_name = request.POST.get("last_name")
        father_name = request.POST.get("father_name")
        gender = request.POST.get('gender')
        dob = request.POST.get("dob")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        bio = request.POST.get("bio")
        avatar = request.FILES.get("avatar")

        profile.f_name = name
        profile.l_name = last_name
        profile.father_name = father_name
        profile.gender = gender
        profile.phone_number = phone_number
        profile.address = address
        profile.bio = bio
        profile.avatar = avatar
        profile.save()

        return redirect("admin_profile_info") 
    context = {
        'profile' : profile
    }

    return render(request, "adminPanel/profile/update_info.html", context)


@staff_member_required
def groups_list_view(request):
    groups = Group.objects.all()

    context = {
        "groups" : groups
    }

    return render(request, "adminPanel/groups/list.html", context)


@staff_member_required
def create_group_views(request):

    if request.user.is_staff == True and request.method == "POST":
        name = request.POST.get("name")
        try:
            Group.objects.create(
                name=name
            )
            messages.success(request, "گروپ جدید موفقانه ایجاد شد.")
            return redirect("all-groups")
        except:
            messages.error(request, "گروپ با این نام در حال حاضر موجود می باشد.")
            return redirect("all-groups")




@staff_member_required
def group_delete_view(request, pk):
    group = Group.objects.get(pk=pk)
    if request.user.is_staff == True and request.method == "POST":
        try:
            group.delete()
            messages.success(request, "گروپ فوق از موفقانه حذف گردید.")
            return redirect("all-groups")
        except:
            messages.error(request, "عملیات ناموفقانه بود. گروپ فوق حذف نگردید.")
            return redirect("all-groups")
    
    context = {"group" : group}

    
    return render(request, "adminPanel/groups/delete.html", context)


@staff_member_required
def update_group_view(request):
    if request.user.is_staff == True and request.method == "POST":
        name = request.POST.get("name")
        id = request.POST.get("id")
        group = Group.objects.get(pk=id)

        try:
            group.name = name
            group.save()
            messages.success(request, f"گروپ {group} موفقانه ویرایش گردید.")
            return redirect("all-groups")
        except:
            messages.error(request, "اشتباهی رخ داد لطفا دوباره تلاش کنید.")
            return redirect("all-groups")


@staff_member_required
def group_detail_view(request, pk):
    group = Group.objects.get(pk=pk)
    selected_permissions = group.permissions.all()
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
    members = group.user_set.all()
    users = User.objects.exclude(username=request.user.username)

    if request.method == "POST" and request.user.is_staff == True:
        member = User.objects.get(pk=request.POST.get("id"))
        try:
            group.user_set.remove(member)
            messages.success(request, f"کاربر {member.first_name} از این گروپ حذف گردید.")
            return redirect("all-groups")
        except:
            messages.error(request, "اشتباهی رخ داده لطفا دوباره سعی کنید.")
            return redirect('group-detail', group.pk)


    context = {
        "group" : group, 
        "members" : members, 
        "users" : users,
        "permissions" : permissions,
        "selected_permissions" : selected_permissions,
        "custom_permissions" :custom_permissions     
    }

    return render(request, "adminPanel/groups/detail.html", context)


@staff_member_required
def add_user_to_group_view(request):
    if request.user.is_staff == True and request.method == "POST":
        user = User.objects.get(pk=request.POST.get("user_id"))
        group = Group.objects.get(pk=request.POST.get("group_id"))
        if user is not None:
            try:
                group.user_set.add(user)
                messages.success(request, f"کاربر جدید به این گروپ موفقانه اضافه گردید.")
                return redirect("group-detail", group.pk)
            except:
                messages.error(request, "یک اشتباه رخ داد لطفا دوباره سعی کنید. ")
                return redirect("group-detail", group.pk)



@staff_member_required
def permission_list(request):
    permissions = Permission.objects.all()

    context={
        "permissions": permissions
    }
    return render(request, "adminpanel/groups/detail.html", context)



@staff_member_required
def create_permission(request, id):
    group = Group.objects.get(id=id)

    if request.method == "POST":
        permissions = request.POST.getlist("permission")
        

        group.permissions.clear()
        for i in permissions:
            group.permissions.add(i)
        
        group.save()
        messages.success(request, "صلاحیت موفقانه به گروپ اضافه گردید")
    return redirect("group-detail", group.id)




@allowed_groups(groups=["admins", "manager"])
def employee_detail_view(request, pk):
    employee = Employee.objects.get(pk=pk)
    
    context = {
        "employee" : employee
    }
    return render(request, "adminPanel/employees/detail.html", context)



@staff_member_required
def employee_delete_view(request, pk):

    employee = Employee.objects.get(pk=pk)
    if request.method == "POST":
        employee.delete()
        messages.success(request, f"کارمند {employee.f_name} {employee.l_name} موفقانه از سیستم حذف شد.")
        return redirect("department-detail", employee.department.slug)

    context = {
        "employee" : employee
    }

    return render(request, "adminPanel/employees/delete.html", context)


