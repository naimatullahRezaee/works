from django.contrib import admin

# Register your models here.
from .models import InstructorEvaluation, Evaluation

admin.site.register(InstructorEvaluation)
admin.site.register(Evaluation)