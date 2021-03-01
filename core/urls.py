from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("books/", include("books.urls")),
    path("quiz/", include("quiz.urls")),
    path("search/", include("search_test.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
