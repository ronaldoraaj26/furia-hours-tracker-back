from rest_framework import serializers

from .models import Approval, CalendarEvent, Category, FileAttachment, Project, TimeEntry, TimeEntryParticipant


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'max_hours',
            'academic_validation',
        ]


class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'active',
            'created_by',
        ]


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'active',
        ]
        extra_kwargs = {
            'description': {'required': False, 'allow_blank': True},
        }


class ProjectForEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'name',
        ]


class CalendarEventSerializer(serializers.ModelSerializer):
    project_id = serializers.PrimaryKeyRelatedField(
        source='project',
        queryset=Project.objects.all(),
        write_only=True,
    )
    project = ProjectForEventSerializer(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    event_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])
    event_time = serializers.TimeField(
        format='%H:%M:%S',
        input_formats=['%H:%M', '%H:%M:%S'],
    )

    class Meta:
        model = CalendarEvent
        fields = [
            'id',
            'title',
            'event_date',
            'event_time',
            'project_id',
            'project',
            'description',
            'created_by',
            'created_at',
            'updated_at',
        ]


class TimeEntryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEntry
        fields = [
            'project',
            'category',
            'work_date',
            'start_time',
            'end_time',
            'hours_worked',
            'description',
        ]
        extra_kwargs = {
            'description': {'required': False, 'allow_blank': True},
        }


class TimeEntrySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    project = ProjectForEventSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = TimeEntry
        fields = [
            'id',
            'user',
            'project',
            'category',
            'work_date',
            'start_time',
            'end_time',
            'hours_worked',
            'description',
            'approved',
            'created_at',
            'updated_at',
        ]


class TimeEntryParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEntryParticipant
        fields = [
            'id',
            'time_entry',
            'name',
            'ra',
            'participated_at',
        ]


class FileAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileAttachment
        fields = [
            'id',
            'time_entry',
            'file_name',
            'file_path',
            'file_type',
            'uploaded_at',
            'file',
        ]
        read_only_fields = [
            'file_name',
            'file_path',
            'file_type',
            'uploaded_at',
        ]


class ApprovalSerializer(serializers.ModelSerializer):
    approver = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Approval
        fields = [
            'id',
            'time_entry',
            'approver',
            'status',
            'approved_at',
            'comments',
        ]
        read_only_fields = ['approved_at']
