from django.contrib import admin
from .models import Department, Semester, DepartmentChief, DepartmentProgramLevel


admin.site.register(Department)
admin.site.register(Semester)
admin.site.register(DepartmentProgramLevel)
admin.site.register(DepartmentChief)
