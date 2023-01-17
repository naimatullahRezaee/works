from urllib import request
from django import forms

from courses.models import Course
from .models import Assignment, Respond, Event



class AssignmentCreateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["title", "description", "file", "expire_date", "expire_time", "score", "lock_after_expiration"]


class RespondForm(forms.ModelForm):
    class Meta:
        model = Respond
        fields = '__all__'
        exclude = ["sender", "assignment"]


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title", 
            "description",
            "start_date", 
            "end_date",
        ]

        widgets = {
            "title" : forms.TextInput(
                attrs={"class" : "form-control", "placeholder" : "عنوان رویداد"}
            ),
            "description" : forms.Textarea(
                attrs={"class" : "form-control", "placeholder" : "توضیحات در مورد رویداد فوق"}
            ),
            "start_date" : forms.DateInput(
                attrs={
                    "type"  : "datetime-local",  "class" : "form-control"
                },
                format="%Y-%m-%dT%H%M",
            ),
            "end_date" : forms.DateInput(
                attrs={"type" : "datetime-local", "class" : "form-control"}, 
                format="%Y-%m-%dT%H%M"
            ),
        }
        exclude = ["user"]

    def __init__(self, *args, user=None, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["start_date"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_date"].input_formats = ("%Y-%m-%dT%H:%M",)
