from django.urls import path
from . import views


urlpatterns = [
    path("subjects/list/", views.subject_list, name="subject-list"),
    path("subject/create/", views.create_subject, name="subject-create"),

    # upload list of subjects
    path("subjects/upload/list/", views.subject_bulk_upload_view, name="subject-upload"), 
    path("subject/donwload/csv/", views.subject_csv_download_view, name="subject-download-csv")
]