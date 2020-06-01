from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'admin/', admin.site.urls),
    # url(r'^', include('upload.urls'), name="index"),
    url(r'upload/', include('upload.urls')),
    url(r'trends/', include('analytics.urls')),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)