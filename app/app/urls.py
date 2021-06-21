from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('website.urls')),
    path('doctor/', include('doctor.urls')),
    path('lab/', include('lab.urls')),
    path('agent/', include('agent.urls')),
    path('patient/', include('patient.urls')),
    path('admin/', include('core.urls')),
    path('admin/location/', include('location.urls')),
    path('admin/healthcare/', include('healthcare.urls')),
    path('admin/warehouse/', include('warehouse.urls')),
    path('admin/services/', include('services.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
