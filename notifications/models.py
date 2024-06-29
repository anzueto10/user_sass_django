from django.db import models
from auditorias.models import Auditoria
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Notification(models.Model):
    notifier = models.ForeignKey(
        User, related_name="notifier", on_delete=models.CASCADE
    )
    notified_users = models.ManyToManyField(
        User, through="NotificationStatus", related_name="notified_users"
    )

    created_at = models.DateTimeField(default=timezone.now)
    note = models.TextField()
    auditoria = models.ForeignKey(
        Auditoria, related_name="auditoria_notifications", on_delete=models.CASCADE
    )

    def check_and_delete_if_done(self):
        if all(notified.is_read == True for notified in self.notified_users.all()):
            self.delete()

    def __str__(self):
        return f"{self.notifier}: {self.note} - {self.created_at}"


class NotificationStatus(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    readed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.notification.note} - {"Leida" if self.is_read else "Sin leer"}"

    def read_notification(self):
        self.is_read = True
        self.readed_date = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        if (
            self.notification.notifier.role == "auditor"
            and self.user.role != "supervisor"
        ):

            raise ValueError(
                "Los Auditores únicamente pueden notificar a los Supervisores."
            )
        elif self.notification.notifier.role == "supervisor" and self.user.role not in [
            "jefe_auditoria",
            "auditor",
        ]:
            raise ValueError(
                "Los Supervisores solo pueden notificar a los Auditores o Jefes de Auditoria."
            )
        super().save(*args, **kwargs)
