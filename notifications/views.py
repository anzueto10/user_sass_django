from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification, NotificationStatus
from .errors import (
    InvalidNoteNotificationError,
    InvalidNotifiedsNotificationError,
    NotifiedsNotificatonDoNotExitsError,
    AuditoriaNotificationDoNotExitsError,
    InvalidAuditoriaNotificationError,
)
from django.contrib.auth import get_user_model
from auditorias.models import Auditoria

User = get_user_model()


def notifications(req):
    if req.method == "GET":
        return notifications_page(req)


def create_notification(req):
    if req.method == "GET":
        return create_notification_page(req)
    elif req.method == "POST":
        return push_notification(req)


@login_required
def push_notification(req):
    notifier = req.user

    note = req.POST.get("notification_note")
    auditoria_id = req.POST.get("auditoria_id")
    notifieds_usernames = [req.POST.get("notifieds_users")]

    print(note, auditoria_id, notifieds_usernames)

    try:
        if not note:
            raise InvalidNoteNotificationError()

        if not notifieds_usernames:
            raise InvalidNotifiedsNotificationError()

        if not auditoria_id:
            raise InvalidAuditoriaNotificationError()

        try:
            auditoria_id = int(auditoria_id)
        except ValueError:
            raise InvalidAuditoriaNotificationError()

        notifieds_users = User.objects.filter(username__in=notifieds_usernames)
        auditoria = get_object_or_404(Auditoria, pk=auditoria_id)

        if not notifieds_users:
            raise NotifiedsNotificatonDoNotExitsError()

        if not auditoria:
            raise AuditoriaNotificationDoNotExitsError()

        notification = Notification.objects.create(
            notifier=notifier, note=note, auditoria=auditoria
        )

        new_notification_statuses = [
            NotificationStatus.objects.create(
                user=notified_user, notification=notification
            )
            for notified_user in notifieds_users
        ]
        # Error en la base de datos o en el servidor o similar
        if not notification or not new_notification_statuses:
            return create_notification_page(req, pushed=False)

        return create_notification_page(req, pushed=True)

    except Exception as e:
        if isinstance(e, InvalidNoteNotificationError):
            return create_notification_page(req, error={"invalid_note": e})
        elif isinstance(e, InvalidNotifiedsNotificationError):
            return create_notification_page(req, error={"invalid_notified": e})

        elif isinstance(e, NotifiedsNotificatonDoNotExitsError):
            return create_notification_page(req, error={"invalid_notified": e})

        elif isinstance(e, InvalidAuditoriaNotificationError):
            return create_notification_page(req, error={"invalid_auditoria": e})

        elif isinstance(e, AuditoriaNotificationDoNotExitsError):
            return create_notification_page(req, error={"invalid_auditoria": e})
        else:
            return create_notification_page(req, error=e)


@login_required
def mark_notification_as_read(req, notification_status_id):
    notification_status = get_object_or_404(
        NotificationStatus, pk=notification_status_id
    )
    notification_status.read_notification()
    return redirect("notifications")


@login_required
def notifications_page(req):
    user = req.user
    notifications = NotificationStatus.objects.filter(user=user).all()

    filter = req.GET.get("filter")
    if not filter or filter not in ["readed", "not_readed"]:
        data = {"notifications": notifications}
    else:
        data = {
            "notifications": notifications,
            "filter": filter,
        }
    return render(req, "notifications/notifications.html", data)


@login_required
def create_notification_page(req, **notification_status):
    notifieds = []

    auditorias_asignadas = req.user.auditorias_asignadas.all()

    if req.user.role == "jefe_auditoria":
        auditores = User.objects.filter(
            auditorias_asignadas__in=auditorias_asignadas, role="auditor"
        ).distinct()

        supervisores = User.objects.filter(
            auditorias_asignadas__in=auditorias_asignadas, role="supervisor"
        ).distinct()

        notifieds.extend(auditores)
        notifieds.extend(supervisores)

    elif req.user.role == "supervisor":
        auditores = User.objects.filter(
            auditorias_asignadas__in=auditorias_asignadas, role="auditor"
        ).distinct()

        jefes_auditoria = User.objects.filter(
            auditorias_asignadas__in=auditorias_asignadas, role="jefe_auditoria"
        ).distinct()

        notifieds.extend(auditores)
        notifieds.extend(jefes_auditoria)

    elif req.user.role == "auditor":
        supervisores = User.objects.filter(
            auditorias_asignadas__in=auditorias_asignadas, role="supervisor"
        ).distinct()

        notifieds.extend(supervisores)

    data = {"notifieds": notifieds}

    if notification_status.get("error"):
        data["errors"] = notification_status.get("error")

    if notification_status.get("pushed") == True:
        data["notification_pushed"] = "pushed"
    elif notification_status.get("pushed") == False:
        data["notification_pushed"] = "not_pushed"

    return render(req, "notifications/createNotification.html", data)
