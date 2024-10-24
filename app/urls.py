from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api/auth/", include('authentication.urls')),
    path("api/users/", include('user.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from core.startup import *