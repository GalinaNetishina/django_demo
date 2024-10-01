from django.conf.urls.static import static
from django.urls import path

from measurement.views import ListCreateView, SensorUpdateView, MeasurementCreateView
from smart_home import settings

urlpatterns = [
    path("sensors/", ListCreateView.as_view()),
    path("sensors/<pk>/", SensorUpdateView.as_view()),
    path("measurements/", MeasurementCreateView.as_view()),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
