"""
Test for the Standard API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Standard

from audit.serializers import StandardSerializer


STDS_URL = reverse_lazy('audit:standard-list')


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicStandardsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving standards."""
        res = self.client.get(STDS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateStandardApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_standards(self):
        """Test rerieving a list of standards."""
        Standard.objects.create(user=self.user, name="ISO")
        Standard.objects.create(user=self.user, name="SNI")

        res = self.client.get(STDS_URL)

        standards = Standard.objects.all().order_by('-name')
        serializer = StandardSerializer(standards, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

