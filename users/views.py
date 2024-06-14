from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout as logout_func
from django.contrib.auth import login as login_func
from django.contrib.auth.decorators import login_required
from .models import User
from .services import is_email_used, is_username_used
from .errors import UsedMailError, UsedUserNameError
from .const import routes


def user(req):
    if req.method == "GET":
        return user_page(req)
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
        return render(req, "users/signup.html", errors)

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
        return render(req, "users/signup.html", errors)

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
        return render(req, "users/login.html", errors)

    if username == "":
        errors["username_error"] = "The User Name cant be null"

    if password == "":
        errors["password_error"] = "The Password cant be null"

    if errors:
        return render(req, "users/login.html", errors)

    user = authenticate(req, username=username, password=password)

    if user != None:
        login_func(req, user)
        return redirect("user")
    else:
        errors["full_error"] = "Invalid username or password"
        return render(req, "users/login.html", errors)


@login_required
def logout(req):
    logout_func(req)
    return redirect("home")


def edit_user(req):
    error: str = ""
    id = req.POST.get("id")

    username = req.POST.get("username")
    first_name = req.POST.get("first_name")
    last_name = req.POST.get("last_name")
    email = req.POST.get("email")

    field = (
        "username"
        if username
        else "first_name" if first_name else "last_name" if last_name else "email"
    )
    value = (
        username
        if username
        else first_name if first_name else last_name if last_name else email
    )

    if username:
        try:
            is_username_used(username)
        except UsedUserNameError:
            error = "The User name is alredy in use"

    if email:
        try:
            is_email_used(email)
        except UsedMailError:
            error = "The Email is alredy in use"

    if error:
        print(error)
        return render(
            req,
            "users/user.html",
            {"routes": routes, "active": "User"},
        )

    try:
        user = User.objects.get(id=id)
        setattr(user, field, value)
        user.save()
        return redirect("user")

    except User.DoesNotExist:
        return redirect("user")


# Páginas para el front
def home_page(req):
    return render(req, "users/home.html", {"routes": routes, "active": "Home"})


def login_page(req):
    return render(req, "users/login.html", {"title": "Iniciar Seción"})


def signup_page(req):
    return render(req, "users/signup.html", {"title": "Registrarse"})


@login_required
def user_page(req):
    data = {
        "routes": routes,
        "active": "User",
    }
    return render(req, "users/user.html", data)


@login_required
def dashboard(req):
    data = {
        "routes": routes,
        "active": "Dashboard",
    }
    return render(req, "users/dashboard.html", data)


@login_required
def example(req):
    return render(
        req,
        "users/example.html",
        {"routes": routes, "active": "app1"},
    )
