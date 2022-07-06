"""
Serializers for audit APIs
"""
from rest_framework import serializers

from core.models import (
    Audit,
    Correctiveaction
)


class AuditSerializer(serializers.ModelSerializer):
    """Serializer for audits"""

    class Meta:
        model = Audit
        fields = ['id', 'title', 'audit_date', 'area', 'sub_area', 'standard', 'nc_point', 'nc_source', 'description']
        read_only_fields = ['id']

class AuditDetailSerializer(AuditSerializer):
    """Serializer for audit details"""

    class Meta(AuditSerializer.Meta):
        fields = AuditSerializer.Meta.fields + ['is_verified']


class CorrectiveSerializer(serializers.ModelSerializer):
    """Serilizer for corrective actions"""

    class Meta:
        model = Correctiveaction
        fields = ['id', 'cause_analysis', 'corrective_actions', 'due_date', 'prepared_by', 'pre_actions', 'links', 'audit']
        read_only_fields = ['id']
