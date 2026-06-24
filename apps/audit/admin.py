from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'entity', 'user', 'timestamp')
    search_fields = ('entity', 'action', 'details', 'user__email')
