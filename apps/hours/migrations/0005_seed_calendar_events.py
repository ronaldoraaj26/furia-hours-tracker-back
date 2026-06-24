import uuid
from datetime import datetime, timedelta

from django.db import migrations
from django.utils import timezone


def seed_calendar_events(apps, schema_editor):
    CalendarEvent = apps.get_model('hours', 'CalendarEvent')
    Project = apps.get_model('hours', 'Project')

    if CalendarEvent.objects.exists():
        return

    today = timezone.localdate()
    seeds = [
        ('League of Legends', 'Treino semanal da equipe', today + timedelta(days=1), datetime.strptime('19:00', '%H:%M').time(), 'Treino tático e revisão de rotações.'),
        ('Valorant', 'Review de VOD', today + timedelta(days=2), datetime.strptime('20:00', '%H:%M').time(), 'Análise de partidas recentes e ajustes de estratégia.'),
        ('CS2', 'Scrim interno', today + timedelta(days=3), datetime.strptime('18:30', '%H:%M').time(), 'Sessão de treino com foco em comunicação e execução.'),
    ]

    for project_name, title, event_date, event_time, description in seeds:
        project = Project.objects.filter(name=project_name).first()
        if not project:
            continue
        CalendarEvent.objects.update_or_create(
            id=uuid.uuid5(uuid.NAMESPACE_URL, f'furia-hours-calendar-event:{title}'),
            defaults={
                'project': project,
                'title': title,
                'event_date': event_date,
                'event_time': event_time,
                'description': description,
                'created_by_id': None,
            },
        )


def unseed_calendar_events(apps, schema_editor):
    CalendarEvent = apps.get_model('hours', 'CalendarEvent')
    CalendarEvent.objects.filter(
        title__in=[
            'Treino semanal da equipe',
            'Review de VOD',
            'Scrim interno',
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('hours', '0004_seed_categories'),
    ]

    operations = [
        migrations.RunPython(seed_calendar_events, reverse_code=unseed_calendar_events),
    ]
