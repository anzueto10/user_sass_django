from django.contrib import admin
from .models import Notification, NotificationStatus


admin.site.register(Notification)
admin.site.register(NotificationStatus)
