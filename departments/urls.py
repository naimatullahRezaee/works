from django.urls import path
from . import views

urlpatterns = [
    path("department/list/", views.department_list_view, name="department-list"), 
    path("department/create/", views.create_department_view, name="department-create"),
    path("department/<slug:slug>/detail/", views.department_detail_view, name='department-detail'),
    path("department/<slug:slug>/program/", views.department_program, name="department_program"), 
    path("department/<slug:slug>/students/", views.department_students_list, name="department_student"),
    path("department/<slug:slug>/subjects/", views.department_subject_list, name="department_subject_list"),
    path("department/<slug:slug>/instructors/", views.department_instructors_list, name="department_instructors_list"),
    path("department/<slug:slug>/create/instructors/", views.department_create_instructor, name="department_create_instructor"), 
    path("department/<slug:slug>/courses/", views.department_courses, name="department_courses"),
    path("department/<slug:slug>/<str:current_session>/courses/", views.department_courses, name="department_courses_by_session"),
    path("department/<slug:slug>/update/", views.department_detail_update_view, name="department_detail_update_view"),
    path("department/delete/", views.department_delete_view, name="department_delete_view")
]