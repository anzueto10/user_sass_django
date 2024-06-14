from django.urls import path
from users import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("user/", views.user, name="user"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("app1/", views.example, name="app1"),
    path("app2/", views.example, name="app2"),
    path("app3/", views.example, name="app3"),
    path("app4/", views.example, name="app4"),
    path("app5/", views.example, name="app5"),
]
