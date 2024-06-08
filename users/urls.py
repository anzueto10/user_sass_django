from django.urls import path
from users import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    path("user/", views.user_page, name="user_profile"),
    path("edit/", views.edit, name="edit_user"),
]
