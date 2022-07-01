"""
Serializers for personel APIs
"""
from rest_framework import serializers

from core.models import Personel


class PersonelSerializer(serializers.ModelSerializer):
    """Serializer for personels."""

    class Meta:
        model = Personel
        fields = ['id', 'full_name', 'department', 'position', 'user']
        read_only_fields = ['id']

