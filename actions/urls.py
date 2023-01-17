from django.urls import path
from . import views


urlpatterns  = [
    path("detail/<str:pk>/", views.action_detail, name="action_detail"),
]