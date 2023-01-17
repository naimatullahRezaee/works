from django.db import models
from departments.models import Department, Semester
from courses.models import Session
from employees.models import Employee
from subjects.models import Subject
# Create your models here.


"""
todo to build out the schedule model we need the following relations
    ? 1 - department
    ? 2 - semester
    ? 3 - sessions
    ? 4 - subject
    ? 5 - official days
    ? 6 - official hours
"""


class Schedule(models.Model):
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Employee, on_delete=models.CASCADE)
    days = models.CharField(max_length=250)
    hours = models.CharField(max_length=250)
    from_time = models.TimeField()
    to_time = models.TimeField()

    def __str__(self):
        return self.days