from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.urls.conf import include
from django.conf.urls.static import static

api_patterns = [
    path("auth/", include("user_profile.urls")),
    path("chat/", include("chat.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_patterns)),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
