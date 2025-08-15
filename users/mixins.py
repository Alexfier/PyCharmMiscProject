from messaging import admin
from users.admin import ManagerAccessMixin
from users.models import User, Profile


@admin.register(User)
class CustomUserAdmin(ManagerAccessMixin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "avatar", "phone", "country")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


@admin.register(Profile)
class ProfileAdmin(ManagerAccessMixin, admin.ModelAdmin):
    list_display = ("user", "phone", "country")
    search_fields = ("user__email", "phone")
