import re
from django.db import models
from subjects.models import  Subject
from accounts.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from students.models import Student
import random
import string
from django.urls import reverse



def random_course_code():
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))


def random_slug():
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(9))   


class Session(models.Model):
    SETTION_TYPE = (
        ("بهاری", "بهاری"),
        ("خزانی", "خزانی"),
    )

    session = models.DateField()
    session_type = models.CharField(
        max_length=20, choices=SETTION_TYPE, default="بهاری"
    )
    generate_auto = models.BooleanField(default=False)
    current_session = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.session}"

    def get_absolute_url(self):
        return reverse("session-detail", args=[self.session.year, self.session.month, self.session.day, self.session_type])


class Course(models.Model):
    SYSTEM = (
        ("کریدیت", "کریدیت"),
        ("قدیمی", "قدیمی"),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name="join_course", blank=True)

    code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    overview = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    system = models.CharField(max_length=20, choices=SYSTEM, default="کریدیت")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(random_course_code())
        if not self.slug:
            self.slug = slugify(random_slug() + "-" + self.title)
        return super().save(*args, **kwargs)



class CourseDetail(models.Model):

    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    color = models.CharField(max_length=200)
    image = models.ImageField(upload_to="course/images", default="course.png")


    def __str__(self):
        return f"{self.course} detail"




class Module(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    week = models.PositiveIntegerField(help_text="شما در کدام هفته ای از سمستر قرار دارید.", verbose_name="شماره هفته")
    title = models.CharField(max_length=200, help_text="عنوان ماجول شما چی هست؟", verbose_name="عنوان ماجول")
    content = models.TextField(help_text="توضیحات در مورد ماجول فوق.", verbose_name="توضیحات در مورد ماجول")


    def __str__(self):
        return self.title



class Content(models.Model):
    module = models.ForeignKey(Module, related_name="contents", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    video = models.FileField(upload_to="course/content/videos", null=True, blank=True)
    file = models.FileField(upload_to="course/content/files", null=True, blank=True)
    image = models.ImageField(upload_to="course/content/images", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"content for {self.module}"




