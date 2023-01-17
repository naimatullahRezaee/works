from django.urls import path
from .views import views
from .views import report_views

urlpatterns = [
    path("student/dashboard/", views.student_dashboard, name="student-dashboard"),
    path("student/profile/first/page/", views.student_profile, name="student-profile"),
    path("student/profile/detail/page/<str:pk>/", views.profile_detail, name="profile-detail"),

    # course
    path("students/courses/start/", views.student_course_start_view, name="course-start"),
    path("students/courses/relevant/", views.student_relevant_course_view, name="relevant-course"),
    path("students/courses/join/<slug:slug>/", views.join_to_course_view, name="join-course"),
    path("students/courses/mine/<int:page>/", views.my_courses_view, name="my-courses"),

    # report
    path("report/semester/<str:pk>/", report_views.semester_report_view, name="semester-report"),
    path("report/general/<str:pk>/", report_views.general_report_view, name="general-report"), 

    # activities
    path("activit/mine/", views.my_activity_view, name="my-activity"), 
    # departments and subjects

    path("department/subjects/info/", views.department_subject_view, name="department-subject"), 

    # student upload
    path("student/upload/", views.student_bulk_upload_view, name="student-upload"),
    path("student/download_csv/", views.student_csv_download_view, name="student-download-csv"),

    # * student detail and more
    path("student/<str:pk>/detail/", views.student_detail_info, name="student_detail_actions"),
    path("student/delete/", views.delete_student, name="delete_student")

]