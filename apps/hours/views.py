from rest_framework import serializers
from .models import CalendarEvent, Project, Category


class ProjectForEventSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para aninhar informações do projeto no evento.
    """

    class Meta:
        model = Project
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer para categorias.
    """

    class Meta:
        model = Category
        fields = ['id', 'name']


class CalendarEventSerializer(serializers.ModelSerializer):
    """
    Serializer para leitura (GET) de CalendarEvent.
    Retorna o objeto do projeto aninhado.
    """

    project = ProjectForEventSerializer(read_only=True)

    class Meta:
        model = CalendarEvent
        fields = [
            'id',
            'title',
            'event_date',
            'event_time',
            'project',
            'description',
        ]


class CalendarEventCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação (POST) de CalendarEvent.
    Recebe o ID do projeto.
    """

    class Meta:
        model = CalendarEvent
        fields = [
            'title',
            'event_date',
            'event_time',
            'project',
            'description',
        ]
        extra_kwargs = {
            'description': {'required': False, 'allow_blank': True}
        }


class ApprovalSerializer(serializers.Serializer):
    """
    Serializer usado para aprovar/reprovar algo relacionado às horas/eventos.
    """

    approved = serializers.BooleanField(required=True)
    observation = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )
