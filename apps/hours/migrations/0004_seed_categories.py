import uuid

from django.db import migrations


CATEGORIES = [
    ('Treino', 'Horas de treino e preparação', 80, True),
    ('Campeonato', 'Participação em campeonatos e eventos', 100, True),
    ('Organização', 'Apoio administrativo e organização', 60, True),
    ('Representação', 'Representação institucional', 40, True),
]


def seed_categories(apps, schema_editor):
    Category = apps.get_model('hours', 'Category')

    for name, description, max_hours, academic_validation in CATEGORIES:
        Category.objects.update_or_create(
            name=name,
            defaults={
                'id': uuid.uuid5(uuid.NAMESPACE_URL, f'furia-hours-category:{name}'),
                'description': description,
                'max_hours': max_hours,
                'academic_validation': academic_validation,
            },
        )


def unseed_categories(apps, schema_editor):
    Category = apps.get_model('hours', 'Category')
    Category.objects.filter(name__in=[name for name, _, _, _ in CATEGORIES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('hours', '0003_seed_projects'),
    ]

    operations = [
        migrations.RunPython(seed_categories, reverse_code=unseed_categories),
    ]
