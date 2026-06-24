from django.core.management.base import BaseCommand

from apps.access.models import Permission, RolePermission
from apps.hours.models import Category, Project
from apps.users.models import Role, User


class Command(BaseCommand):
    help = 'Popula dados iniciais do sistema.'

    def handle(self, *args, **options):
        permissions = [
            ('manage_users', 'Gerenciar usuários'),
            ('manage_roles', 'Gerenciar papéis'),
            ('manage_permissions', 'Gerenciar permissões'),
            ('manage_tokens', 'Visualizar tokens'),
            ('approve_time_entries', 'Aprovar registros de horas'),
            ('manage_calendar_events', 'Gerenciar eventos do calendário'),
            ('view_audit_logs', 'Visualizar auditoria'),
        ]
        for name, description in permissions:
            Permission.objects.get_or_create(name=name, defaults={'description': description})

        admin_role, _ = Role.objects.get_or_create(name='Admin', defaults={'description': 'Administrador do sistema'})
        director_role, _ = Role.objects.get_or_create(name='Diretoria', defaults={'description': 'Diretoria da atlética'})
        member_role, _ = Role.objects.get_or_create(name='Membro', defaults={'description': 'Membro comum'})

        for permission in Permission.objects.all():
            RolePermission.objects.get_or_create(role=admin_role, permission=permission)

        for perm_name in ['approve_time_entries', 'manage_calendar_events', 'view_audit_logs']:
            permission = Permission.objects.get(name=perm_name)
            RolePermission.objects.get_or_create(role=director_role, permission=permission)

        categories = [
            ('Treino', 'Horas de treino e preparação', 80, True),
            ('Campeonato', 'Participação em campeonatos e eventos', 100, True),
            ('Organização', 'Apoio administrativo e organização', 60, True),
            ('Representação', 'Representação institucional', 40, True),
        ]
        for name, description, max_hours, academic_validation in categories:
            Category.objects.get_or_create(
                name=name,
                defaults={
                    'description': description,
                    'max_hours': max_hours,
                    'academic_validation': academic_validation,
                },
            )

        modalities = [
            'League of Legends', 'Valorant', 'Wild Rift', 'TFT',
            'CS2', 'Rocket League', 'Free Fire', 'EA FC',
        ]
        creator = User.objects.filter(is_superuser=True).first()
        for modality in modalities:
            Project.objects.get_or_create(
                name=modality,
                defaults={
                    'description': f'Modalidade {modality}',
                    'active': True,
                    'created_by': creator,
                },
            )

        self.stdout.write(self.style.SUCCESS('Dados iniciais criados com sucesso.'))
