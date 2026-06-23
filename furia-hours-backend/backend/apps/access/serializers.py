from rest_framework import serializers

from apps.users.serializers import RoleSerializer, UserSerializer
from .models import Permission, RolePermission, Token


class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Token
        fields = ['id', 'user', 'token', 'issued_at', 'expires_at', 'revoked']
        read_only_fields = ['id', 'issued_at', 'expires_at']


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'description']


class RolePermissionSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    permission = PermissionSerializer(read_only=True)
    role_id = serializers.UUIDField(write_only=True)
    permission_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission', 'role_id', 'permission_id']

    def create(self, validated_data):
        return RolePermission.objects.create(
            role_id=validated_data['role_id'],
            permission_id=validated_data['permission_id'],
        )
