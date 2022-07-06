"""
Test for the areas API"
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase


from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    SubArea,
    Area,
)

from personel.serializers import SubAreaSerializer

SUBAREAS_URL = reverse('personel:subarea-list')

# def create_area():
#     """create and return area."""
#     return Area.objects.create(user=create_user(), name='Pengujian')

def create_user(email='user@example.com', password='testpass123'):
    """Create and return user"""
    return get_user_model().objects.create(email=email, password=password)


class PublicSubAreasApiTest(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()
    
    def test_auth_required(self):
        """Test auth is required for retrieving sub areas."""
        res = self.client.get(SUBAREAS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivatSubAreasApiTest(TestCase):
    """Test authenticated API request."""
 
    def setUp(self):
        self.user = create_user(email='user1@example.com')
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.area = Area.objects.create(user=self.user, name='Pengujian')
    
    def test_retrieve_subareas(self):
        """Test retrieving a list of sub areas."""
        SubArea.objects.create(user=self.user, name="Diklat", area_id=self.area)

        res = self.client.get(SUBAREAS_URL)

        subareas = SubArea.objects.all().order_by('-id')
        serializer = SubAreaSerializer(subareas, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    
        