from django import forms
from .models import Notification


class NotificationAdminForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ["notifier", "notified_users", "note", "auditoria"]
