from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
def notifications(req):
    if req.method == "GET":
        return notifications_page(req)
    elif req.method == "POST":
        return push_notification(req)


@login_required
def push_notification(req):
    pass


@login_required
def notifications_page(req):
    data = {"active": "Notifications"}
    return render(req, "notifications/notifications.html", data)
