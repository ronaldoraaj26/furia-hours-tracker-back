from django.db import models
from django.utils import timezone

from apps.common.models import UUIDPrimaryKeyModel
from apps.users.models import User


class AuditLog(UUIDPrimaryKeyModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='audit_logs')
    action = models.CharField(max_length=50)
    entity = models.CharField(max_length=100)
    entity_id = models.UUIDField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    details = models.TextField(blank=True)

    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.action} - {self.entity}'
