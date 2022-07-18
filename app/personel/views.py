"""
Views for the personel APIs.
"""
from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Personel,
    Area,
    SubArea,
)
from personel import serializers


class PersonelViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.PersonelDetailSerializer
    queryset = Personel.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve personels for authenticated user."""
        if self.request.user.is_superuser:
            return self.queryset.order_by('-id')

        # return self.queryset.filter(user=self.request.user).order_by('-id')
        return self.queryset.order_by('-id')
    

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.PersonelSerializer

        return self.serializer_class

    def perform_create(self, serilizer):
        """Add a new data of personel. """
        serilizer.save(user=self.request.user)


class AreaViewSet(viewsets.ModelViewSet):
    """Manage area in the database"""
    serializer_class = serializers.AreaDetailSerializer
    queryset = Area.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated.user"""
        return self.queryset.order_by('-name')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.AreaSerializer
        
        return self.serializer_class

    
    def perform_create(self, serilizer):
        """Add a new area. """
        serilizer.save(user=self.request.user)

class SubAreaViewSet(viewsets.ModelViewSet):
    """Manage area in the database"""
    serializer_class = serializers.SubAreaDetailSerializer
    queryset = SubArea.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated.user"""
        return self.queryset.order_by('-name')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.SubAreaSerializer
        
        return self.serializer_class

    
    def perform_create(self, serilizer):
        """Add a new area. """
        serilizer.save(user=self.request.user)