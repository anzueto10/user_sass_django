from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Role", {"fields": ("role",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "email",
                    "is_active",
                    "is_staff",
                    "role",
                ),
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "role",
        "display_auditorias_asignadas",
    )
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)

    def display_auditorias_asignadas(self, obj):
        auditorias = obj.auditorias_asignadas.all()
        if auditorias:
            return "\n".join([f"{a['title']} - {a['company']}" for a in auditorias])
        else:
            return "No hay auditorias asignadas."

    display_auditorias_asignadas.short_description = "Auditorias Asignadas"


admin.site.register(User, CustomUserAdmin)
