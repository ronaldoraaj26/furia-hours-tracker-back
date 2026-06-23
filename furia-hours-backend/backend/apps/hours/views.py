from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.access.permissions import RequiresPermission
from .models import Approval, CalendarEvent, Category, FileAttachment, Project, TimeEntry, TimeEntryParticipant
from .serializers import (
    ApprovalSerializer,
    CalendarEventSerializer,
    CategorySerializer,
    FileAttachmentSerializer,
    ProjectSerializer,
    TimeEntryParticipantSerializer,
    TimeEntrySerializer,
)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.select_related('created_by').all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'description']
    ordering_fields = ['name']


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'max_hours']


class TimeEntryViewSet(ModelViewSet):
    serializer_class = TimeEntrySerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['description', 'project__name', 'category__name', 'user__name', 'user__email']
    ordering_fields = ['work_date', 'hours_worked', 'created_at']
    filterset_fields = ['project', 'category', 'approved', 'work_date']

    def get_queryset(self):
        queryset = TimeEntry.objects.select_related('user', 'project', 'category').prefetch_related('participants', 'attachments', 'approvals__approver')
        if self.request.query_params.get('mine') == '1':
            queryset = queryset.filter(user=self.request.user)
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        project_id = self.request.query_params.get('project_id')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class TimeEntryParticipantViewSet(ModelViewSet):
    queryset = TimeEntryParticipant.objects.select_related('time_entry').all()
    serializer_class = TimeEntryParticipantSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'ra']
    ordering_fields = ['participated_at', 'name']

    def perform_create(self, serializer):
        time_entry_id = self.request.data.get('time_entry')
        serializer.save(time_entry_id=time_entry_id)


class ApprovalViewSet(ModelViewSet):
    queryset = Approval.objects.select_related('time_entry', 'approver').all()
    serializer_class = ApprovalSerializer
    permission_classes = [IsAuthenticated, RequiresPermission]
    required_permissions = ['approve_time_entries']
    search_fields = ['time_entry__description', 'approver__name', 'comments']
    ordering_fields = ['approved_at', 'status']
    filterset_fields = ['status', 'time_entry']


class FileAttachmentViewSet(ModelViewSet):
    queryset = FileAttachment.objects.select_related('time_entry').all()
    serializer_class = FileAttachmentSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['uploaded_at']
    filterset_fields = ['time_entry']


class CalendarEventViewSet(ModelViewSet):
    queryset = CalendarEvent.objects.select_related('project', 'created_by').all()
    serializer_class = CalendarEventSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['title', 'description', 'project__name']
    ordering_fields = ['event_date', 'event_time', 'title']
    filterset_fields = ['project', 'event_date']
