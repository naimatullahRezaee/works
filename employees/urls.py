from django.urls import path
from . import views


urlpatterns = [
    path("", views.employee_dashboard_view, name="employee-dashboard"),
    path("employee/register/", views.create_employee_view, name="register_employee"),
    path("employee/profile/info/", views.employee_profile, name="employee-profile"),
    path("employee/profile/detail/<str:pk>/", views.employee_profile_detail, name="employee-detail1"), 
    path("employee/profile/education/<str:pk>/", views.create_education_view, name="education-background"),
    path("employee/profile/experience/<str:pk>/", views.create_background_experience_view, name="work-experience"),
    path("employee/members/lists/", views.employee_list_view, name="employee_list"), 
    path("employee/<str:pk>/detail/", views.employee_detail_view, name="employee_detail_route"),
    path("employee/<str:pk>/update/", views.update_employee_info, name="update_employee_info"),
    path("employee/delete/", views.delete_employee, name="delete_employee"),
    # assign permission to a user
    path("employee/<str:pk>/assign/perm/", views.employee_create_permission, name="employee_create_permission"),
]