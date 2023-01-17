from django.shortcuts import get_object_or_404, redirect, render
import weasyprint
import results
from .models import Result, CourseResultUpload, ResultBulkUpload
from .forms import CreateResult, EditResult
from students.models import Student
from courses.models import Course
from django.contrib import  messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_groups
from subjects.models import Subject

# generating pdf file
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import csv

# Create your views here.



@login_required(login_url="login")
@allowed_groups(groups=["instructors"])
def result_start_view(request, slug):
    subject = Subject.objects.get(slug=slug)
    context = {
        "subject" : subject
    }
    return render(request, "results/start.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["instructors"])
def create_result(request, slug):
    subject = Subject.objects.get(slug=slug)
    
    students = subject.course_set.last().students.all()

    if request.method == "POST":
        # after visiting the second page
        if "finish" in request.POST:
            form = CreateResult(request.POST)
            if form.is_valid():
                # course = form.cleaned_data["courses"]
                students = request.POST["students"]
                results = []

                for student in students.split(","):
                    stu = Student.objects.get(pk=student)
                    print(stu)
                    check = Result.objects.filter(
                        subject=subject, 
                        student=stu
                    ).first()
                    if not check:
                        results.append(
                            Result(
                                subject=subject, 
                                student=stu
                            )
                        )
                Result.objects.bulk_create(results)
                return redirect("edit-results", subject.slug)
        id_list = request.POST.getlist("students")
        if id_list:
            form = CreateResult(
                initial={"subject" : subject}
            )
            studentlist = ",".join(id_list)
            return render(request, "results/create_result_page2.html", {"students" : studentlist, "count" : len(id_list), "form" : form, "subject" : subject})
        else:
            messages.warning(request, "لطفا یک یا چند شاگرد را انتخاب کنید.")
    return render(request, "results/create_result.html", {"students" : students, "subject" : subject})


@login_required(login_url="login")
@allowed_groups(groups=["instructors"])
def edit_results(request, slug):
    subject = Subject.objects.get(slug=slug)
    if request.method == "POST":
        form = EditResult(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "لیست نمرات جدید اضافه و ذخیره گردید.")
            return redirect("edit-results", subject.slug)
    else:
        results=  Result.objects.filter(
            subject=subject
            )
        form = EditResult(queryset=results)
    return render(request, "results/edit_results.html", {"formset" : form, "subject" : subject})



# generate pdf view

def result_pdf_view(request, slug):
    subject = get_object_or_404(Subject, slug=slug)
    course = subject.course_set.filter(status=True).last()
    instructor = course.owner
    html = render_to_string("results/pdf.html", {"result" : subject.result_set.all(), "subject" : subject, "instructor" : instructor})

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f"filename=result_{subject.subject}.pdf"
    try:
        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=[
            weasyprint.CSS(settings.STATIC_ROOT  + 'assets/css/bootstrap.min.css')
        ])
    except:
        return HttpResponse("something went wrong ")
    return response


@login_required(login_url="login")
@allowed_groups(groups=["instructors"])
def course_score_upload(request, slug):
    subject = get_object_or_404(Subject, slug=slug)
    course = subject.course_set.filter(status=True).last()
    if request.method == "POST":
        if request.user == course.owner:
            file = request.FILES.get("course_result_file")
            CourseResultUpload.objects.create(
                    csv_file=file
                )
            return redirect("/")
        
    context = {
        "subject":subject
    }
    return render(request, "results/upload_score_file.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["instructors"])
def download_csv_file(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="score_template.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        "f_name",
        "father_name", 
        "subject", 
        "mid_term_score", 
        "final_score", 
        "activity_score", 
        "project_score", 
        "homework_score", 
        "chance"
    ])
    return response
