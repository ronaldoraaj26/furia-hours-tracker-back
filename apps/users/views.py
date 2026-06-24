from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.access.permissions import RequiresPermission
from .models import Role, User
from .serializers import RoleSerializer, UserSerializer


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, RequiresPermission]
    required_permissions = ['manage_roles']
    search_fields = ['name', 'description']
    ordering_fields = ['name']


class UserViewSet(ModelViewSet):
    queryset = User.objects.select_related('role').all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, RequiresPermission]
    required_permissions = ['manage_users']
    search_fields = ['name', 'email', 'role__name']
    ordering_fields = ['name', 'email', 'created_at']
