from django import template
from results.models import Result
from subjects.models import Subject
from students.models import Student
from departments.models import Semester


register = template.Library()

@register.simple_tag
def calculate_percentage(student, sememster):
    results = student.result_set.filter(student=student, subject__semester__exact=sememster)
    percentage = 0
    total = 1
    total_credit = 1
    for i in results:
        total_credit += i.subject.credit
        total += i.total_score()
    percentage = total / total_credit
    return round(percentage, 2)