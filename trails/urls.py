from django.urls import path

from waypoint_core.views import catalog


urlpatterns = [
    path("", catalog, name="catalog"),
]