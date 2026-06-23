from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from apps.common.models import TimestampedModel, UUIDPrimaryKeyModel
from apps.users.models import User


class Project(UUIDPrimaryKeyModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_projects')

    class Meta:
        db_table = 'projects'
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(UUIDPrimaryKeyModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    max_hours = models.DecimalField(max_digits=8, decimal_places=2)
    academic_validation = models.BooleanField(default=True)

    class Meta:
        db_table = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class TimeEntry(UUIDPrimaryKeyModel, TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='time_entries')
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='time_entries')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='time_entries')
    work_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    hours_worked = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'time_entries'
        ordering = ['-work_date', '-created_at']

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('O horário final deve ser maior que o inicial.')
        if self.hours_worked <= Decimal('0'):
            raise ValidationError('As horas devem ser maiores que zero.')
        if self.category and self.hours_worked > self.category.max_hours:
            raise ValidationError('As horas excedem o limite da categoria.')

    def __str__(self):
        return f'{self.user} - {self.work_date} - {self.hours_worked}h'


class TimeEntryParticipant(UUIDPrimaryKeyModel):
    time_entry = models.ForeignKey(TimeEntry, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=255)
    ra = models.CharField(max_length=50)
    participated_at = models.DateTimeField()

    class Meta:
        db_table = 'time_entry_participants'
        ordering = ['participated_at', 'name']

    def __str__(self):
        return self.name


class Approval(UUIDPrimaryKeyModel):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendente'),
        (STATUS_APPROVED, 'Aprovado'),
        (STATUS_REJECTED, 'Rejeitado'),
    ]

    time_entry = models.ForeignKey(TimeEntry, on_delete=models.CASCADE, related_name='approvals')
    approver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approvals_made')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    approved_at = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        db_table = 'approvals'
        ordering = ['-approved_at']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        approved = self.status == self.STATUS_APPROVED
        TimeEntry.objects.filter(pk=self.time_entry_id).update(approved=approved)


class FileAttachment(UUIDPrimaryKeyModel):
    time_entry = models.ForeignKey(TimeEntry, on_delete=models.CASCADE, related_name='attachments')
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    file_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='attachments/%Y/%m/%d/')

    class Meta:
        db_table = 'file_attachments'
        ordering = ['-uploaded_at']

    def save(self, *args, **kwargs):
        if self.file:
            self.file_name = self.file.name.split('/')[-1]
            self.file_path = self.file.name
            self.file_type = getattr(self.file.file, 'content_type', self.file_type or '') if hasattr(self.file, 'file') else self.file_type
        super().save(*args, **kwargs)
        if self.file:
            self.file_path = self.file.name
            super().save(update_fields=['file_name', 'file_path', 'file_type'])


class CalendarEvent(UUIDPrimaryKeyModel, TimestampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='calendar_events')
    title = models.CharField(max_length=255)
    event_date = models.DateField()
    event_time = models.TimeField()
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='calendar_events')

    class Meta:
        db_table = 'calendar_events'
        ordering = ['event_date', 'event_time']

    def __str__(self):
        return self.title
