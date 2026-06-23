from rest_framework.permissions import BasePermission

from .models import RolePermission


def user_has_permission(user, permission_name: str) -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    role_id = getattr(user, 'role_id', None)
    if not role_id:
        return False
    return RolePermission.objects.filter(role_id=role_id, permission__name=permission_name).exists()


class RequiresPermission(BasePermission):
    def has_permission(self, request, view):
        required = getattr(view, 'required_permissions', [])
        if not required:
            return True
        return all(user_has_permission(request.user, permission_name) for permission_name in required)
