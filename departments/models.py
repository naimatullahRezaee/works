from django.db import models
from accounts.models import User
import random
import string
from django.utils.text import slugify



def random_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))

class Department(models.Model):
    STATUS = (
        ("فعال", "فعال"),
        ("غیر فعال", "غیر فعال"),
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=200)
    publish_date = models.DateField(null=True, blank=True)
    status = models.CharField(choices=STATUS, default="فعال", max_length=20)
    about = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(random_slug() + "_" + self.name)
        super(Department, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class DepartmentChief(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    from_date = models.DateField()
    to_date =models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-from_date']

    def __str__(self):
        return f"{self.department.name}'s chief"


class DepartmentProgramLevel(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    level = models.CharField(max_length=200)

    def __str__(self):
        return self.level

class Semester(models.Model):
    program = models.ForeignKey(DepartmentProgramLevel, on_delete=models.CASCADE, null=True, blank=True)
    semester_number = models.PositiveIntegerField(default=1)
    semester_name = models.CharField(max_length=130)

    def __str__(self):
        return f"{self.semester_name} {self.program.level} {self.program.department.name}"


