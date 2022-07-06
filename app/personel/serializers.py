"""
Serializers for personel APIs
"""
from rest_framework import serializers

from core.models import (
    Personel,
    Area,
    SubArea,
)


class PersonelSerializer(serializers.ModelSerializer):
    """Serializer for personels."""

    class Meta:
        model = Personel
        fields = ['id', 'full_name', 'user_id']
        read_only_fields = ['id']


class PersonelDetailSerializer(PersonelSerializer):
    """Serializer for personel detail view"""

    class Meta(PersonelSerializer.Meta):
        fields = PersonelSerializer.Meta.fields + ['birthday', 'is_coordinator', 'is_subcoordinator', 'area', 'sub_area']


class AreaSerializer(serializers.ModelSerializer):
    """Serializer for areas"""

    class Meta:
        model = Area
        fields = ['id', 'name']
        read_only_fields = ['id']


class AreaDetailSerializer(AreaSerializer):
    """Serializer for area detail view"""

    class Meta(AreaSerializer.Meta):
        fields = AreaSerializer.Meta.fields + ['description']


class SubAreaSerializer(serializers.ModelSerializer):
    """Serializer for subareas"""

    class Meta:
        model = SubArea
        fields = ['id', 'name']
        read_only_fields = ['id']


class SubAreaDetailSerializer(SubAreaSerializer):
    """Serializer for subarea detail view"""

    class Meta(SubAreaSerializer.Meta):
        fields = AreaSerializer.Meta.fields + ['description', 'area_id']