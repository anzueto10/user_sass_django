from django.urls import path
from . import views

urlpatterns = [
    path("", views.auditorias_asignadas, name="auditorias_asignadas"),
    path(
        "gestionar_auditores/",
        views.gestionar_auditores_page,
        name="gestionar_auditores",
    ),
]
