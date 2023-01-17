from django.contrib import admin

# Register your models here.
from .models import Employee, Education, Experience, EmployeeNationalityCart

admin.site.register(Employee)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(EmployeeNationalityCart)