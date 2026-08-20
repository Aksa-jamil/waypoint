from django.contrib import admin
from django.urls import path

from waypoint_core.views import home, report, search, catalog


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("report/", report, name="report"),
    path("search/", search, name="search"),
    path("catalog/", catalog, name="catalog"),
]