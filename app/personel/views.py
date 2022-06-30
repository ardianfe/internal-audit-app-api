"""
Views for the personel APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Personel
from personel import serializers


class PersonelViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.PersonelSerializer
    queryset = Personel.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve personels for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
