from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.access.views import AuthViewSet, PermissionViewSet, RolePermissionViewSet, TokenViewSet
from apps.audit.views import AuditLogViewSet
from apps.hours.views import (
    ApprovalViewSet,
    CalendarEventViewSet,
    CategoryViewSet,
    FileAttachmentViewSet,
    ProjectViewSet,
    TimeEntryParticipantViewSet,
    TimeEntryViewSet,
)
from apps.users.views import RoleViewSet, UserViewSet

router = DefaultRouter()
router.register('auth', AuthViewSet, basename='auth')
router.register('users', UserViewSet, basename='users')
router.register('roles', RoleViewSet, basename='roles')
router.register('permissions', PermissionViewSet, basename='permissions')
router.register('role-permissions', RolePermissionViewSet, basename='role-permissions')
router.register('tokens', TokenViewSet, basename='tokens')
router.register('projects', ProjectViewSet, basename='projects')
router.register('categories', CategoryViewSet, basename='categories')
router.register('time-entries', TimeEntryViewSet, basename='time-entries')
router.register('participants', TimeEntryParticipantViewSet, basename='participants')
router.register('approvals', ApprovalViewSet, basename='approvals')
router.register('file-attachments', FileAttachmentViewSet, basename='file-attachments')
router.register('calendar-events', CalendarEventViewSet, basename='calendar-events')
router.register('audit-logs', AuditLogViewSet, basename='audit-logs')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
