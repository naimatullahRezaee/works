from django import forms
from .models import InstructorEvaluation



class InstructorEvaluationForm(forms.ModelForm):

    class Meta:
        model = InstructorEvaluation
        fields = '__all__'
        exclude = ["evaluation", "student"]