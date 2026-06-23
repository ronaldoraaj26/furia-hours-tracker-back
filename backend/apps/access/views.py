from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

from apps.users.serializers import UserSerializer
from .models import Permission, RolePermission, Token
from .permissions import RequiresPermission
from .serializers import PermissionSerializer, RolePermissionSerializer, TokenSerializer


class AuthViewSet(GenericViewSet):
    queryset = Token.objects.none()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='login')
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'detail': 'E-mail e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({'detail': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
        token = Token.issue_for_user(user)
        return Response({
            'token': token.token,
            'expires_at': token.expires_at,
            'user': UserSerializer(user).data,
        })

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated], url_path='logout')
    def logout(self, request):
        auth = request.auth
        if auth:
            auth.revoked = True
            auth.save(update_fields=['revoked'])
        return Response({'detail': 'Logout realizado com sucesso.'})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='me')
    def me(self, request):
        return Response(UserSerializer(request.user).data)


class TokenViewSet(ReadOnlyModelViewSet):
    queryset = Token.objects.select_related('user').all()
    serializer_class = TokenSerializer
    permission_classes = [IsAuthenticated, RequiresPermission]
    required_permissions = ['manage_tokens']
    search_fields = ['user__email', 'user__name', 'token']
    ordering_fields = ['issued_at', 'expires_at']


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, RequiresPermission]
    required_permissions = ['manage_permissions']
    search_fields = ['name', 'description']
    ordering_fields = ['name']


class RolePermissionViewSet(ModelViewSet):
    queryset = RolePermission.objects.select_related('role', 'permission').all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated, RequiresPermission]
    required_permissions = ['manage_permissions']
