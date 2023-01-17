from django.shortcuts import render, redirect

# Create your views here.
from .models import Subject, SubjectBulkUpload
from .forms import SubjectCreateForm
from django.contrib import messages
from django.http import HttpResponse
import csv
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_groups



@login_required(login_url="login")
@allowed_groups(groups=["managers", "admins", "instructors"])
def subject_list(request):
    subjects = Subject.objects.all()
    context = {
        "subjects" : subjects
    }
    return render(request, "subjects/subject_list.html", context)

@login_required(login_url="login")
@allowed_groups(groups=["managers", "admins", "instructors"])
def create_subject(request):
    if request.method == "POST":
        form = SubjectCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "مضمون جدید به لیست مضامین موفقانه اضافه شد")
            return redirect("subject-create")
    else:
        form = SubjectCreateForm()
    context = {
        "form" : form
    }
    return render(request, "subjects/form.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["managers", "admins", "instructors"])
def subject_bulk_upload_view(request):
    if request.method == "POST":
        file = request.FILES.get("subject_file")
        if file == None:
            messages.error(request, "لطفا لیست مضامین را انتخاب و بعدا ارسال نمایید.")
            return redirect("subject-upload")
        try:
            SubjectBulkUpload.objects.create(
                csv_file=file
            )
            messages.success(request, "لیست کریکولم آپلود و موفقانه ثبت سیستم گردید.")
            return redirect("subject-upload")
        except:
            messages.error(request, "اشتباهی رخ داده لطفا فایل خود را دوباره چک کرده و دوباره آپلود نمایید.")
            return redirect("subject-upload")
        
            

    return render(request, "subjects/subject_upload.html")


@login_required(login_url="login")
@allowed_groups(groups=["managers", "admins", "instructors"])
def subject_csv_download_view(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="subject_template.csv"'
    writer = csv.writer(response)
    writer.writerow(
        [
            "department",
            "subject",
            "code",
            "credit",
            "semester",
            "subject_type",
            "description",
        ]
    )

    return response