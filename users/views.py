from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout as logout_func
from django.contrib.auth import login as login_func
from django.contrib.auth.decorators import login_required
from .models import User
from .services import is_email_used, is_username_used
from .errors import UsedMailError, UsedUserNameError


def edit(req):
    if req.method == "GET":
        return edit_page(req)
    elif req.method == "POST":
        return edit_user(req)


def login(req):
    if req.method == "GET":
        return login_page(req)
    elif req.method == "POST":
        return login_user(req)


def signup(req):
    if req.method == "GET":
        return signup_page(req)
    elif req.method == "POST":
        return create_user(req)


# Funciones back-end
def create_user(req):
    errors = {}
    try:
        username = req.POST["username"]
        first_name = req.POST["first_name"]
        last_name = req.POST["last_name"]
        email = req.POST["email"]
        password_1 = req.POST["password_1"]
        password_2 = req.POST["password_2"]
    except KeyError:
        errors["full_error"] = "The Fields are invalid"
        return render(req, "pages/signup.html", errors)

    if username == "":
        errors["username_error"] = "The User Name cant be null"

    if first_name == "":
        errors["first_name_error"] = "The First Name cant be null"

    if last_name == "":
        errors["last_name_error"] = "The Lat Name cant be null"

    if email == "":
        errors["email_error"] = "The Email cant be null"

    if password_1 == "":
        errors["password_error"] = "The Password cant be null"

    if password_1 != password_2:
        errors["passwords_error"] = "The password do not matches"

    try:
        is_username_used(username)
        is_email_used(email)

    except UsedMailError:
        errors["email_error"] = "The email is used"

    except UsedUserNameError:
        errors["username_error"] = " The User Name is used"

    if errors:
        return render(req, "pages/signup.html", errors)

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password_1,
    )

    user.save()

    return redirect("login")


def login_user(req):
    errors = {}
    try:
        username = req.POST["username"]
        password = req.POST["password"]
    except KeyError:
        errors["full_error"] = "The Fields are invalid"
        return render(req, "pages/login.html", errors)

    if username == "":
        errors["username_error"] = "The User Name cant be null"

    if password == "":
        errors["password_error"] = "The Password cant be null"

    if errors:
        return render(req, "pages/login.html", errors)

    user = authenticate(req, username=username, password=password)

    if user != None:
        login_func(req, user)
        return redirect("user_profile")
    else:
        errors["full_error"] = "Invalid username or password"
        return render(req, "pages/login.html", errors)


@login_required
def logout(req):
    logout_func(req)
    return redirect("home")


def edit_user(req):
    error: str = ""

    field = req.POST.get("field")
    new_value = req.POST.get(field)
    username = req.POST.get("user")

    if not new_value:
        error = "The field cant be null"

    if field == "username":
        try:
            is_username_used(new_value)

        except UsedUserNameError:
            error = "The User name is alredy in use"

    if field == "email":
        try:
            is_email_used(new_value)
        except UsedMailError:
            error = "The Email is alredy in use"

    if error:
        return render(req, "pages/edit.html", {"error": error, "field": field})

    try:
        user = User.objects.get(username=username)
        setattr(user, field, new_value)
        user.save()
        return redirect("user_profile")

    except User.DoesNotExist:
        return redirect("user_profile")


# Páginas para el front
def home_page(req):
    return render(req, "pages/home.html", {})


def login_page(req):
    return render(req, "pages/login.html", {})


def signup_page(req):
    return render(req, "pages/signup.html", {})


@login_required
def user_page(req):
    return render(req, "pages/user.html", {})


@login_required
def edit_page(req):
    field = req.GET.get("field")
    if not field:
        return redirect("user_profile")

    else:
        return render(req, "pages/edit.html", {"field": field})
