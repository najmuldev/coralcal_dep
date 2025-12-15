from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('ks', include('knowledge_series.urls')),
    path('gift/', include('dr_gift_catalogs.urls')),
    path('dep/admin/', include('dep_admin.urls')),
    path('anniversary/', include('anniversary.urls')),
    path('rgc/', include('green_corner.urls')),
    path('doctors_opinion/', include('doctors_opinion.urls')),
    path('doctors_data/', include('doctors_data.urls')),
    path('dac/', include('doctors_ai_course.urls')),
    path('plant/', include('plant_module.urls')),
    path('dac2/', include('doctors_ai_course2.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)