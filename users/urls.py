from django.urls import path
from users import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("user/", views.user, name="user"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("auditorias/", views.auditorias_asignadas, name="auditorias_asignadas"),
    path(
        "gestionar_auditores/",
        views.gestionar_auditores_page,
        name="gestionar_auditores",
    ),
]
