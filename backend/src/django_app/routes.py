# src/django_app/routes.py

from django.urls import include, path

urlpatterns = [
    path('stations/', include('modules.stations.urls')),
    path('places/', include('modules.places.urls')),
    path('records/', include('modules.records.urls')),
    path('sensors/', include('modules.sensors.urls')),
]