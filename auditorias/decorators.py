from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse


def jefe_auditoria_required(view_func):
    def check_roles(user) -> bool:
        return user.is_authenticated and (
            user.is_staff or user.role == "jefe_auditoria"
        )

    @wraps(view_func)
    def wrapper(req, *args, **kwargs):
        if check_roles(req.user):
            return view_func(req, *args, **kwargs)
        else:
            return redirect(reverse("user"))

    return wrapper
