from django.contrib.auth.models import AbstractUser
from django.db import models
from .const import ROLE_CHOICES
from auditorias.models import Auditoria
import uuid


class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    auditorias_asignadas = models.ManyToManyField(
        Auditoria, related_name="auditorias_asignadas", blank=True
    )

    signature = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    role = models.CharField(choices=ROLE_CHOICES, default="auditor", max_length=20)

    def __str__(self) -> str:
        return f"{self.username} - {self.role}"

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
