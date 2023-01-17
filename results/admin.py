from django.contrib import admin

# Register your models here.
from .models import Result,CourseResultUpload

admin.site.register(Result)
admin.site.register(CourseResultUpload)