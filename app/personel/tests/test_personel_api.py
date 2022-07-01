"""
Test for personel APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Personel

from personel.serializers import (
    PersonelSerializer,
    PersonelDetailSerializer,
)


PERSONELS_URL = reverse('personel:personel-list')


def detail_url(personel_id):
    """Create and return a personel detail URL"""
    return reverse('personel:personel-detail', args=[personel_id])

def create_personel(user, **params):
    """Create and return a personel data. """
    defaults = {
        'full_name': 'Auditor Internal',
        'department': 'Sertifikasi',
        'position': 'subkoordinator',
    }
    defaults.update(params)

    personel = Personel.objects.create(user=user, **defaults)
    return personel


class PublicPersonelAPITest(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(PERSONELS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePersonelAPITest(TestCase):
    """Test authenticated API rewquests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_personals(self):
        """Test retrieving a list of personels."""
        create_personel(user=self.user)
        create_personel(user=self.user)

        res = self.client.get(PERSONELS_URL)

        personels = Personel.objects.all().order_by('-id')
        serializer = PersonelSerializer(personels, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_personel_list_limited_to_user(self):
        """Test list of personel is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123'
        )
        create_personel(user=other_user)
        create_personel(user=self.user)

        res = self.client.get(PERSONELS_URL)

        personels = Personel.objects.filter(user=self.user)
        serializer = PersonelSerializer(personels, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_personel_detail(self):
        """Test get personel detail."""
        personel = create_personel(user=self.user)

        url = detail_url(personel.id)
        res = self.client.get(url)

        serializer = PersonelDetailSerializer(personel)
        self.assertEqual(res.data, serializer.data)

    def test_create_personel(self):
        """Test creating personal data."""
        payload = {
            'full_name': 'Auditor Internal',
            'department': 'Sertifikasi',
            'position': 'Koordinator',
        }
        res = self.client.post(PERSONELS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        personel = Personel.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(personel,k), v)
        self.assertEqual(personel.user, self.user)

