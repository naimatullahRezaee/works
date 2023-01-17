from django.db import models
from departments.models import Department, Semester
import random
import string
from django.utils.text import slugify


def random_slug():
    return "".join(random.choice(string.ascii_letters+ string.digits) for _ in range(6))


class Subject(models.Model):
    SUBJECT_TYPE = (
        ("اصلی", "اصلی"),
        ("فرعی", "فرعی")
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    code = models.CharField(max_length=200, unique=True)
    credit = models.IntegerField()
    slug = models.SlugField(max_length=200)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject_type = models.CharField(max_length=20, choices=SUBJECT_TYPE, default="اصلی")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(random_slug() + "_" + self.subject)
        super().save(*args, **kwargs)
# class for subject prerequsites





class SubjectBulkUpload(models.Model):
    csv_file = models.FileField(upload_to="subjects/bulk/")
    uploaded_at = models.DateTimeField(auto_now=True)

