from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import error_404_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path("chat/", include("chat.urls", namespace="chat")),
    path("", include("accounts.urls")),
    path("", include("departments.urls")),
    path("", include("students.urls")),
    path("", include("employees.urls")),
    path("", include("subjects.urls")), 
    path("", include("courses.urls")), 
    path("", include("tasks.urls")),
    path("", include("results.urls")),
    path("", include("assessments.urls")),
    path("", include("adminPanel.urls")),
    path("schedule/", include("schedule.urls")),
    path("actions/", include("actions.urls")),

    path("ckeditor/", include('ckeditor_uploader.urls'))

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "management_system.views.error_404_view"