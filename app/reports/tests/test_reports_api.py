"""
Test for report APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy, reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Audit

from reports.serializers import ReportSerializer

def create_report(user, **params):
    """Create and return a report data"""
    defaults = {
        'sub_area' : 'Diklat',
        'pic': 'sub_koordinator',
        'total': 3,
        'status': 'is_closed'
    }