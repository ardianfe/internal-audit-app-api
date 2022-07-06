"""
Test for corrective action APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

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