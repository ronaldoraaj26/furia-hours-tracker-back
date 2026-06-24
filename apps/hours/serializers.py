from rest_framework import serializers
from .models import CalendarEvent, Project, Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer para categorias.
    """

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer completo para projetos.
    """

    category = CategorySerializer(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'category',
        ]


class ProjectCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação/edição de projetos.
    Recebe o ID da categoria.
    """

    class Meta:
        model = Project
        fields = [
            'name',
            'category',
        ]


class ProjectForEventSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para exibir projeto dentro do evento.
    """

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
        ]


class CalendarEventSerializer(serializers.ModelSerializer):
    """
    Serializer para leitura de eventos.
    Retorna o projeto aninhado.
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
    Serializer para criação/edição de eventos.
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
            'description': {
                'required': False,
                'allow_blank': True,
            },
        }


class ApprovalSerializer(serializers.Serializer):
    """
    Serializer para aprovar/reprovar eventos ou horas.
    """

    approved = serializers.BooleanField(required=True)
    observation = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )