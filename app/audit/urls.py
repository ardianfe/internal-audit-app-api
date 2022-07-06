"""
URL mappings for the audit app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from audit import views


router = DefaultRouter()
router.register('ncreports', views.AuditViewSet)
router.register('correctives', views.CorrectiveViewSet)

app_name = 'audit'

urlpatterns = [
    path('', include(router.urls)),
]