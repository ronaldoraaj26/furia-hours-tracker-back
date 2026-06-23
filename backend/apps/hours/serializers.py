from rest_framework import serializers

from apps.users.serializers import UserSerializer
from .models import Approval, CalendarEvent, Category, FileAttachment, Project, TimeEntry, TimeEntryParticipant


class ProjectSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'active', 'created_by', 'created_by_id']

    def create(self, validated_data):
        created_by_id = validated_data.pop('created_by_id', None)
        return Project.objects.create(created_by_id=created_by_id, **validated_data)

    def update(self, instance, validated_data):
        created_by_id = validated_data.pop('created_by_id', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if created_by_id is not None:
            instance.created_by_id = created_by_id
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'max_hours', 'academic_validation']


class TimeEntryParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEntryParticipant
        fields = ['id', 'time_entry', 'name', 'ra', 'participated_at']
        read_only_fields = ['time_entry']


class FileAttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = FileAttachment
        fields = ['id', 'time_entry', 'file_name', 'file_path', 'file_type', 'uploaded_at', 'file', 'file_url']
        read_only_fields = ['file_name', 'file_path', 'file_type', 'uploaded_at', 'file_url']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url if obj.file else None


class ApprovalSerializer(serializers.ModelSerializer):
    approver = UserSerializer(read_only=True)
    approver_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Approval
        fields = ['id', 'time_entry', 'approver', 'approver_id', 'status', 'approved_at', 'comments']

    def create(self, validated_data):
        approver_id = validated_data.pop('approver_id', None)
        if approver_id:
            validated_data['approver_id'] = approver_id
        return super().create(validated_data)


class TimeEntrySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    project_id = serializers.UUIDField(write_only=True)
    category_id = serializers.UUIDField(write_only=True)
    participants = TimeEntryParticipantSerializer(many=True, required=False)
    attachments = FileAttachmentSerializer(many=True, read_only=True)
    approvals = ApprovalSerializer(many=True, read_only=True)

    class Meta:
        model = TimeEntry
        fields = [
            'id', 'user', 'project', 'category', 'project_id', 'category_id', 'work_date',
            'start_time', 'end_time', 'hours_worked', 'description', 'approved',
            'created_at', 'updated_at', 'participants', 'attachments', 'approvals',
        ]
        read_only_fields = ['approved', 'created_at', 'updated_at']

    def create(self, validated_data):
        project_id = validated_data.pop('project_id')
        category_id = validated_data.pop('category_id')
        participants_data = validated_data.pop('participants', [])
        user = self.context['request'].user
        instance = TimeEntry.objects.create(
            user=user,
            project_id=project_id,
            category_id=category_id,
            **validated_data,
        )
        for participant in participants_data:
            TimeEntryParticipant.objects.create(time_entry=instance, **participant)
        return instance

    def update(self, instance, validated_data):
        validated_data.pop('participants', None)
        project_id = validated_data.pop('project_id', None)
        category_id = validated_data.pop('category_id', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if project_id:
            instance.project_id = project_id
        if category_id:
            instance.category_id = category_id
        instance.save()
        return instance


class CalendarEventSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    project_id = serializers.UUIDField(write_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = CalendarEvent
        fields = ['id', 'project', 'project_id', 'title', 'event_date', 'event_time', 'description', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        project_id = validated_data.pop('project_id')
        return CalendarEvent.objects.create(project_id=project_id, created_by=self.context['request'].user, **validated_data)
