"""
Serializers for personel APIs
"""
from rest_framework import serializers

from core.models import Personel


class PersonelSerializer(serializers.ModelSerializer):
    """Serializer for personels."""

    class Meta:
        model = Personel
        fields = ['id', 'full_name', 'user_id']
        read_only_fields = ['id']

class PersonelDetailSerializer(PersonelSerializer):
    """Serializer for personel detail view"""

    class Meta(PersonelSerializer.Meta):
        fields = PersonelSerializer.Meta.fields + ['department', 'position']