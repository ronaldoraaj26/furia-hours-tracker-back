import secrets
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.common.models import UUIDPrimaryKeyModel
from apps.users.models import Role, User


class Token(UUIDPrimaryKeyModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    token = models.TextField(unique=True)
    issued_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    revoked = models.BooleanField(default=False)

    class Meta:
        db_table = 'tokens'
        ordering = ['-issued_at']

    @classmethod
    def issue_for_user(cls, user):
        now = timezone.now()
        token = secrets.token_urlsafe(32)
        return cls.objects.create(
            user=user,
            token=token,
            issued_at=now,
            expires_at=now + timedelta(hours=getattr(settings, 'TOKEN_EXPIRATION_HOURS', 12)),
        )

    @property
    def is_valid(self):
        return not self.revoked and self.expires_at > timezone.now()


class Permission(UUIDPrimaryKeyModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'permissions'
        ordering = ['name']

    def __str__(self):
        return self.name


class RolePermission(UUIDPrimaryKeyModel):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='permission_roles')

    class Meta:
        db_table = 'role_permissions'
        unique_together = ('role', 'permission')

    def __str__(self):
        return f'{self.role} -> {self.permission}'
