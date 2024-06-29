from .models import User
from .errors import UsedMailError, UsedUserNameError


def is_email_used(email):
    try:
        if User.objects.filter(email=email).exists():
            raise UsedMailError()
    except UsedMailError as e:
        raise e


def is_username_used(username):
    try:
        if User.objects.filter(username=username).exists():
            raise UsedUserNameError()
    except UsedUserNameError as e:
        raise e
