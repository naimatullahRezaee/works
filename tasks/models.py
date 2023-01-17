from hashlib import blake2b
from django.db import models
from jalali_date import date2jalali,datetime2jalali
from courses.models import Content, Course
from accounts.models import User
from ckeditor_uploader.fields import RichTextUploadingField

from students.models import Student

class Assignment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to="assignments/", blank=True, null=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    # expir_at = models.DateTimeField()
    expire_date = models.DateField()
    expire_time = models.TimeField()
    score = models.IntegerField(default=0)
    lock_after_expiration = models.BooleanField(default=False)
    is_submitted  = models.ManyToManyField(Student, blank=True)


    def __str__(self):
        return self.title
    
    def get_jalali_datetime(self):
        return date2jalali(self.expire_date)


class Respond(models.Model):
    DIFFICULITIES = (
        ("آسان", "آسان"),
        ("متوسط", "متوسط"),
        ("سخت", "سخت"),
        ("دشوار", "دشوار"),
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True)
    difficulties = models.CharField(max_length=20, choices=DIFFICULITIES, default="آسان")
    file = models.FileField(upload_to="responds/", blank=True)
    # it should be change in to persian
    respond_at = models.DateTimeField(auto_now_add=True)
  

    def __str__(self):
        return self.title

    def get_jalali_datetime(self):
        return date2jalali(self.respond_at)



class AssignmentScore(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True)
    score = models.DecimalField(decimal_places=2, max_digits=4)


    def __str__(self):
        return f"{self.student.user.first_name}'s score for {self.assignment.title} assignment"



class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    # receiver
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

    