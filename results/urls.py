from django.urls import path
from . import views


urlpatterns = [
    path("create/result/start/<slug:slug>/", views.result_start_view, name="result-start"),
    path("create/result/<slug:slug>/", views.create_result, name="create-result"),
    path("edit/result/<slug:slug>/", views.edit_results, name="edit-results"),
    # path("result/generate/pdf/<slug:slug>/", views.result_pdf_view, name="result-pdf"), 
    path("course/<str:slug>/score/upload/", views.course_score_upload, name="course_upload_score"),
    path("course/score/download/", views.download_csv_file, name="course_score_file")
]