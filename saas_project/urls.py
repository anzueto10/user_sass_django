from django.contrib import admin
from django.urls import path, include
from notifications import urls as notifications_urls
from users import urls as users_urls

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("", include(users_urls)),
    path("notifications/", include(notifications_urls)),
]
