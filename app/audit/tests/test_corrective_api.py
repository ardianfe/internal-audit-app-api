"""
Test for corrective action APIs.
"""
import tempfile
import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy, reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Correctiveaction,
    Audit,
    Personel,
    Area,
    SubArea
)

from audit.serializers import CorrectiveSerializer


CORRECTIVES_URL = reverse_lazy('audit:corrective-list')


def file_upload_url(corrective_id):
    """Create and return file upload URL."""
    return reverse('audit/correctives:corrective-upload-file', args=[corrective_id])



def create_correctiveaction(user, **params):
    """Create and return corrective action"""
    personel = Personel.objects.create(user=user)
    area = Area.objects.create(user=user)
    sub_area = SubArea.objects.create(user=user, area_id=area)
    audit = Audit.objects.create(user=user, area=area, sub_area=sub_area)
    defaults = {
        'cause_analysis':'penyebab terbesar adalah dari akarnya sendiri',
        'corrective_actions':'tindakan perbaikan sudah dilakukan',
        'due_date':'2022-07-10',
        'prepared_by':personel,
        'pre_actions':'tindakan pencegahan',
        'links':'http://example.com',
        'audit': audit
    }
    defaults.update(params)

    corrective = Correctiveaction.objects.create(user=user, **defaults)
    return corrective


class PublicCorrectiveAPITests(TestCase):
    "Test unauthenticated API requests."

    def setUp(self):
        self.client = APIClient()
    
    def auth_required(self):
        """Test auth is required to call APIs."""
        res = self.client.get(CORRECTIVES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
# class PrivateCorrectiveAPITests(TestCase):
#     """Test authenticated API request."""

#     def setUp(self):
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(
#             'user@example.com',
#             'testpass123'
#         )
#         self.client.force_authenticate(self.user)
    
#     def test_filter_corrective_by_audit_id(self):
#         """Filtering corrective by audit_id"""
#         area1 = Area.objects.create(user=self.user, name='area1')
#         area2 = Area.objects.create(user=self.user, name='area2')
#         sub_area1 = SubArea.objects.create(user=self.user, name='subarea1', area_id=area1)
#         sub_area2 = SubArea.objects.create(user=self.user, name='subarea2', area_id=area2)
#         audit1 = Audit.objects.create(user=self.user, title='Audit Internal B4t', area=area1, sub_area=sub_area1)
#         audit2 = Audit.objects.create(user=self.user, title='Audit Sertifikasi', area=area1, sub_area=sub_area2)
#         c1 = create_correctiveaction(user=self.user, cause_analysis='penyebab1', audit=audit1)
#         c2 = create_correctiveaction(user=self.user, cause_analysis='penyebab1', audit=audit2)
#         c3 = create_correctiveaction(user=self.user, cause_analysis='penyebab')

#         params = {'audit': f'{audit1.id}, {audit2.id}'}
#         res = self.client.get(CORRECTIVES_URL, params=params)

#         s1 = CorrectiveSerializer(c1)
#         s2 = CorrectiveSerializer(c2)
#         s3 = CorrectiveSerializer(c3)
#         self.assertIn(s1.data, res.data)
#         self.assertIn(s2.data, res.data)
#         self.assertIn(s3.data, res.data)



class FileUloadTests(TestCase):
    """Test for the file upload API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'password123',
        )
        self.client.force_authenticate(self.user)
        self.corrective = create_correctiveaction(self.user)

    def tearDown(self):
        self.corrective.evidence.delete()

    # def test_upload_file(self):
    #     """Test uploading a file to a corrective action"""
    #     url = file_upload_url(self.corrective.id)
    #     with tempfile.NamedTemporaryFile(suffix='.pdf') as file:

