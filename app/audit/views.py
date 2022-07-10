"""
Views for the audit APIs.
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Audit, 
    Correctiveaction,
    Standard,
    Standardpoint,
)

from audit import serializers


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'sub-area',
                OpenApiTypes.STR,
                description='Coma separated list of ID to filter',
            ),
        ]
    )
)

class AuditViewSet(viewsets.ModelViewSet):
    """View for manage audit APIs."""
    serializer_class = serializers.AuditDetailSerializer
    queryset = Audit.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def _params_to_ints(self,qs):
    #     """Convert a list of strings to integers."""
    #     return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve personels for authenticated user."""
        user = self.request.user
        if user.is_staff:
            return self.queryset.filter(user=self.request.user).order_by('-id')
        
        sub_area = self.request.query_params.get('sub-area')
        queryset = self.queryset
        if sub_area:
            sub_area_id = sub_area
            queryset = queryset.filter(sub_area=sub_area_id)
        
        return queryset.order_by('-id').distinct()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.AuditSerializer

        return self.serializer_class

    def perform_create(self, serilizer):
        """Add a new data of personel. """
        serilizer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'audit',
                OpenApiTypes.STR,
                description='Coma separated list of ID to filter',
            ),
        ]
    )
)

class CorrectiveViewSet(viewsets.ModelViewSet):
    """View for manage correctives APIs."""
    serializer_class = serializers.CorrectiveSerializer
    queryset = Correctiveaction.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve correctives for authenticated user."""
        # return self.queryset.filter(user=self.request.user).order_by('-id')
        user = self.request.user
        # if user.is_staff:
        #     return self.queryset.filter(user=self.request.user).order_by('-id')
        
        audit = self.request.query_params.get('audit')
        queryset = self.queryset
        if audit:
            audit_id = audit
            queryset = queryset.filter(audit=audit_id)
        print(audit)
        
        return queryset.order_by('-id').distinct()

    def perform_create(self, serilizer):
        """Add a new data of personel. """
        serilizer.save(user=self.request.user)


class StandardViewSet(viewsets.ModelViewSet):
    """View for manage correctives APIs."""
    serializer_class = serializers.StandardSerializer
    queryset = Standard.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve correctives for authenticated user."""
        return self.queryset.order_by('-name')

    def perform_create(self, serilizer):
        """Add a new data of personel. """
        serilizer.save(user=self.request.user)


class StandardpointViewSet(viewsets.ModelViewSet):
    """View for manage audit APIs."""
    serializer_class = serializers.StandardpointDetailSerializer
    queryset = Standardpoint.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve correctives for authenticated user."""
        return self.queryset.order_by('-name')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.StandardpointSerializer

        return self.serializer_class

    def perform_create(self, serilizer):
        """Add a new data of personel. """
        serilizer.save(user=self.request.user)