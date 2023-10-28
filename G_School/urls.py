from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib.messages.context_processors import messages

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('GSchoolApp.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)