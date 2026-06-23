from django.contrib import admin

from .models import Approval, CalendarEvent, Category, FileAttachment, Project, TimeEntry, TimeEntryParticipant


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'created_by')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_hours', 'academic_validation')
    search_fields = ('name',)


class TimeEntryParticipantInline(admin.TabularInline):
    model = TimeEntryParticipant
    extra = 0


class FileAttachmentInline(admin.TabularInline):
    model = FileAttachment
    extra = 0


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'category', 'work_date', 'hours_worked', 'approved')
    search_fields = ('user__email', 'description', 'project__name')
    list_filter = ('approved', 'project', 'category')
    inlines = [TimeEntryParticipantInline, FileAttachmentInline]


@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = ('time_entry', 'approver', 'status', 'approved_at')
    list_filter = ('status',)


@admin.register(FileAttachment)
class FileAttachmentAdmin(admin.ModelAdmin):
    list_display = ('time_entry', 'file_name', 'file_type', 'uploaded_at')


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'event_date', 'event_time', 'created_by')
    search_fields = ('title', 'project__name')
