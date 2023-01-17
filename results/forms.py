from django import forms
from django.forms import modelformset_factory
from .models import Result
from courses.models import Course
from students.models import Student
from subjects.models import Subject



class CreateResult(forms.Form):
    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all()
    )



EditResult = modelformset_factory(Result, fields=(
    "class_activity",
    "assignment",
    "mid_term",
    "final",
    "project",
    "chances"
), extra=0, can_delete=True)