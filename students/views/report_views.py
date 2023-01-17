from django.shortcuts import render, redirect
from courses.models import Course
from results.models import Result
from students.models import Student
from subjects.models import Subject
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_groups
from students.utils import endResult


@login_required(login_url="login")
@allowed_groups(groups=["students","managers", "admins"])
def semester_report_view(request, pk):
    student = Student.objects.get(pk=pk)
    results = []
    for result in Result.objects.all():
        if result.student == student and result.subject.semester == student.semester:
            results.append(result)
    subjects = Subject.objects.filter(department=student.department, semester=student.semester)
    
    my_courses = Course.objects.filter(students=student)
    # drawing charts for results
    courses = []
    score = []

    for result in results:
        if result.subject.semester == student.semester:
            courses.append(result.subject.subject)
            score.append(int(result.total_score()))
    
    total_credits = 0
    scores = 0
    percentage = 0
    passed_credits = 0
    grade = "D"

    for subject in subjects:
        total_credits += subject.credit

    for result in results:
        if result.subject.semester.semester_name == result.student.semester.semester_name:
            scores += result.total_score()
            if result.total_score() > 55:
                passed_credits += result.subject.credit
            if result.total_score() >= 55:
                result.is_pass = True
            else:
                result.is_pass = False
            result.save()    
    if passed_credits > (total_credits // 2) and student.semester.semester_number != 8:
        student.semester.semester_number += 1

        for course in my_courses:
            course.students.remove(student)
        student.save()
    try:
        percentage = scores / total_credits
    except:
        percentage = 0

    status = "ناکام"
    for r in results:
        if r.total_score() < 55:
            status = "چانس"
            break
        else:
            status = "کامیاب"
    if passed_credits < (total_credits // 2):
        status = "ناکام"
    
    if percentage < 55:
        grade = "F"
    elif percentage >= 55 or percentage <= 69:
        grade = "D"
    elif percentage >= 70 or percentage <= 79:
        grade = "C"
    elif percentage >= 80 or percentage <= 89:
        grade = "B"
    elif percentage >= 90 or percentage <= 100:
        grade = "A"
    context = {
        "student" : student,
        "results" : results, 
        "total_credits" : total_credits, 
        "scores" : scores, 
        "percentage" : percentage, 
        "passed_credits" : passed_credits, 
        "grade" : grade, 
        "score" : score, 
        "courses" : courses, 
        "status" : status
    }
    return render(request, "students/report/semester.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["students", 'managers', "admins", "instructors"])
def general_report_view(request, pk):
    student = Student.objects.get(pk=pk)
    results = student.result_set.filter(student=student)
    bulk = {}
    percentage = 0

    for result in results:

        assignment = 0
        mid_term = 0
        final = 0
        total = 1
        total_credit = 1
        percentage = 0
        subjects = []

        
        for subject in results:
            if student == result.student and subject.subject.semester.semester_number == result.subject.semester.semester_number:
                subjects.append(subject)
                total_credit += subject.subject.credit
                
                assignment += subject.class_activity + subject.assignment + subject.project
                mid_term += subject.mid_term
                final += subject.final
                total += subject.total_score()
                percentage = total / total_credit
        
        bulk[result.subject.semester.id] = {
            "semester" : result.subject.semester.semester_number,
            "subjects" : subjects,
            "assignment" : assignment,
            "mid_term" : mid_term,
            "final" : final,
            "total" : total, 
        }
    
    context = {
        "student" : student, 
        "results" : bulk, 
        "percentage" : percentage
    }
    return render(request, "students/report/general.html", context)

