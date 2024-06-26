from django.contrib.auth.models import AbstractUser
from django.db import models
from .const import ROLE_CHOICES
import uuid


class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    """auditorias_asignadas = models.ManyToManyField(
        Auditoria, related_name="auditorias_asignadas", blank=True
    )"""

    signature = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    auditorias_asignadas = [
        {
            "title": "Auditoría de Estados Financieros 2023",
            "description": "Revisión completa de los estados financieros de la empresa, incluyendo balance general, estado de resultados y flujo de efectivo.",
            "company": "ABC Corp",
            "start_date": "2024-02-01",
            "end_date": "2024-03-31",
        },
        {
            "title": "Cumplimiento de Regulaciones Ambientales",
            "description": "Verificación de que todas las operaciones de la empresa cumplen con las normativas ambientales locales e internacionales.",
            "company": "Green Earth Ltd.",
            "start_date": "2024-01-15",
            "end_date": "2024-02-28",
        },
        {
            "title": "Auditoría de Seguridad Informática",
            "description": "Revisión de los sistemas de seguridad informática de la empresa para identificar vulnerabilidades y mejorar la protección de datos.",
            "company": "Tech Solutions Inc.",
            "start_date": "2024-04-10",
            "end_date": "2024-05-30",
        },
        {
            "title": "Auditoría de Procesos de Producción",
            "description": "Evaluación de los procesos de producción para mejorar la eficiencia y reducir costos operativos.",
            "company": "Manufacturing Co.",
            "start_date": "2024-03-01",
            "end_date": "2024-04-15",
        },
        {
            "title": "Auditoría de Cumplimiento Legal",
            "description": "Examen del cumplimiento de la empresa con las leyes y regulaciones locales e internacionales aplicables.",
            "company": "Legal Services Ltd.",
            "start_date": "2024-06-01",
            "end_date": "2024-07-15",
        },
        {
            "title": "Auditoría de Recursos Humanos",
            "description": "Revisión de las prácticas de recursos humanos para asegurar el cumplimiento de políticas y procedimientos.",
            "company": "HR Solutions LLC",
            "start_date": "2024-05-10",
            "end_date": "2024-06-30",
        },
    ]

    role = models.CharField(choices=ROLE_CHOICES, default="auditor", max_length=20)
