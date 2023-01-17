from pickle import LONG_BINPUT
from django.shortcuts import redirect, render
from .forms import InstructorEvaluationForm
from .models import Evaluation, InstructorEvaluation
from employees.models import Employee
from courses.models import Course
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_groups
# Create your views here.


@login_required(login_url="login")
@allowed_groups(groups=["students"])
def evaluation_list_view(request):
    student = request.user.student
    evaluations = []
    evaluation = Evaluation.objects.all()
    for a in evaluation:
        if a.teacher.user.course_set.filter(students=student):
            evaluations.append(a)
        for res in a.instructorevaluation_set.all():
            if res.student == student:
                evaluations.remove(a)
     
    context = {
        "evaluations" : evaluations
    }
    return render(request, "assessments/list.html", context)

@login_required(login_url="login")
@allowed_groups(groups=["students"])
def create_evaluation_view(request, pk, evaluation_id):
    employee = Employee.objects.get(pk=pk)
    evaluation = Evaluation.objects.get(pk=evaluation_id)
    if request.method == "POST":
        form = InstructorEvaluationForm(request.POST)
        if form.is_valid():
            evaluate = form.save(commit=False)
            evaluate.evaluation = evaluation
            evaluate.student = request.user.student
            evaluate.save()
            messages.success(request, "تشکر از همکاری تان شما موفقانه استاد مورد نظر را ارزیابی کردید.")
            return redirect("/")
    else:
        form = InstructorEvaluationForm()
    context = {
        "employee" : employee, 
        "form" : form
    }

    return render(request, "assessments/evaluate.html", context)
