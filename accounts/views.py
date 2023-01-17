
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from accounts.models import User
from results.forms import EditResult
from students.models import Student
from .forms import EmployeeRegisterForm, StudentReigsterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import allowed_groups
from results.models import Result, ResultBulkUpload
from subjects.models import Subject
from django.forms.models import modelformset_factory
import  csv
from django.contrib.auth.hashers import make_password

# change password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
# verify email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage 
from django.conf import settings

EditResult = modelformset_factory(Result, fields=("subject", "class_activity", "assignment", "mid_term", "final", "project", "chances"), can_delete=True, extra=0)


def send_activition_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('accounts/auth/activate.html', {
        'user' : user,
        'domain' : current_site, 
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER, to=[user.email])
    try:
        email.send()
    except:
        messages.error(request, "لطفا به انترنت وصل شوید.")



def login_page(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        new_p = make_password(password)

        try:
            user = User.objects.get(email=email)
        except:
            return redirect("login")
        user = authenticate(request, email=email, password=password)
        if user == None:
            messages.error(request, "ایمیل یا رمز ورود اشتباه می باشد!")
            return redirect("login")
        if not user.is_email_verified:
            messages.error(request, "ایمیل شما تایید نشده. لطفا باکس ایمیل خود را چک کنید. ")
            send_activition_email(user, request)
            return render(request, "authentication/login.html")
        if user is not None:
            try:
                if user.last_login == None:
                    login(request, user)
                    return redirect("change-password")
                elif user.last_login != None:
                    login(request, user)
                    if request.user.is_student:
                        return redirect("student-dashboard")
                    elif request.user.is_staff:
                        return redirect("admin-dashboard")
                    else:
                        return redirect("employee-dashboard")
            except:
                messages.error(request, "ایمیل یا رمز ورود اشتباه می باشد!")

    return render(request, "authentication/login.html")


def logout_page(request):
    logout(request)
    return redirect("login")


# @login_required(login_url="login")
# def employee_register_view(request):
#     if request.method == "POST":
#         form = EmployeeRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "کارمند جدید موفقانه ثبت گردید.")
#             if request.user.is_staff == True:
#                 return redirect("admin-dashboard")
#             else:
#                 return redirect("/")
#     else:
#         form = EmployeeRegisterForm()

#     context = {
#         "form" : form
#     }

#     return render(request, "employees/register.html", context)

@login_required(login_url="login")
@allowed_groups(groups=["managers", "admins"])
def student_register_view(request):
    if request.method == "POST":
        form = StudentReigsterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "محصل جدید موفقانه ثبت سیستم گردید.")
            return redirect("student-score-all", Student.objects.last().id)
    else:
        form = StudentReigsterForm()
    return render(request, "accounts/student_register.html", {"form" : form})



@login_required(login_url="login")
@allowed_groups(groups=["managers", "admins"])
def student_scores_view(request, pk):
    student = Student.objects.get(pk=pk)
    
    not_scored_subjects = []
    for subject in Subject.objects.all():
        if subject.semester.semester_number < student.semester.semester_number:
            not_scored_subjects.append(subject)
    
    objects = [
        Result(
            subject=Subject.objects.get(pk=sbj.pk),
            student=student,
        )
        for sbj in not_scored_subjects
    ]

    if not student.result_set.all():
        result = Result.objects.bulk_create(objects)

    if request.method == "POST":
        form = EditResult(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your score has been updated successfully updated ")
            return redirect("student-score-all", student.pk)
    else:
        results = Result.objects.filter(subject__semester=student.semester.semester_number -1, student=student)
        form = EditResult(queryset=results)

    context = {
      "student" : student,
      "formset" : form, 
      "not_scored_subjects" : not_scored_subjects
    }
    return render(request, "accounts/student_score.html", context)

#//////////////////////////////////////////////
@login_required(login_url="login")
@allowed_groups(groups=["managers"])
def student_score_upload_view(request, pk):
    student = Student.objects.get(pk=pk)
    if request.method == "POST":
        file = request.FILES.get("result_file")
        if file == None:
            messages.error(request, "لطفا فایل مورد نظر را انتخاب نمایید.")
        
        try:
            ResultBulkUpload.objects.create(
                csv_file=file
            )
            messages.success(request, f"نمرات مربوط به محصل {student.f_name} {student.l_name} موفقانه ثبت سیستم گردید.")
            return redirect("department-detail", student.department.slug)
        except:
            messages.error(request, "اشتباه رخ داد لطفا فایل مورد نظر ره چک کرده و دوباره تلاش کنید.")
            return redirect("student-score-all", student.pk)
        
        

    context = {
        "student" : student
    }
    return render(request, "accounts/results/result_upload.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["managers"])
def result_csv_download_view(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="result_template.csv"'
    writer = csv.writer(response)
    writer.writerow([
        "subject", 
        "student",
        "student_ID",
        "mid_term", 
        "final", 
        "chances", 
        "assignment"
        ])

    return response



def lock_screen_view(request):
    user = request.session.get("user", request.user)
    context = {
        "user" : user
    }
    return render(request, "accounts/lock_screen.html", context)

# change password view
@login_required(login_url="login")
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "رمز ورود شما موفقانه ویرایش گردید. ")
            if request.user.is_student:
                return redirect("student-dashboard")
            elif request.user.is_staff:
                return redirect("admin-dashboard")
            else:
                return redirect("employee-dashboard")
        else:
            messages.error(request, "اشتباهی رخ داد، لطفا بررسی کرده و دوباره سعی کنید. ")

    else:
        form = PasswordChangeForm(request.user)


    return render(request, "accounts/auth/change_password.html", {"form" : form})





def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None


    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        messages.success(request, "ایمیل شما موفقانه تایید شد.")
        return redirect("login")

    
    return redirect(request, "accounts/auth/activate-failed.html", {"user" : user})



@login_required(login_url="login")
def verify_email_view(request):
    user = request.user

    send_activition_email(user, request)
    return render(request, "authentication/login.html")



