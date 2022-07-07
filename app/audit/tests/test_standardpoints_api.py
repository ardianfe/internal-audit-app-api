"""
Test for the Standard API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Standard,
    Standardpoint,
)

from audit.serializers import StandardpointSerializer


STDPOINT_URL = reverse_lazy('audit:standardpoint-list')


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicStandardpointsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving standards."""
        res = self.client.get(STDPOINT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateStandardpointApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_standardspoint(self):
        """Test rerieving a list of standards."""
        standard = Standard.objects.create(user=self.user)
        Standardpoint.objects.create(user=self.user, name="Point 1.1", standard_id=standard)
        Standardpoint.objects.create(user=self.user, name="Point 1.2", standard_id=standard)

        res = self.client.get(STDPOINT_URL)

        standardpoints = Standardpoint.objects.all().order_by('-name')
        serializer = StandardpointSerializer(standardpoints, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

