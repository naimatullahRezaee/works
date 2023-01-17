from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.schedule_list, name="schedule_list"),
    path("create/step1/", views.create_new_schedule, name="create_schedule_step1"),
    path("create/<slug:slug>/step2/", views.create_schedule_step2, name="create_schedule_step2"),
    path("create/<slug:slug>/<str:id>/final/", views.create_schedule_final, name="create_schedule_final")
]