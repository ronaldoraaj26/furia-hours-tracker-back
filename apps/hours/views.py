from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.access.permissions import RequiresPermission
from .models import Approval, CalendarEvent, Category, FileAttachment, Project, TimeEntry, TimeEntryParticipant
from .serializers import (
    ApprovalSerializer,
    CalendarEventSerializer,
    CategorySerializer,
    FileAttachmentSerializer,
    ProjectCreateSerializer,
    ProjectSerializer,
    TimeEntryParticipantSerializer,
    TimeEntrySerializer,
    TimeEntryWriteSerializer,
)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.select_related('created_by').all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'active']

    def get_serializer_class(self):
        if self.action in {'create', 'update', 'partial_update'}:
            return ProjectCreateSerializer
        return ProjectSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'max_hours', 'academic_validation']


class TimeEntryViewSet(ModelViewSet):
    queryset = TimeEntry.objects.select_related('user', 'project', 'category').all()
    serializer_class = TimeEntrySerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['description', 'project__name', 'category__name', 'user__email', 'user__name']
    ordering_fields = ['work_date', 'created_at', 'hours_worked', 'approved']

    def get_serializer_class(self):
        if self.action in {'create', 'update', 'partial_update'}:
            return TimeEntryWriteSerializer
        return TimeEntrySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TimeEntryParticipantViewSet(ModelViewSet):
    queryset = TimeEntryParticipant.objects.select_related('time_entry').all()
    serializer_class = TimeEntryParticipantSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'ra', 'time_entry__description']
    ordering_fields = ['participated_at', 'name']


class ApprovalViewSet(ModelViewSet):
    queryset = Approval.objects.select_related('time_entry', 'time_entry__project', 'approver').all()
    serializer_class = ApprovalSerializer
    permission_classes = [IsAuthenticated, RequiresPermission]
    required_permissions = ['approve_time_entries']
    search_fields = ['status', 'comments', 'time_entry__description', 'approver__email', 'approver__name']
    ordering_fields = ['approved_at', 'status']

    def perform_create(self, serializer):
        approved_at = serializer.validated_data.get('approved_at')
        if not approved_at and serializer.validated_data.get('status') != Approval.STATUS_PENDING:
            approved_at = timezone.now()
        serializer.save(approver=self.request.user, approved_at=approved_at)

    def perform_update(self, serializer):
        status = serializer.validated_data.get('status', serializer.instance.status)
        approved_at = serializer.validated_data.get('approved_at', serializer.instance.approved_at)
        if status == Approval.STATUS_PENDING:
            approved_at = None
        elif not approved_at:
            approved_at = timezone.now()
        serializer.save(approved_at=approved_at)


class FileAttachmentViewSet(ModelViewSet):
    queryset = FileAttachment.objects.select_related('time_entry').all()
    serializer_class = FileAttachmentSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['file_name', 'file_type', 'time_entry__description']
    ordering_fields = ['uploaded_at', 'file_name', 'file_type']


class CalendarEventViewSet(ModelViewSet):
    queryset = CalendarEvent.objects.select_related('project', 'created_by').all()
    serializer_class = CalendarEventSerializer
    permission_classes = [IsAuthenticated]
    required_permissions = ['manage_calendar_events']
    search_fields = ['title', 'description', 'project__name']
    ordering_fields = ['event_date', 'event_time', 'created_at']

    def get_permissions(self):
        if self.action in {'create', 'update', 'partial_update', 'destroy'}:
            return [IsAuthenticated(), RequiresPermission()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
