from django.contrib.auth.models import User
from django import forms
from .models import Employee, Education, Experience


class UserProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "email"]



class EmployeeProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "phone_number", 
            "bio",
            "address", 
            "avatar"
        ]



class EmployeeEducation(forms.ModelForm):
    class Meta:
        model = Education
        fields = [
            "title", 
            "university", 
            "start_date", 
            "finish_date", 
            "diploma", 
            "description"
        ]
        exclude = ["user"]


class EmployeeExperience(forms.ModelForm):
    class Meta:
        model = Experience
        fields = [
            "org", 
            "position", 
            "from_date", 
            "finish_date", 
            "description", 
            "document"
        ]

        exclude = ["user"]
