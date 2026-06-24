from django.db import migrations


def seed_calendar_permission(apps, schema_editor):
    Permission = apps.get_model('access', 'Permission')
    Permission.objects.update_or_create(
        name='manage_calendar_events',
        defaults={'description': 'Gerenciar eventos do calendário'},
    )


def unseed_calendar_permission(apps, schema_editor):
    Permission = apps.get_model('access', 'Permission')
    Permission.objects.filter(name='manage_calendar_events').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(seed_calendar_permission, reverse_code=unseed_calendar_permission),
    ]
