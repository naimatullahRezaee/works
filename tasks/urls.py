from django.urls import path
from . import views


urlpatterns = [
    path("assignment/create/<str:pk>/",  views.create_assignment_view, name="create-assignment"),
    path("assignment/open/student/<str:pk>/", views.open_assignment_for_student_view, name="open-student-assignment"),
    path("assignment/open/instructor/<str:pk>/", views.open_assignment_for_instructor_view, name="open-instructor"),
    path("assignment/assign/score/<str:pk>/<str:student_pk>/", views.check_and_score_assignment, name="assign-score"),

    # events paths
    path("event/create/select/course/", views.create_event_phase_one, name="select-course"), 
    path("event/create/<slug:slug>/", views.create_event_view, name="create-event"),
    path("event/list/", views.event_list_view, name="event-list"), 
    path("event/student/list/", views.student_event_list_view, name="student-event-list")
]