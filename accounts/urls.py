from django.urls import path
from . import views
# reset password route
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("account/login/", views.login_page, name="login"),
    path("account/logout/", views.logout_page, name="logout"),
    # path("account/register/emp/", views.employee_register_view, name="register-emp"), 
    path("account/register/student/", views.student_register_view, name="register-student"),
    path("accont/lock/screen/", views.lock_screen_view, name="lock-screen"), 
    path("account/change/password/", views.change_password, name="change-password"),
    path("activate-user/<uidb64>/<token>/", views.activate_user, name="activate"),

    path("email-verification/", views.verify_email_view, name="verify_email"),


    path("student/<str:pk>/scores/", views.student_scores_view, name="student-score-all"),
    path('student/<str:pk>/upload/score/', views.student_score_upload_view, name="student-upload-file"), 
    path("student/result/download/csv/", views.result_csv_download_view, name="result-download-csv"), 


    # request for new password
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="accounts/auth/password_reset.html"), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="accounts/auth/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='accounts/auth/password_reset_confirm.html'), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name="accounts/auth/password_reset_complete.html"), name="password_reset_complete"),

]