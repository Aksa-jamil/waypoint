from django.urls import path

from waypoint_core.views import catalog, trail_detail


urlpatterns = [
    path("", catalog, name="catalog"),
    path("<int:trail_id>/", trail_detail, name="trail-detail"),
]