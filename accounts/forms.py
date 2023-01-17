from django.db import transaction
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from employees.models import Employee
from students.models import Student
from departments.models import Department, Semester

class EmployeeRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True)
    GENDER = (
        ("خانم", "خانم",),
        ("آقا", "آقا"),
    )
    emp_unique_id = forms.CharField(max_length=200)
    f_name = forms.CharField(max_length=200)
    l_name = forms.CharField(max_length=200)
    father_name = forms.CharField(max_length=200)
    gender = forms.ChoiceField(choices=GENDER)
    dob = forms.DateField(required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    @transaction.atomic
    def save(self, commit=True):
        
        cleaned_data = super(EmployeeRegisterForm, self).clean()
        emp_unique_id = cleaned_data.get("emp_unique_id")
        f_name = cleaned_data.get("f_name")
        l_name = cleaned_data.get('l_name')
        father_name = cleaned_data.get("father_name")
        gender = cleaned_data.get("gender")
        dob = cleaned_data.get("dob")
        department = cleaned_data.get("department")
        user = super().save(commit=False)
        user.is_employee = True
        if commit:
            user.save()
            user.groups.add(*self.cleaned_data.get("groups"))
        emp = Employee.objects.create(
            user=user,
            emp_unique_id=emp_unique_id,
            f_name=f_name,
            l_name=l_name,
            father_name=father_name,
            gender=gender,
            dob=dob,
            department=department
        )
        return user



class StudentReigsterForm(UserCreationForm):

    email = forms.EmailField(max_length=255)
    GENDER = (
        ("خانم", "خانم"),
        ("آقا", "آقا"),
    )
    SECTION = (
        ("A", "A"),
        ("B", "B")
    )
    kankor_id = forms.CharField(max_length=200)
    f_name =  forms.CharField(max_length=200)
    l_name =  forms.CharField(max_length=200)
    father_name =  forms.CharField(max_length=200)
    grand_father_name =  forms.CharField(max_length=200)
    school_name = forms.CharField(max_length=200)
    score = forms.CharField()
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    province = forms.CharField(max_length=200)
    gender = forms.ChoiceField(choices=GENDER)
    semester = forms.ModelChoiceField(queryset=Semester.objects.all())
    section = forms.ChoiceField(choices=SECTION)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    @transaction.atomic
    def save(self):
        cleaned_data = super(StudentReigsterForm, self).clean()
        kankor_id = cleaned_data.get("kankor_id")
        f_name = cleaned_data.get("f_name")
        l_name = cleaned_data.get("l_name")
        father_name = cleaned_data.get("father_name")
        grand_father_name = cleaned_data.get("grand_father_name")
        school_name = cleaned_data.get("school_name")
        score = cleaned_data.get("score")
        department = cleaned_data.get("department")
        province = cleaned_data.get("province")
        gender = cleaned_data.get("gender")
        semester = cleaned_data.get("semester")
        section = cleaned_data.get("section")

        user = super().save(commit=False)
        user.is_student = True
        user.save()
        user.groups.add(Group.objects.get(name="students"))
        
        student = Student.objects.create(
            user=user, 
            kankor_id=kankor_id,
            f_name=f_name,
            l_name=l_name,
            father_name=father_name,
            grand_father_name=grand_father_name,
            school_name=school_name,
            score=score,
            department=department, 
            province=province,
            gender=gender, 
            semester=semester, 
            section=section
        )

        return user

        

