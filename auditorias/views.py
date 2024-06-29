from django.shortcuts import render
from .decorators import jefe_auditoria_required
from .models import Auditoria
from .errors import (
    InvalidAuditoriaAuditoresError,
    InvalidAuditoriaCompanyError,
    InvalidAuditoriaDescriptionError,
    InvalidAuditoriaTitleError,
    InvalidAuditoriaSupervisoresError,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


def auditorias_asignadas(req):
    if req.method == "GET":
        return auditorias_asignadas_page(req)
    elif req.method == "POST":
        return create_auditoria()


@login_required
@jefe_auditoria_required
def create_auditoria(req):
    try:
        title = req.POST.get("auditoria_title")
        if not title:
            raise InvalidAuditoriaTitleError()

        description = req.POST.get("auditoria_description")
        if not description:
            raise InvalidAuditoriaDescriptionError()

        company = req.POST.get("auditoria_company")
        if not company:
            raise InvalidAuditoriaCompanyError()

        auditores_asignados_usernames = req.POST.get("auditores_asignados")
        if not auditores_asignados_usernames:
            raise InvalidAuditoriaAuditoresError

        supervisores_asignados_usernames = req.POST.get("supervisores_asignados")
        if not supervisores_asignados_usernames:
            raise InvalidAuditoriaSupervisoresError()

        auditores_asignados = User.objects.filter(
            username__in=auditores_asignados_usernames
        )
        if not auditores_asignados:
            raise InvalidAuditoriaSupervisoresError()

        supervisores_asignados = User.objects.filter(
            username__in=supervisores_asignados_usernames
        )
        if not supervisores_asignados:
            raise InvalidAuditoriaAuditoresError()

        auditoria = Auditoria.objects.create(
            title=title, description=description, company=company
        )

        auditoria.save()

        for auditor in auditores_asignados:
            auditor.auditorias_asignadas.add(auditoria)
            auditor.save()

        for supervisor in supervisores_asignados:
            supervisor.auditorias_asignadas.add(auditoria)
            supervisor.save()

        req.user.auditorias_asignadas.add(auditoria)
        req.user.save()
    except Exception as e:
        if isinstance(e, InvalidAuditoriaTitleError):
            pass
        elif isinstance(e, InvalidAuditoriaDescriptionError):
            pass
        elif isinstance(e, InvalidAuditoriaCompanyError):
            pass
        elif isinstance(e, InvalidAuditoriaAuditoresError):
            pass
        elif isinstance(e, InvalidAuditoriaSupervisoresError):
            pass
        else:
            raise e

    return


@login_required
def auditorias_asignadas_page(req):
    auditorias = req.user.auditorias_asignadas.all()
    data = {"auditorias_asignadas": auditorias}
    return render(req, "auditorias/auditorias.html", data)


@login_required
@jefe_auditoria_required
def gestionar_auditores_page(req):
    return render(req, "auditorias/gestionarAuditores.html", {})
