from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("", include("users.urls")),
]
