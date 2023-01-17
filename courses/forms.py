from django import forms
from .models import Course, CourseDetail, Content



class UpdateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['session', "title", 'overview', 'system']


class UpdateCourseDetailForm(forms.ModelForm):
    class Meta:
        model = CourseDetail
        fields = ["image", "color"]
        


class ContentUpdateForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = [
            "title", 
            "text", 
            "video", 
            "file", 
            "image"
        ]