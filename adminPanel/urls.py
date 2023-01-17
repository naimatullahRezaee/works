from django import views
from django.urls import path
from .views import (
    general_views, 
    user_management_views, 
    subject_views, 
    course_views
    )



urlpatterns = [
    path("super/dashboard/", general_views.dashboard, name="admin-dashboard"),
    path("groups/all/", user_management_views.groups_list_view, name="all-groups"), 
    path("group/new/", user_management_views.create_group_views, name="create-new-group"), 
    path("group/delete/<str:pk>/", user_management_views.group_delete_view, name="delete-group"),
    path('group/update/', user_management_views.update_group_view, name="update-group"),
    path("group/detail/<str:pk>/", user_management_views.group_detail_view, name='group-detail'), 
    path("group/add/member/", user_management_views.add_user_to_group_view, name="add-member-to-group"), 
    path("permission/create/<str:id>/", user_management_views.create_permission, name="create-permission"),
    
    path("employee/<str:pk>/detail/", user_management_views.employee_detail_view, name="employee-detail"), 
    path("employee/<str:pk>/delete/", user_management_views.employee_delete_view, name="employee-delete"), 

    path("profile/detail/", user_management_views.admin_profile, name="admin_profile_info"),
    path("profile/detail/update/", user_management_views.admin_update_profile_info, name="update_profile_detail_info"),
    # subjects

    path("subject/<slug:slug>/detail/", subject_views.subject_detail_view, name="subject-detail"), 
    path("subject/<slug:slug>/delete/", subject_views.subject_delete_view, name="subject-delete"), 

    # courses
    path("course/<slug:slug>/detail/admin/", course_views.course_detail_view, name="course-detail-admin"), 
    path("course/<slug:slug>/review/", course_views.course_review_view, name="course-review"),


]
