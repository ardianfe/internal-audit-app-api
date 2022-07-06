"""
Tests for the Area API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Area, 
    Personel,
)

from personel.serializers import (
    AreaSerializer,
    AreaDetailSerializer,
)


AREAS_URL = reverse('personel:area-list')


def detail_url(area_id):
    """Create and return a area detail"""
    return reverse('personel:area-detail', args=[area_id])

def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user"""
    return get_user_model().objects.create_user(email=email, password=password)

def create_personel(**params):
    """Create and return a personel data."""
    user3 = create_user(email='user3@example.com')
    defaults = {
        'full_name': 'Auditor Internal',
        'birthday': '1980-01-01'
    }
    defaults.update(params)

    personel = Personel.objects.create(user=user3, **defaults)
    return personel

    
class PublicPersonalAreasTests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving tags."""
        res = self.client.get(AREAS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAreasApiTests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.user = create_user()
        self.coordinator = create_personel()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_areas(self):
        """Test retrieving a list of areas"""
        Area.objects.create(user=self.user, name="Standardidasi", description="Standard description")
        Area.objects.create(user=self.user, name="Sertifikasi", description="Sertifikasi description")

        res = self.client.get(AREAS_URL)

        areas = Area.objects.all().order_by('-name')
        serilizer = AreaSerializer(areas, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serilizer.data)
    
    def test_get_area_detail(self):
        """Test get personel detail."""
        area = Area.objects.create(user=self.user, name='New Area', description='New Area description')

        url = detail_url(area.id)
        res = self.client.get(url)

        serializer = AreaDetailSerializer(area)
        self.assertEqual(res.data, serializer.data)
    
    def test_update_area(self):
        """Test upadating a area"""
        area = Area.objects.create(user=self.user, name='PJT')

        payload = {'name': 'Keuangan'}
        url = detail_url(area.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        area.refresh_from_db()
        self.assertEqual(area.name, payload['name'])

    def test_delete_area(self):
        """Test deleting a area."""
        area = Area.objects.create(user=self.user, name='PJT')

        url = detail_url(area.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        areas = Area.objects.filter(user=self.user)
        self.assertFalse(areas.exists())