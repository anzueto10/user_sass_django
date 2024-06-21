from django.contrib.auth.models import AbstractUser
from django.db import models
from .const import ROLE_CHOICES


class Auditoria(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    auditorias_asignadas = models.ManyToManyField(
        Auditoria, related_name="auditorias_asignadas", blank=True
    )
    role = models.CharField(choices=ROLE_CHOICES, default="auditor", max_length=20)
