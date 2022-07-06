"""
Test for audit APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Audit,
    Area,
    SubArea
)

from audit.serializers import AuditSerializer


AUDITS_URL = reverse('audit:audit-list')

def create_audit(user, **params):
    """Create and return a audit"""
    area = Area.objects.create(user=user)
    sub_area = SubArea.objects.create(user=user, area_id=area)
    defaults = {
        'title': 'Audit Internal PJT',
        'audit_date': '2022-07-05',
        'area': area,
        'sub_area': sub_area,
        'standard': 'ISO 9001',
        'nc_point': '6.4',
        'nc_source': 'Audit Internal',
        'description': 'Penjelasan tentang temuan',
        'is_verified': False,
    }
    defaults.update(params)

    audit = Audit.objects.create(user=user, **defaults)
    return audit


class PublicAuditAPITests(TestCase):
    "Test unauthenticated API requests."

    def setUp(self):
        self.client = APIClient()
    
    def auth_required(self):
        """Test auth is required to call APIs."""
        res = self.client.get(AUDITS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAuditApiTests(TestCase):
    """Test authenticated API request."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_audits(self):
        """Test retrieving a list of audits."""
        create_audit(user=self.user)
        create_audit(user=self.user)

        res = self.client.get(AUDITS_URL)

        audits = Audit.objects.all().order_by('-id')
        serializer = AuditSerializer(audits, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_audit_list_limited_to_user(self):
        """Test list of audits is limited to authenticated users."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123'
        )
        create_audit(user=other_user)
        create_audit(user=self.user)

        res = self.client.get(AUDITS_URL)

        audits = Audit.objects.filter(user=self.user)
        serializer = AuditSerializer(audits, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
