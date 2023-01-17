from django.urls import path
from . import views


urlpatterns = [
    # path("create/assessment/", views.create_assessment_view, name="create-assessment")
    path("evaluate/list/all/", views.evaluation_list_view, name="evaluation-list"), 
    path("evaluate/<str:pk>/<str:evaluation_id>/", views.create_evaluation_view, name="evaluate-detail")
]