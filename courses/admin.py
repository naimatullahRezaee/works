from django.contrib import admin

from .models import Session, Course, CourseDetail,Content, Module


admin.site.register(Session)
admin.site.register(Course)
admin.site.register(CourseDetail)
admin.site.register(Content)
admin.site.register(Module)
