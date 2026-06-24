import uuid

from django.db import migrations


PROJECTS = [
    ('League of Legends', 'Modalidade League of Legends'),
    ('Valorant', 'Modalidade Valorant'),
    ('Wild Rift', 'Modalidade Wild Rift'),
    ('TFT', 'Modalidade TFT'),
    ('CS2', 'Modalidade CS2'),
    ('Rocket League', 'Modalidade Rocket League'),
    ('Free Fire', 'Modalidade Free Fire'),
    ('EA FC', 'Modalidade EA FC'),
]


def seed_projects(apps, schema_editor):
    Project = apps.get_model('hours', 'Project')

    for name, description in PROJECTS:
        Project.objects.update_or_create(
            name=name,
            defaults={
                'id': uuid.uuid5(uuid.NAMESPACE_URL, f'furia-hours-project:{name}'),
                'description': description,
                'active': True,
                'created_by_id': None,
            },
        )


def unseed_projects(apps, schema_editor):
    Project = apps.get_model('hours', 'Project')
    Project.objects.filter(name__in=[name for name, _ in PROJECTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('hours', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(seed_projects, reverse_code=unseed_projects),
    ]
