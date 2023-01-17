from django.contrib.auth.models import  User
from django.contrib.auth.forms import UserCreationForm
from .models import Student, StudentBulkUpload
from django import forms



class StudentUploadForm(forms.ModelForm):
    class Meta:
        model = StudentBulkUpload
        fields = ["csv_file"]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email" , "username"]


class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "phone",
            "cart",
            "cart_number", 
            "page_number",
            "register_number", 
            "volume_number",
            "cart_image",

            "hostel", 
            "wing_number", 
            "room_number", 
            "graduated_from_school", 
            "rel_with_std", 
            "rel_name", 
            "rel_job", 
            "rel_phone1",
            "rel_phone2",
            "rel_current_address", 
            "avatar"
        ]