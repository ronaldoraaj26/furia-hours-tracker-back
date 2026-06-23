from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.access.permissions import RequiresPermission
from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogViewSet(ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related('user').all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, RequiresPermission]
    required_permissions = ['view_audit_logs']
    search_fields = ['action', 'entity', 'details', 'user__email']
    ordering_fields = ['timestamp']
