from django.contrib import admin
from django.contrib.auth.models import Group


admin.site.unregister(Group)


class ManagerAccessMixin:
    def has_module_permission(self, request):
        return request.user.has_perm(
            "users.is_manager"
        ) or super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        return request.user.has_perm("users.is_manager") or super().has_view_permission(
            request, obj
        )

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm(
            "users.is_manager"
        ) or super().has_change_permission(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.has_perm("users.is_manager"):
            return qs
        return qs.filter(pk=request.user.pk)


admin.site.register(Group)
