from django.contrib import admin

from .models import Permission, RolePermission, Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'issued_at', 'expires_at', 'revoked')
    search_fields = ('user__email', 'token')


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission')
    search_fields = ('role__name', 'permission__name')
