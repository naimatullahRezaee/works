from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("room/<str:course_id>/", views.course_discussion, name="course_discussion")
]