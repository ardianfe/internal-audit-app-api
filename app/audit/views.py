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
from rest_framework.pagination import PageNumberPagination


from core.models import (
    Audit, 
    Correctiveaction,
    Standard,
    Standardpoint,
)

from audit import serializers


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'area',
                OpenApiTypes.STR,
                description='area id to filter',
            ),
            OpenApiParameter(
                'standard',
                OpenApiTypes.STR,
                description='standar to filter',
            ),
            OpenApiParameter(
                'sub-area',
                OpenApiTypes.STR,
                description='Coma separated list of ID to filter',
            ),
            OpenApiParameter(
                'short',
                OpenApiTypes.STR,
                description='input : sub_area, area, cat, id, standard, nc_point',
            ),
        ]
    )
)

class AuditViewSet(viewsets.ModelViewSet):
    """View for manage audit APIs."""
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.AuditDetailSerializer
    queryset = Audit.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve personels for authenticated user."""
        user = self.request.user
        standard_id = self.request.query_params.get('standard')
        area_id = self.request.query_params.get('area')
        sub_area = self.request.query_params.get('sub-area')
        short = self.request.query_params.get('short')
        queryset = self.queryset

        print(standard_id)

        if short == None:
            short = 'id'

        if area_id:
            area_id = area_id
            queryset = queryset.filter(area=area_id).order_by(short).distinct()
        
        if standard_id:
            standard_id = standard_id
            queryset = queryset.filter(standard__id=standard_id).order_by(short).distinct()

        if sub_area:
            sub_area_id = sub_area
            queryset = queryset.filter(sub_area=sub_area_id).order_by(short).distinct()
        
        if user.is_staff and user.is_superuser:
            return queryset.order_by(short).distinct()
        
        if user.is_staff:
            return queryset.filter(user=self.request.user).order_by(short).distinct()

        
        return queryset.order_by(short).distinct()

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