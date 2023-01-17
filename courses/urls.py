from django.urls import path
from . import views


urlpatterns = [
    path("course/mine/<int:page>/", views.list_course_view, name="list-course"),
    path("course/create/", views.create_course_view, name="create-course"),
    path("course/detail/<slug:slug>/", views.course_detail_view, name="course-detail"),
    path("course/contents/<slug:slug>/<int:pk>/", views.course_content_view, name="course-content"), 
    path("content/update/<str:pk>/", views.content_update_view, name="update-content"), 
    path("content/delete/", views.delete_content_view, name="delete-content"), 
    path("course/approve/", views.approve_course, name="approve-course"), 
    # session list

    path("session/list/", views.session_list_view, name="session-list"), 
    path('session/detail/<int:year>/<int:month>/<int:day>/<str:type>/', views.session_detail_view, name="session-detail"), 
    path("session/create/", views.session_create_view, name="session-create"),

    # admin side course detail 
    path("course/<slug:slug>/", views.course_admin_detail_view, name="course_admin_detail_view")
]